"""Telegram WebApp init_data verification.

Telegram Mini Apps hand the page a client-side ``initDataUnsafe`` object that
is trivial to spoof (it's just JS the browser executed), plus a separate
signed ``initData`` string. Only the signed string proves who the user
actually is. This module verifies that signature so the server can derive a
trustworthy user id instead of taking the client's word for it.

Algorithm: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
"""
import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl


def validate_init_data(init_data: str, bot_token: str, max_age_seconds: int = 86400):
    """Return the verified numeric Telegram user id, or None if ``init_data``
    is missing, malformed, unsigned, too old, or doesn't match ``bot_token``.

    ``max_age_seconds`` guards against a leaked/replayed init_data string
    being reused long after the session that generated it; it's generous
    (24h) because a webapp tab can legitimately stay open and polling for a
    while without the user re-launching it.
    """
    if not init_data or not bot_token:
        return None
    try:
        pairs = parse_qsl(init_data, strict_parsing=True, keep_blank_values=True)
    except ValueError:
        return None
    parsed = dict(pairs)
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        return None

    check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(computed_hash, received_hash):
        return None

    auth_date = parsed.get("auth_date")
    if auth_date:
        try:
            if time.time() - int(auth_date) > max_age_seconds:
                return None
        except ValueError:
            pass

    user_raw = parsed.get("user")
    if not user_raw:
        return None
    try:
        user = json.loads(user_raw)
        return int(user["id"])
    except (ValueError, KeyError, TypeError):
        return None
