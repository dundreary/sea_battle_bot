import secrets
import string


def make_game_code(length: int = 6) -> str:
    """Generate a short, human-friendly uppercase game code."""
    return "".join(secrets.choice(string.ascii_uppercase) for _ in range(length))
