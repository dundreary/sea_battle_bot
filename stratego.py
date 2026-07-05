import random
import time

BOARD_SIZE = 10
EMPTY = 0
LAKE = 99

# Piece types
FLAG = 1
SPY = 2
SCOUT = 3
MINER = 4
SERGEANT = 5
LIEUTENANT = 6
CAPTAIN = 7
MAJOR = 8
COLONEL = 9
GENERAL = 10
MARSHAL = 11
BOMB = 12

PIECE_NAMES = {
    FLAG: 'F', SPY: 'S', SCOUT: 's', MINER: 'M',
    SERGEANT: '5', LIEUTENANT: '6', CAPTAIN: '7',
    MAJOR: '8', COLONEL: '9', GENERAL: '10', MARSHAL: '11',
    BOMB: 'B',
}

PIECE_TITLES = {
    FLAG: 'Флаг', SPY: 'Шпион', SCOUT: 'Разведчик', MINER: 'Минёр',
    SERGEANT: 'Сержант', LIEUTENANT: 'Лейтенант', CAPTAIN: 'Капитан',
    MAJOR: 'Майор', COLONEL: 'Полковник', GENERAL: 'Генерал', MARSHAL: 'Маршал',
    BOMB: 'Бомба',
}

PIECE_TITLES_EN = {
    FLAG: 'Flag', SPY: 'Spy', SCOUT: 'Scout', MINER: 'Miner',
    SERGEANT: 'Sergeant', LIEUTENANT: 'Lieutenant', CAPTAIN: 'Captain',
    MAJOR: 'Major', COLONEL: 'Colonel', GENERAL: 'General', MARSHAL: 'Marshal',
    BOMB: 'Bomb',
}

PIECE_TITLES_UK = {
    FLAG: 'Прапор', SPY: 'Шпигун', SCOUT: 'Розвідник', MINER: 'Мінер',
    SERGEANT: 'Сержант', LIEUTENANT: 'Лейтенант', CAPTAIN: 'Капітан',
    MAJOR: 'Майор', COLONEL: 'Полковник', GENERAL: 'Генерал', MARSHAL: 'Маршал',
    BOMB: 'Бомба',
}

CAN_MOVE = {FLAG: False, BOMB: False}

def get_piece_title(ptype, lang='ru'):
    if lang == 'en':
        return PIECE_TITLES_EN.get(ptype, '?')
    if lang in ('uk', 'ua'):
        return PIECE_TITLES_UK.get(ptype, '?')
    return PIECE_TITLES.get(ptype, '?')

PLAYER1 = 1
PLAYER2 = 2

LAKE_CELLS = {(4, 2), (4, 3), (5, 2), (5, 3),
              (4, 6), (4, 7), (5, 6), (5, 7)}

INITIAL_PIECES = [
    (SCOUT, 8), (MINER, 5), (SERGEANT, 4), (LIEUTENANT, 4),
    (CAPTAIN, 4), (MAJOR, 3), (COLONEL, 2), (GENERAL, 1),
    (MARSHAL, 1), (SPY, 1), (BOMB, 6), (FLAG, 1),
]

def initial_piece_list():
    pieces = []
    for ptype, count in INITIAL_PIECES:
        pieces.extend([ptype] * count)
    return pieces

def opponent(p):
    return PLAYER2 if p == PLAYER1 else PLAYER1

def in_bounds(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

def is_lake(r, c):
    return (r, c) in LAKE_CELLS

def is_water(r, c):
    return not in_bounds(r, c) or (r, c) in LAKE_CELLS

def cell_owner(val):
    if val == EMPTY or val == LAKE:
        return None
    return PLAYER1 if val > 0 else PLAYER2

def cell_type(val):
    return abs(val)

def can_move(ptype):
    return ptype not in CAN_MOVE or CAN_MOVE[ptype]

def encode(r, c):
    return r * BOARD_SIZE + c

def new_board():
    board = [EMPTY] * (BOARD_SIZE * BOARD_SIZE)
    for r, c in LAKE_CELLS:
        board[encode(r, c)] = LAKE
    return board

def set_piece(board, r, c, ptype, owner):
    board[encode(r, c)] = ptype if owner == PLAYER1 else -ptype

def get_piece(board, r, c):
    return board[encode(r, c)]

def pieces_on_board(board, owner):
    result = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            val = board[encode(r, c)]
            if val == EMPTY or val == LAKE:
                continue
            if cell_owner(val) == owner and can_move(cell_type(val)):
                result.append((r, c))
    return result

def has_movable_pieces(board, owner):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            val = board[encode(r, c)]
            if val == EMPTY or val == LAKE:
                continue
            if cell_owner(val) == owner:
                pt = cell_type(val)
                if can_move(pt):
                    return True
    return False

def has_flag(board, owner):
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            val = board[encode(r, c)]
            if val == EMPTY or val == LAKE:
                continue
            if cell_owner(val) == owner and cell_type(val) == FLAG:
                return True
    return False

def scout_moves(board, r, c, owner):
    moves = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        while in_bounds(nr, nc) and (nr, nc) not in LAKE_CELLS:
            val = board[encode(nr, nc)]
            if val == EMPTY:
                moves.append((nr, nc))
            elif val != LAKE:
                if cell_owner(val) != owner:
                    moves.append((nr, nc))
                break
            nr += dr
            nc += dc
    return moves

def normal_moves(board, r, c, owner):
    moves = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if not in_bounds(nr, nc) or (nr, nc) in LAKE_CELLS:
            continue
        val = board[encode(nr, nc)]
        if val == EMPTY:
            moves.append((nr, nc))
        elif val != LAKE and cell_owner(val) != owner:
            moves.append((nr, nc))
    return moves

def get_moves(board, r, c):
    val = board[encode(r, c)]
    if val == EMPTY or val == LAKE:
        return []
    owner = cell_owner(val)
    ptype = cell_type(val)
    if not can_move(ptype):
        return []
    if ptype == SCOUT:
        return scout_moves(board, r, c, owner)
    return normal_moves(board, r, c, owner)

PIECE_RANK = {
    SPY: 1, SCOUT: 2, MINER: 3, SERGEANT: 4,
    LIEUTENANT: 5, CAPTAIN: 6, MAJOR: 7,
    COLONEL: 8, GENERAL: 9, MARSHAL: 10,
    BOMB: 0, FLAG: -1,
}

def resolve_combat(attacker_type, defender_type):
    if defender_type == FLAG:
        return 'attacker_wins'
    if attacker_type == MINER and defender_type == BOMB:
        return 'attacker_wins'
    if defender_type == BOMB:
        return 'defender_wins'
    if attacker_type == SPY and defender_type == MARSHAL:
        return 'attacker_wins'
    ar = PIECE_RANK.get(attacker_type, 0)
    dr = PIECE_RANK.get(defender_type, 0)
    if ar > dr:
        return 'attacker_wins'
    elif dr > ar:
        return 'defender_wins'
    else:
        return 'both_removed'

def apply_move(board, r, c, nr, nc):
    val = board[encode(r, c)]
    tval = board[encode(nr, nc)]
    owner = cell_owner(val)
    ptype = cell_type(val)
    if tval == EMPTY:
        board[encode(r, c)] = EMPTY
        board[encode(nr, nc)] = val
        return {'result': 'move', 'captured': None, 'attacker_rank': ptype, 'defender_rank': None}
    defender_type = cell_type(tval)
    result = resolve_combat(ptype, defender_type)
    board[encode(r, c)] = EMPTY
    if result == 'attacker_wins':
        board[encode(nr, nc)] = val
        return {'result': 'attack_win', 'captured': defender_type, 'attacker_rank': ptype, 'defender_rank': defender_type}
    elif result == 'defender_wins':
        board[encode(nr, nc)] = tval
        return {'result': 'attack_lose', 'captured': ptype, 'attacker_rank': ptype, 'defender_rank': defender_type}
    else:
        board[encode(nr, nc)] = EMPTY
        return {'result': 'both_removed', 'captured': ptype, 'attacker_rank': ptype, 'defender_rank': defender_type}

def setup_placement():
    pieces = initial_piece_list()
    random.shuffle(pieces)
    return pieces

def board_to_dict(board):
    return list(board)

def dict_to_board(d):
    return list(d)

class StrategoGame:
    def __init__(self, code, player1_id, solo=False, difficulty=2):
        self.code = code
        self.player1_id = player1_id
        self.player2_id = None
        self.solo = solo
        self.difficulty = difficulty
        self.board = new_board()
        self.phase = 'setup_p1'
        self.turn = PLAYER1
        self.winner = None
        self.created_at = time.time()
        self.p1_pieces = setup_placement()
        self.p2_pieces = setup_placement()
        self.p1_placed = []
        self.p2_placed = []
        self.last_battle = None
        self.game_over = False

    def player_color(self, uid):
        if uid == self.player1_id:
            return PLAYER1
        if uid == self.player2_id or (self.solo and uid == 0):
            return PLAYER2
        return None

    def current_player(self):
        return self.player1_id if self.turn == PLAYER1 else self.player2_id

    def switch_turn(self):
        self.turn = opponent(self.turn)

    def place_piece(self, uid, r, c, ptype):
        owner = self.player_color(uid)
        if owner is None:
            return False, 'not_in_game'
        if self.phase == 'setup_p1' and owner == PLAYER1:
            pass
        elif self.phase == 'setup_p2' and owner == PLAYER2:
            pass
        else:
            return False, 'wrong_phase'
        if not in_bounds(r, c) or is_lake(r, c):
            return False, 'invalid_cell'
        if owner == PLAYER1 and r > 3:
            return False, 'wrong_zone'
        if owner == PLAYER2 and r < 6:
            return False, 'wrong_zone'
        if self.board[encode(r, c)] != EMPTY:
            return False, 'occupied'
        piece_list = self.p1_pieces if owner == PLAYER1 else self.p2_pieces
        placed_list = self.p1_placed if owner == PLAYER1 else self.p2_placed
        if placed_list.count(ptype) >= piece_list.count(ptype):
            return False, 'no_more_of_type'
        placed_list.append(ptype)
        set_piece(self.board, r, c, ptype, owner)
        return True, 'placed'

    def remove_placed(self, uid, r, c):
        owner = self.player_color(uid)
        if owner is None:
            return False
        val = self.board[encode(r, c)]
        if val == EMPTY or val == LAKE or cell_owner(val) != owner:
            return False
        ptype = cell_type(val)
        placed_list = self.p1_placed if owner == PLAYER1 else self.p2_placed
        if ptype in placed_list:
            placed_list.remove(ptype)
        self.board[encode(r, c)] = EMPTY
        return True

    def confirm_setup(self, uid):
        owner = self.player_color(uid)
        if owner is None:
            return False, 'not_in_game'
        piece_list = self.p1_pieces if owner == PLAYER1 else self.p2_pieces
        placed_list = self.p1_placed if owner == PLAYER1 else self.p2_placed
        if len(placed_list) != len(piece_list):
            return False, f'need_{len(piece_list) - len(placed_list)}_more'
        if owner == PLAYER1 and self.phase == 'setup_p1':
            if self.solo or not self.player2_id:
                self.auto_setup(self.player2_id or 0)
                self.phase = 'playing'
                self.turn = PLAYER1
            else:
                self.phase = 'setup_p2'
            return True, 'confirmed'
        elif owner == PLAYER2 and self.phase == 'setup_p2':
            self.phase = 'playing'
            self.turn = PLAYER1
            return True, 'confirmed'
        return False, 'wrong_phase'

    def move(self, uid, r, c, nr, nc):
        owner = self.player_color(uid)
        if owner is None:
            return None, 'not_in_game'
        if self.phase != 'playing':
            return None, 'not_playing'
        if self.turn != owner:
            return None, 'not_your_turn'
        val = self.board[encode(r, c)]
        if val == EMPTY or val == LAKE or cell_owner(val) != owner:
            return None, 'not_your_piece'
        ptype = cell_type(val)
        if not can_move(ptype):
            return None, 'cannot_move'
        moves = get_moves(self.board, r, c)
        if (nr, nc) not in moves:
            return None, 'illegal_move'
        result = apply_move(self.board, r, c, nr, nc)
        self.last_battle = result

        over = False
        if not has_flag(self.board, opponent(owner)):
            self.winner = owner
            self.phase = 'finished'
            self.game_over = True
            over = True
        elif not has_movable_pieces(self.board, opponent(owner)):
            self.winner = owner
            self.phase = 'finished'
            self.game_over = True
            over = True

        if not over:
            self.switch_turn()

        return result, 'ok'

    def auto_setup(self, uid):
        owner = self.player_color(uid)
        if owner is None:
            owner = PLAYER2 if uid == (self.player2_id or 0) else None
        if owner is None:
            return False
        piece_list = self.p1_pieces if owner == PLAYER1 else self.p2_pieces
        placed_list = self.p1_placed if owner == PLAYER1 else self.p2_placed
        placed_list.clear()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = self.board[encode(r, c)]
                if val != EMPTY and val != LAKE and cell_owner(val) == owner:
                    self.board[encode(r, c)] = EMPTY
        rows = range(0, 4) if owner == PLAYER1 else range(6, 10)
        cells = [(r, c) for r in rows for c in range(BOARD_SIZE) if not is_lake(r, c)]
        random.shuffle(cells)
        sorted_pieces = sorted(piece_list, key=lambda p: PIECE_RANK.get(p, 0), reverse=True)
        for i, (r, c) in enumerate(cells):
            if i >= len(sorted_pieces):
                break
            ptype = sorted_pieces[i]
            placed_list.append(ptype)
            set_piece(self.board, r, c, ptype, owner)
        return True

    def get_remaining_pieces(self, uid):
        owner = self.player_color(uid)
        if owner is None:
            return {}
        piece_list = self.p1_pieces if owner == PLAYER1 else self.p2_pieces
        placed_list = self.p1_placed if owner == PLAYER1 else self.p2_placed
        remaining = {}
        for ptype in set(piece_list):
            total = piece_list.count(ptype)
            used = placed_list.count(ptype)
            if total - used > 0:
                remaining[ptype] = total - used
        return remaining

    HIDDEN = -99

    def get_state(self, uid):
        owner = self.player_color(uid)
        hidden_board = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = self.board[encode(r, c)]
                if val == EMPTY:
                    hidden_board.append(0)
                elif val == LAKE:
                    hidden_board.append(99)
                elif self.phase == 'playing':
                    occ = cell_owner(val)
                    if occ == owner:
                        hidden_board.append(val)
                    else:
                        hidden_board.append(self.HIDDEN)
                else:
                    occ = cell_owner(val)
                    if occ == owner:
                        hidden_board.append(val)
                    elif occ is None:
                        hidden_board.append(val)
                    else:
                        hidden_board.append(self.HIDDEN)
        visible_board = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = self.board[encode(r, c)]
                if val == EMPTY:
                    visible_board.append(0)
                elif val == LAKE:
                    visible_board.append(99)
                else:
                    visible_board.append(val)

        my_turn = self.turn == owner
        remaining = self.get_remaining_pieces(uid) if self.phase in ('setup_p1', 'setup_p2') else {}
        return {
            'code': self.code,
            'phase': self.phase,
            'turn': self.turn,
            'my_turn': my_turn,
            'you': uid,
            'solo': self.solo,
            'difficulty': self.difficulty,
            'winner': self.winner,
            'game_over': self.game_over,
            'board': hidden_board,
            'full_board': visible_board,
            'last_battle': self.last_battle,
            'remaining_pieces': {str(k): v for k, v in remaining.items()},
        }

    @staticmethod
    def generate_code():
        return ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ', k=6))

    def to_dict(self):
        return {
            'code': self.code,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'solo': self.solo,
            'difficulty': self.difficulty,
            'board': board_to_dict(self.board),
            'phase': self.phase,
            'turn': self.turn,
            'winner': self.winner,
            'created_at': self.created_at,
            'p1_pieces': list(self.p1_pieces),
            'p2_pieces': list(self.p2_pieces),
            'p1_placed': list(self.p1_placed),
            'p2_placed': list(self.p2_placed),
            'last_battle': self.last_battle,
            'game_over': self.game_over,
        }

    @staticmethod
    def from_dict(data):
        g = StrategoGame.__new__(StrategoGame)
        g.code = data['code']
        g.player1_id = data['player1_id']
        g.player2_id = data.get('player2_id')
        g.solo = data.get('solo', False)
        g.difficulty = data.get('difficulty', 2)
        g.board = dict_to_board(data['board'])
        g.phase = data['phase']
        g.turn = data['turn']
        g.winner = data.get('winner')
        g.created_at = data.get('created_at', 0)
        g.p1_pieces = list(data.get('p1_pieces', initial_piece_list()))
        g.p2_pieces = list(data.get('p2_pieces', initial_piece_list()))
        g.p1_placed = list(data.get('p1_placed', []))
        g.p2_placed = list(data.get('p2_placed', []))
        g.last_battle = data.get('last_battle')
        g.game_over = data.get('game_over', False)
        return g


# AI
def ai_get_move(game, difficulty=None):
    if difficulty is None:
        difficulty = getattr(game, 'difficulty', 2)
    board = game.board
    pieces = pieces_on_board(board, PLAYER2)
    if not pieces:
        return None

    if difficulty <= 1:
        random.shuffle(pieces)
        for r, c in pieces:
            moves = get_moves(board, r, c)
            if moves:
                nr, nc = random.choice(moves)
                return (r, c, nr, nc)
        return None

    random.shuffle(pieces)
    if difficulty >= 3:
        own_types = {}
        for rr in range(BOARD_SIZE):
            for cc in range(BOARD_SIZE):
                v = board[encode(rr, cc)]
                if v < 0 and v != LAKE:
                    own_types[(rr, cc)] = cell_type(v)

    best_overall = None
    best_overall_score = -999
    for r, c in pieces:
        moves = get_moves(board, r, c)
        if not moves:
            continue
        own_val = board[encode(r, c)]
        own_type = cell_type(own_val)
        random.shuffle(moves)
        for nr, nc in moves:
            tval = board[encode(nr, nc)]
            if tval == EMPTY:
                score = 0
                if difficulty >= 3 and own_type in (MARSHAL, GENERAL):
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        cr, cc = nr + dr, nc + dc
                        if in_bounds(cr, cc) and not is_lake(cr, cc):
                            cv = board[encode(cr, cc)]
                            if cv > 0:
                                ctype = cell_type(cv)
                                if ctype == SPY:
                                    score -= 300
            else:
                ttype = cell_type(tval)
                if ttype == FLAG:
                    score = 1000
                elif ttype == BOMB and own_type == MINER:
                    score = 500
                elif ttype == MARSHAL and own_type == SPY:
                    score = 400
                else:
                    rank_diff = PIECE_RANK.get(own_type, 0) - PIECE_RANK.get(ttype, 0)
                    if rank_diff > 0:
                        score = 100 + rank_diff
                    elif rank_diff == 0:
                        score = -50
                    else:
                        score = -200
            if score > best_overall_score:
                best_overall_score = score
                best_overall = (r, c, nr, nc)
    if best_overall:
        return best_overall
    return None


def ai_apply_move(game, move):
    r, c, nr, nc = move
    result, status = game.move(game.player2_id or 0, r, c, nr, nc)
    return result
