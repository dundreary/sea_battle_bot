"""Security response headers for the embedded HTTP handlers in ``main.py``.

This module is intentionally standalone: it has **no dependency on
``telegram``** (or any other third-party package), so it can be imported and
unit-tested in environments where ``python-telegram-bot`` is not installed
(e.g. the smoke test harness, which only exercises ``main.py`` by reading its
source text). The bot-facing Telegram Mini App runs inside an ``<iframe>``
served from ``https://web.telegram.org`` / ``webk`` / ``webz``, so the
``Content-Security-Policy`` below must permit those frames while still locking
down everything else.
"""

# Ordered list of (name, value) pairs emitted verbatim by
# ``send_security_headers``. Order is asserted by the smoke test so the CSP
# ships first (most browsers evaluate headers in order) and the no-op
# ``X-Frame-Options`` is never added (it would ``DENY`` framing and break the
# Telegram Web/Desktop client which embeds the app in an iframe).
SECURITY_HEADERS = [
    (
        "Content-Security-Policy",
        "frame-ancestors https://web.telegram.org https://webk.telegram.org "
        "https://webz.telegram.org 'self'; object-src 'none'",
    ),
    ("X-Content-Type-Options", "nosniff"),
    ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
    ("Referrer-Policy", "strict-origin"),
]


def send_security_headers(send_header):
    """Emit the security headers via ``send_header(name, value)``.

    ``send_header`` is the bound ``BaseHTTPRequestHandler.send_header`` method
    (or any ``callable(str, str)`` in tests): each header is forwarded as a
    plain ``(name, value)`` pair so it slots into an existing
    ``send_response`` -> ``send_header`` -> ``end_headers`` sequence without
    changing the handler's own ``Content-Type`` / ``Content-Length`` logic.
    """
    for name, value in SECURITY_HEADERS:
        send_header(name, value)
