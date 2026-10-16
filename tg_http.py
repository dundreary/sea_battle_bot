"""Bounded HTTP retry for outbound Telegram Bot API calls.

This module is side-effect free at import time: it performs no I/O when
imported, owns no threads, and imports no project modules. All retry policy,
rate-limit honoring and error logging for the two Telegram call sites
(notifications.py and strip.py) lives here so they can stay thin.

Delivery guarantee: :func:`telegram_post` never raises. Every failure path
logs and returns ``False``, so a delivery failure can never affect a game move
(the callers' documented contract).

Retry policy:
* HTTP 429 (flood control) -> retry, honoring ``parameters.retry_after`` but
  capped at :data:`TELEGRAM_RETRY_AFTER_CAP` (a very large ``retry_after`` --
  e.g. the daily limit -- can never stall a game thread). Unreadable bodies or
  a missing ``retry_after`` fall back to :data:`TELEGRAM_BACKOFF`.
* Network-level :class:`urllib.error.URLError` (connection refused, DNS,
  ``socket.timeout`` -- all wrapped by urllib in URLError) -> retry after
  :data:`TELEGRAM_BACKOFF`.

Permanent (no retry): any other HTTP status (400/401/403/404 AND 5xx, because
retrying ``sendPhoto``/``sendMessage`` after a server error risks emitting a
duplicate message), and a 200 with ``ok:false``.

Per the Bot API: ``retry_after`` is "the number of seconds left to wait before
the request can be repeated" (Parameters object, core.telegram.org/bots/api).
"""
import json
import logging
import time
import urllib.error
import urllib.request

logger = logging.getLogger(__name__)

# At most this many urlopen attempts per call (Telegram 429 / transient network).
TELEGRAM_MAX_ATTEMPTS = 3
# Never sleep longer than this when honoring a rate-limit retry_after, so a
# burst throttle can never stall the request thread (or the state-lock-free
# strip-photo path) unbounded.
TELEGRAM_RETRY_AFTER_CAP = 5.0
# Fallback wait for transient network failures and for unreadable 429 bodies.
TELEGRAM_BACKOFF = 1.0


def _retry_after(err):
    """Best-effort extraction of ``retry_after`` from a 429 HTTPError body.

    Returns a value capped at ``TELEGRAM_RETRY_AFTER_CAP``. If the body is
    unreadable or lacks ``retry_after``, falls back to ``TELEGRAM_BACKOFF``.
    """
    try:
        data = json.loads(err.read())
    except (ValueError, OSError, TypeError):
        return TELEGRAM_BACKOFF
    try:
        wait = data["parameters"]["retry_after"]
        return min(float(wait), TELEGRAM_RETRY_AFTER_CAP)
    except (KeyError, TypeError, ValueError):
        return TELEGRAM_BACKOFF


def telegram_post(req, attempts=TELEGRAM_MAX_ATTEMPTS, timeout=30, sleep=time.sleep):
    """POST a ready ``urllib`` Request to the Telegram Bot API with bounded retry.

    Returns ``True`` when Telegram answers ``ok:true``. ``urlopen`` is invoked
    through the ``urllib.request`` module attribute so tests can monkeypatch
    ``urllib.request.urlopen``. ``sleep`` is injectable only so tests can pass a
    no-op/recorder; production uses ``time.sleep``. Never raises.
    """
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            # HTTPError subclasses URLError (and OSError), so it MUST be caught
            # first, otherwise a 429 would be swallowed by the URLError branch.
            if e.code == 429:
                wait = _retry_after(e)
                logger.warning(
                    "Telegram 429 rate-limited (attempt %d/%d); retrying after %.1fs",
                    attempt + 1, attempts, wait,
                )
                # Don't sleep on the final attempt -- there is no next attempt
                # to make, so the sleep only delays giving up.
                if attempt < attempts - 1:
                    sleep(wait)
                continue
            # Permanent HTTP failure (400/401/403/404, and 5xx). 5xx is NOT
            # retried: a retried sendPhoto/sendMessage after a server error
            # risks delivering a duplicate message to the user.
            logger.error("Telegram HTTP %s: %s", e.code, e)
            return False
        except urllib.error.URLError as e:
            # Network-level transient: connection refused, DNS failure,
            # socket.timeout -- urllib wraps these in URLError.
            logger.warning(
                "Transient Telegram network error (attempt %d/%d): %s",
                attempt + 1, attempts, e,
            )
            # Same as the 429 branch: no point sleeping if this was the last
            # attempt -- there is nothing left to retry.
            if attempt < attempts - 1:
                sleep(TELEGRAM_BACKOFF)
            continue
        except ValueError as e:
            # Malformed JSON body: not a transport condition worth retrying.
            logger.error("Telegram response not JSON: %s", e)
            return False
        except Exception as e:  # never raise from a delivery call
            logger.error("Unexpected Telegram error: %r", e)
            return False

        # urlopen succeeded; inspect the Telegram payload.
        if isinstance(data, dict) and data.get('ok'):
            return True
        # 200 OK with ok:false, or a non-object body: permanent API failure.
        logger.error("Telegram API error: %s", data)
        return False

    logger.error(
        "Telegram request failed after %d attempts; giving up", attempts
    )
    return False
