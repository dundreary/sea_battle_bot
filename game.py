import random
import string
import time

SIZE = 10
SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
STRIP_SHIPS = [4, 4, 3, 3, 2, 2, 1, 1]

EMPTY = 0
SHIP = 1
HIT = 2
MISS = 3
SUNK = 4
DEAD = 5

class Ship:
    def __init__(self, cells):
        self.cells = list(cells)
        self.hits = set()

    @property
    def sunk(self):
        return len(self.hits) >= len(self.cells)

    def is_at(self, r, c):
        return (r, c) in self.cells

    def to_dict(self):
        return {
            'cells': [list(c) for c in self.cells],
            'hits': [list(h) for h in self.hits],
        }

    @staticmethod
    def from_dict(data):
        ship = Ship([tuple(c) for c in data['cells']])
        ship.hits = set(tuple(h) for h in data['hits'])
        return ship

class Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
        self.ships = []
        self.placement_mode = True

    def can_place(self, cells):
        for r, c in cells:
            if not (0 <= r < SIZE and 0 <= c < SIZE):
                return False
            if self.grid[r][c] != EMPTY:
                return False
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < SIZE and 0 <= nc < SIZE:
                        if self.grid[nr][nc] == SHIP:
                            return False
        return True

    def place_ship(self, cells):
        ship = Ship(cells)
        for r, c in cells:
            self.grid[r][c] = SHIP
        self.ships.append(ship)

    def _mark_dead_zone(self, ship):
        for sr, sc in ship.cells:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = sr + dr, sc + dc
                    if 0 <= nr < SIZE and 0 <= nc < SIZE:
                        if self.grid[nr][nc] == EMPTY:
                            self.grid[nr][nc] = DEAD

    def receive_shot(self, r, c):
        if self.grid[r][c] == SHIP:
            self.grid[r][c] = HIT
            for ship in self.ships:
                if ship.is_at(r, c):
                    ship.hits.add((r, c))
                    if ship.sunk:
                        for sr, sc in ship.cells:
                            self.grid[sr][sc] = SUNK
                        self._mark_dead_zone(ship)
                        return "sunk"
            return "hit"
        elif self.grid[r][c] == EMPTY:
            self.grid[r][c] = MISS
            return "miss"
        return "repeat"

    def all_sunk(self):
        if not self.ships:
            return False
        return all(ship.sunk for ship in self.ships)

    def cell_display(self, r, c, hide_ships=False):
        v = self.grid[r][c]
        if v == EMPTY:
            return "⬜"
        if v == SHIP:
            return "⬜" if hide_ships else "🟩"
        if v == HIT:
            return "❌"
        if v == MISS:
            return "·"
        if v == SUNK:
            return "✖"
        if v == DEAD:
            return "·"
        return "⬜"

    def render(self, hide_ships=True):
        return "\n".join(
            "".join(self.cell_display(i, j, hide_ships) for j in range(SIZE))
            for i in range(SIZE)
        )

    def to_flat_list(self, hide_ships=False):
        if hide_ships:
            return [EMPTY if v == SHIP else v for row in self.grid for v in row]
        return [v for row in self.grid for v in row]

    def to_dict(self):
        return {
            'grid': self.grid,
            'ships': [s.to_dict() for s in self.ships],
            'placement_mode': self.placement_mode,
        }

    @staticmethod
    def from_dict(data):
        board = Board()
        board.grid = data['grid']
        board.ships = [Ship.from_dict(s) for s in data['ships']]
        board.placement_mode = data.get('placement_mode', True)
        return board

class Game:
    def __init__(self, code, player1_id, player2_id=None, solo=False, strip=False, difficulty=2):
        self.code = code
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.solo = solo
        self.strip = strip
        self.difficulty = difficulty
        self.board1 = Board()
        self.board2 = Board()
        self.bot_ai = BotAI(difficulty=difficulty) if solo else None
        self.turn = 1
        self.phase = "placing1"
        self.placing = {
            1: {"ship_idx": 0, "cells": []},
            2: {"ship_idx": 0, "cells": []},
        }
        self.ready = {1: False, 2: False}
        self.strip_photo = ""
        self.created_at = time.time()

    @property
    def both_placed(self):
        return self.phase == "playing"

    def player_num(self, user_id):
        return 1 if user_id == self.player1_id else 2

    def switch_turn(self):
        self.turn = 3 - self.turn

    def current_player(self):
        return self.player1_id if self.turn == 1 else self.player2_id

    def opponent_id(self, player_id):
        return self.player2_id if player_id == self.player1_id else self.player1_id

    def board_for(self, player_id):
        return self.board1 if player_id == self.player1_id else self.board2

    def opponent_board(self, player_id):
        return self.board2 if player_id == self.player1_id else self.board1

    def needs_ship_of_length(self, pnum=None):
        if pnum is None:
            pnum = self.player_num(self.current_player())
        idx = self.placing[pnum]["ship_idx"]
        ships_list = STRIP_SHIPS if self.strip else SHIPS
        if idx >= len(ships_list):
            return None
        return ships_list[idx]

    @staticmethod
    def generate_code():
        return "".join(random.choices(string.ascii_uppercase, k=6))

    def to_dict(self):
        return {
            'code': self.code,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'solo': self.solo,
            'strip': self.strip,
            'difficulty': self.difficulty,
            'strip_photo': self.strip_photo,
            'created_at': self.created_at,
            'board1': self.board1.to_dict(),
            'board2': self.board2.to_dict(),
            'turn': self.turn,
            'phase': self.phase,
            'placing': {
                str(k): {
                    'ship_idx': v['ship_idx'],
                    'cells': [list(c) for c in v['cells']],
                }
                for k, v in self.placing.items()
            },
            'ready': {str(k): v for k, v in self.ready.items()},
            'bot_ai': self.bot_ai.to_dict() if self.bot_ai else None,
        }

    @staticmethod
    def from_dict(data):
        game = Game.__new__(Game)
        game.code = data['code']
        game.player1_id = data['player1_id']
        game.player2_id = data.get('player2_id')
        game.solo = data.get('solo', False)
        game.strip = data.get('strip', False)
        game.difficulty = data.get('difficulty', 2)
        game.strip_photo = data.get('strip_photo', "")
        game.created_at = data.get('created_at', 0)
        game.board1 = Board.from_dict(data['board1'])
        game.board2 = Board.from_dict(data['board2'])
        game.turn = data['turn']
        game.phase = data['phase']
        game.placing = {
            int(k): {
                'ship_idx': v['ship_idx'],
                'cells': [tuple(c) for c in v.get('cells', [])],
            }
            for k, v in data.get('placing', {}).items()
        }
        game.ready = {int(k): v for k, v in data.get('ready', {}).items()}
        if data.get('bot_ai'):
            game.bot_ai = BotAI.from_dict(data['bot_ai'])
        elif game.solo:
            game.bot_ai = BotAI(difficulty=game.difficulty)
        else:
            game.bot_ai = None
        if game.solo and game.player2_id is None:
            game.player2_id = 0
        return game

def validate_ship_placement(cells, strip=False):
    if len(cells) < 2:
        return True, ""
    if strip:
        # In strip mode, allow any connected shape
        cell_set = set(cells)
        start = cells[0]
        visited = set()
        stack = [start]
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in cell_set and (nr, nc) not in visited:
                    stack.append((nr, nc))
        if len(visited) == len(cell_set):
            return True, ""
        return False, "Корабль должен быть связным (все клетки соединены)."
    sorted_cells = sorted(cells)
    rows = sorted([r for r, c in cells])
    cols = sorted([c for r, c in cells])
    if rows[0] == rows[-1]:
        expected = sorted([(rows[0], c) for c in range(cols[0], cols[-1] + 1)])
        if sorted_cells != expected:
            return False, "Корабль должен быть прямой линией (все клетки подряд по горизонтали)."
        return True, ""
    if cols[0] == cols[-1]:
        expected = sorted([(r, cols[0]) for r in range(rows[0], rows[-1] + 1)])
        if sorted_cells != expected:
            return False, "Корабль должен быть прямой линией (все клетки подряд по вертикали)."
        return True, ""
    return False, "Корабль должен быть прямой линией (горизонтально или вертикально)."

CLOTHING_SHAPES = {
    4: [
        [(0,0), (0,1), (1,0), (1,1)],  # 2x2 square
        [(0,1), (0,2), (1,0), (1,1)],  # shifted square (S-shape)
    ],
    3: [
        [(0,0), (1,0), (1,1)],  # L-shape (angle)
        [(0,0), (0,1), (0,2)],  # straight stick
    ],
    2: [
        [(0,0), (0,1)],  # horizontal pair
    ],
    1: [
        [(0,0)],  # single cell
    ],
}

def auto_place_strip_ships(board: Board) -> None:
    while True:
        board.grid = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
        board.ships = []
        for length in STRIP_SHIPS:
            placed = False
            for _ in range(1000):
                shapes = CLOTHING_SHAPES.get(length, [[(0, i) for i in range(length)]])
                shape = random.choice(shapes)
                r = random.randint(0, SIZE - 1)
                c = random.randint(0, SIZE - 1)
                cells = [(r + dr, c + dc) for dr, dc in shape]
                if all(0 <= cr < SIZE and 0 <= cc < SIZE for cr, cc in cells):
                    if board.can_place(cells):
                        board.place_ship(cells)
                        placed = True
                        break
            if not placed:
                break
        else:
            return


def auto_place_ships(board: Board) -> None:
    while True:
        board.grid = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
        board.ships = []
        for length in SHIPS:
            placed = False
            for _ in range(1000):
                is_horizontal = random.choice([True, False])
                if is_horizontal:
                    r = random.randint(0, SIZE - 1)
                    c = random.randint(0, SIZE - length)
                    cells = [(r, c + i) for i in range(length)]
                else:
                    r = random.randint(0, SIZE - length)
                    c = random.randint(0, SIZE - 1)
                    cells = [(r + i, c) for i in range(length)]
                if board.can_place(cells):
                    board.place_ship(cells)
                    placed = True
                    break
            if not placed:
                break
        else:
            return

class BotAI:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.shots = set()
        self.hunt_queue = []
        self.ship_mode = False

    def reset_for_board(self, board):
        self.shots = set()
        self.hunt_queue = []
        self.ship_mode = False

    def _probability_shot(self, enemy_board, strip=False):
        ships_list = STRIP_SHIPS if strip else SHIPS
        if strip:
            return None
        probs = [[0.0 for _ in range(SIZE)] for _ in range(SIZE)]
        for length in ships_list:
            for r in range(SIZE):
                for c in range(SIZE - length + 1):
                    cells = [(r, c + i) for i in range(length)]
                    if all(enemy_board.grid[nr][nc] in (EMPTY, SHIP) for nr, nc in cells):
                        for nr, nc in cells:
                            probs[nr][nc] += 1.0
            for r in range(SIZE - length + 1):
                for c in range(SIZE):
                    cells = [(r + i, c) for i in range(length)]
                    if all(enemy_board.grid[nr][nc] in (EMPTY, SHIP) for nr, nc in cells):
                        for nr, nc in cells:
                            probs[nr][nc] += 1.0
        best = -1.0
        best_cell = None
        for r in range(SIZE):
            for c in range(SIZE):
                if (r, c) not in self.shots and enemy_board.grid[r][c] in (EMPTY, SHIP):
                    if probs[r][c] > best:
                        best = probs[r][c]
                        best_cell = (r, c)
        return best_cell

    def choose_shot(self, enemy_board, strip=False):
        if self.difficulty >= 3 and not self.hunt_queue:
            result = self._probability_shot(enemy_board, strip=strip)
            if result:
                return result

        validated = []
        for r, c in self.hunt_queue:
            if enemy_board.grid[r][c] in (EMPTY, SHIP):
                validated.append((r, c))
            else:
                for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < SIZE and 0 <= nc < SIZE and (nr, nc) not in self.shots:
                        if enemy_board.grid[nr][nc] not in (HIT, MISS, SUNK, DEAD):
                            if (nr, nc) not in validated:
                                validated.append((nr, nc))
        self.hunt_queue = validated

        while self.hunt_queue:
            r, c = self.hunt_queue.pop(0)
            if enemy_board.grid[r][c] in (EMPTY, SHIP):
                return r, c

        available = [(r, c) for r in range(SIZE) for c in range(SIZE)
                     if (r, c) not in self.shots and enemy_board.grid[r][c] not in (HIT, MISS, SUNK, DEAD)]
        if not available:
            return None
        return random.choice(available)

    def register_shot(self, r, c, result, enemy_board):
        self.shots.add((r, c))
        if result in ("hit", "sunk"):
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    if (nr, nc) not in self.shots and enemy_board.grid[nr][nc] not in (HIT, MISS, SUNK, DEAD):
                        if (nr, nc) not in self.hunt_queue:
                            self.hunt_queue.append((nr, nc))
            if result == "sunk":
                self.hunt_queue = [q for q in self.hunt_queue if enemy_board.grid[q[0]][q[1]] not in (SUNK, DEAD)]

    def to_dict(self):
        return {
            'shots': [list(s) for s in self.shots],
            'hunt_queue': [list(q) for q in self.hunt_queue],
            'ship_mode': self.ship_mode,
            'difficulty': self.difficulty,
        }

    @staticmethod
    def from_dict(data):
        ai = BotAI(difficulty=data.get('difficulty', 2))
        ai.shots = set(tuple(s) for s in data['shots'])
        ai.hunt_queue = [tuple(q) for q in data['hunt_queue']]
        ai.ship_mode = data['ship_mode']
        return ai
