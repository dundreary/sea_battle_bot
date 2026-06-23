import os
import random
import time
import uuid
from collections import Counter

WORD_LIST = None
BASE_WORDS = None

def _load_words():
    global WORD_LIST, BASE_WORDS
    path = os.path.join(os.path.dirname(__file__), 'data', 'uk_words.txt')
    with open(path, 'r', encoding='utf-8') as f:
        words = {line.strip().lower() for line in f if line.strip()}
    WORD_LIST = words
    BASE_WORDS = sorted(w for w in words if len(w) == 6)

def _scoring(n):
    return 100 * (n - 2) ** 2

def _can_form(word, letters):
    wc = Counter(word)
    lc = Counter(letters)
    for ch, cnt in wc.items():
        if lc.get(ch, 0) < cnt:
            return False
    return True

def _find_all_words(letters):
    result = []
    for w in WORD_LIST:
        if len(w) < 3 or len(w) > 6:
            continue
        if _can_form(w, letters):
            result.append(w)
    return sorted(result)

_load_words()

rooms = {}
games = {}

def _code():
    return ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ', k=5))

def _new_state(letters, all_words, solo):
    return {
        'letters': letters,
        'all_words': all_words,
        'found': [],
        'score': 0,
        'hints_used': 0,
        'started_at': time.time(),
        'time_limit': 60,
        'finished': False,
        'solo': solo,
    }

def new_solo():
    letters = random.choice(BASE_WORDS)
    all_words = _find_all_words(letters)
    sid = str(uuid.uuid4())
    games[sid] = _new_state(letters, all_words, True)
    return sid, games[sid]

def new_multi():
    letters = random.choice(BASE_WORDS)
    all_words = _find_all_words(letters)
    code = _code()
    while code in rooms:
        code = _code()
    sid = str(uuid.uuid4())
    games[sid] = _new_state(letters, all_words, False)
    rooms[code] = {'letters': letters, 'all_words': all_words, 'p1_sid': sid, 'p2_sid': None}
    return sid, code, games[sid]

def join(code):
    room = rooms.get(code.upper())
    if not room:
        return None, 'not_found'
    if room['p2_sid'] is not None:
        return None, 'full'
    sid = str(uuid.uuid4())
    games[sid] = _new_state(room['letters'], room['all_words'], False)
    room['p2_sid'] = sid
    return sid, 'ok', games[sid]

def guess(sid, word):
    g = games.get(sid)
    if not g or g['finished']:
        return None, 'game_over'
    word = word.strip().lower()
    if not word or not word.isalpha():
        return None, 'invalid'
    if len(word) < 3 or len(word) > 6:
        return None, 'length'
    if word in g['found']:
        return None, 'duplicate'
    if word not in g['all_words']:
        return None, 'not_a_word'
    if not _can_form(word, g['letters']):
        return None, 'invalid'
    score = _scoring(len(word))
    g['found'].append(word)
    g['score'] += score
    return 'ok', {'word': word, 'score': score, 'total': g['score']}

def hint(sid):
    g = games.get(sid)
    if not g or g['finished']:
        return None
    unfound = [w for w in g['all_words'] if w not in g['found']]
    if not unfound:
        return None
    word = random.choice(unfound)
    g['found'].append(word)
    g['score'] = max(0, g['score'] - 200)
    g['hints_used'] += 1
    return {'word': word, 'penalty': 200, 'total': g['score']}

def get_state(sid):
    g = games.get(sid)
    if not g:
        return None
    elapsed = time.time() - g['started_at']
    remaining = max(0, g['time_limit'] - int(elapsed))
    if remaining <= 0 and not g['finished']:
        g['finished'] = True
    all_words_count = len(g['all_words'])
    return {
        'letters': g['letters'],
        'found': sorted(g['found']),
        'score': g['score'],
        'remaining': remaining,
        'hints_used': g['hints_used'],
        'finished': g['finished'],
        'solo': g['solo'],
        'total_words': all_words_count,
        'found_count': len(g['found']),
    }
