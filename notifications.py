"""Telegram notification delivery system.

Game handlers run on a separate HTTP thread and ask to notify a player
(e.g. "it's your turn") by enqueuing a message here. A single background
worker drains the queue so that slow network calls to Telegram never block
the request handlers that mutate game state.
"""
import json
import logging
import queue
import threading
import time
import urllib.request

import config

logger = logging.getLogger(__name__)

# The browser polls every two seconds. A recent poll means the player is
# already looking at the game, so a Telegram notification would be noise.
NOTIFY_SKIP_IF_ACTIVE_WITHIN = 5.0

_notification_queue: "queue.Queue" = queue.Queue(maxsize=100)


def send_telegram_message(chat_id, text: str) -> bool:
    """Send a text notification; delivery failures never affect a game move."""
    try:
        req = urllib.request.Request(
            f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage',
            data=json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            if result.get('ok'):
                return True
            logger.error("Telegram API error: %s", result)
            return False
    except Exception as exc:
        logger.error("Failed to send Telegram notification: %s", exc)
        return False


def _notification_worker():
    while True:
        chat_id, text = _notification_queue.get()
        try:
            send_telegram_message(chat_id, text)
        finally:
            _notification_queue.task_done()


threading.Thread(target=_notification_worker, name="telegram-notifications", daemon=True).start()


def _enqueue_notifications(pending):
    """Queue delivery only after releasing the state lock."""
    for chat_id, text in pending:
        try:
            _notification_queue.put_nowait((chat_id, text))
        except queue.Full:
            logger.warning("Telegram notification queue is full; dropping message for %s", chat_id)


def mark_active(game, uid):
    """Record that ``uid`` has just received and is displaying game state."""
    if uid:
        if not hasattr(game, 'last_activity'):
            game.last_activity = {}
        game.last_activity[str(uid)] = time.time()


def notify_recipient(game, recipient, text, event_key, force=False):
    """Return one deduplicated notification, unless its recipient is active."""
    if getattr(game, 'solo', False) or not recipient:
        return []
    events = getattr(game, 'notification_events', None)
    if events is None:
        events = game.notification_events = set()
    if event_key in events:
        return []
    events.add(event_key)
    if not force:
        last_seen = getattr(game, 'last_activity', {}).get(str(recipient), 0)
        if time.time() - last_seen < NOTIFY_SKIP_IF_ACTIVE_WITHIN:
            return []
    return [(recipient, text)]


def notify_opponent(game, uid, text, event_key, force=False):
    opponent_id = game.opponent_id(uid) if hasattr(game, 'opponent_id') else (
        game.player2_id if uid == game.player1_id else game.player1_id
    )
    return notify_recipient(game, opponent_id, text, event_key, force=force)
