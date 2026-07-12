"""Strip-mode stake-photo delivery.

When a strip-mode game ends, the loser's pre-committed "stake" photo is
delivered to the winner over Telegram. The photo arrives as a browser
data-URL, so we decode it and POST it as multipart/form-data.
"""
import base64
import json
import logging
import secrets
import urllib.request

import config

logger = logging.getLogger(__name__)

STRIP_LOSE_CAPTIONS = {
    'ru': '👗 Твой друг проиграл в режиме «На раздевание»!',
    'uk': '👗 Твій друг програв у режимі «На роздягання»!',
    'en': '👗 Your friend lost in Strip Mode!',
}

STRIP_PHOTO_BOUNDARY = '----StripPhotoBoundary'


def _strip_photo_mime(photo_data: str) -> str:
    if ',' in photo_data:
        header = photo_data.split(',', 1)[0].lower()
        if 'png' in header:
            return 'image/png'
        if 'gif' in header:
            return 'image/gif'
        if 'webp' in header:
            return 'image/webp'
    return 'image/jpeg'


def _strip_photo_multipart(boundary: str, winner_id: int, photo_bytes: bytes, caption: str, mime: str) -> bytes:
    body = b''
    body += f'--{boundary}\r\n'.encode()
    body += 'Content-Disposition: form-data; name="chat_id"\r\n\r\n'.encode()
    body += f'{winner_id}\r\n'.encode()
    body += f'--{boundary}\r\n'.encode()
    body += 'Content-Disposition: form-data; name="caption"\r\n\r\n'.encode()
    body += f'{caption}\r\n'.encode()
    body += f'--{boundary}\r\n'.encode()
    body += 'Content-Disposition: form-data; name="photo"; filename="strip_photo.jpg"\r\n'.encode()
    body += f'Content-Type: {mime}\r\n\r\n'.encode()
    body += photo_bytes + b'\r\n'
    body += f'--{boundary}--\r\n'.encode()
    return body


def send_strip_photo_to_winner(winner_id: int, photo_data: str, caption: str) -> bool:
    try:
        mime = _strip_photo_mime(photo_data)
        b64_data = photo_data.split(',', 1)[1] if ',' in photo_data else photo_data
        photo_bytes = base64.b64decode(b64_data)
        # A unique boundary per request removes any chance of the binary
        # photo bytes being mistaken for a multipart boundary.
        boundary = STRIP_PHOTO_BOUNDARY + secrets.token_hex(16)
        body = _strip_photo_multipart(boundary, winner_id, photo_bytes, caption, mime)

        req = urllib.request.Request(
            f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendPhoto',
            data=body,
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            if result.get('ok'):
                return True
            logger.error("Telegram API error: %s", result)
            return False
    except Exception as e:
        logger.error("Failed to send strip photo: %s", e)
        return False
