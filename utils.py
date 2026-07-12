import random
import string


def make_game_code(length: int = 6) -> str:
    """Generate a short, human-friendly uppercase game code."""
    return "".join(random.choices(string.ascii_uppercase, k=length))
