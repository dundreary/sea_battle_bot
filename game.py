import random

SIZE = 10
SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

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
        return all(ship.sunk for ship in self.ships)

    SHIP_SYMS = {EMPTY: "·", SHIP: "■", HIT: "✗", MISS: "○", SUNK: "✖", DEAD: "~"}

    def cell_display(self, r, c, hide_ships=False):
        v = self.grid[r][c]
        if v == EMPTY:
            return "·"
        if v == SHIP:
            return "·" if hide_ships else "■"
        if v == HIT:
            return "✗"
        if v == MISS:
            return "○"
        if v == SUNK:
            return "✖"
        if v == DEAD:
            return "~"
        return "·"

    def render(self, hide_ships=True):
        lines = []
        for i in range(SIZE):
            row = f"{i+1:2}" + "".join(self.cell_display(i, j, hide_ships) for j in range(SIZE))
            lines.append(row)
        return "\n".join(lines)

    def render_own(self):
        return self.render(hide_ships=False)

    @staticmethod
    def render_side_by_side(board1, board2, label1="МОИ", label2="БОТ", hide2=True):
        r1 = board1.render(hide_ships=False).split("\n")
        r2 = board2.render(hide_ships=hide2).split("\n")
        gap = "  "
        merged = [f"{label1:^12}{gap}{label2:^12}"]
        for i in range(SIZE):
            merged.append(f"{r1[i]}{gap}{r2[i]}")
        return "\n".join(merged)

class Game:
    def __init__(self, code, player1_id, player2_id=None, solo=False):
        self.code = code
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.solo = solo
        self.board1 = Board()
        self.board2 = Board()
        self.bot_ai = BotAI() if solo else None
        self.turn = 1
        self.phase = "placing1"
        self.placing = {
            1: {"ship_idx": 0, "cells": []},
            2: {"ship_idx": 0, "cells": []},
        }
        self.ready = {1: False, 2: False}

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
        if idx >= len(SHIPS):
            return None
        return SHIPS[idx]

    def generate_code():
        import string
        return "".join(random.choices(string.ascii_uppercase, k=6))

def validate_ship_placement(cells):
    if len(cells) < 2:
        return True, ""
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

def auto_place_ships(board):
    for length in SHIPS:
        placed = False
        attempts = 0
        while not placed and attempts < 1000:
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
            attempts += 1
        if not placed:
            board.grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
            board.ships = []
            auto_place_ships(board)
            return

class BotAI:
    def __init__(self):
        self.shots = set()
        self.hunt_queue = []
        self.ship_mode = False

    def reset_for_board(self, board):
        self.shots = set()
        self.hunt_queue = []
        self.ship_mode = False

    def choose_shot(self, enemy_board):
        try_hunt = list(self.hunt_queue)
        self.hunt_queue = []
        for r, c in try_hunt:
            if (r, c) not in self.shots and enemy_board.grid[r][c] in (EMPTY, SHIP):
                self.hunt_queue.append((r, c))
                self.ship_mode = True
            else:
                for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < SIZE and 0 <= nc < SIZE and (nr, nc) not in self.shots:
                        if enemy_board.grid[nr][nc] not in (HIT, MISS):
                            if (nr, nc) not in self.hunt_queue:
                                self.hunt_queue.append((nr, nc))

        while self.hunt_queue:
            r, c = self.hunt_queue.pop(0)
            if (r, c) not in self.shots and enemy_board.grid[r][c] not in (HIT, MISS):
                return r, c

        available = [(r, c) for r in range(SIZE) for c in range(SIZE)
                     if (r, c) not in self.shots and enemy_board.grid[r][c] not in (HIT, MISS)]
        if not available:
            return None
        return random.choice(available)

    def register_shot(self, r, c, result, enemy_board):
        self.shots.add((r, c))
        if result in ("hit", "sunk"):
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    if (nr, nc) not in self.shots and enemy_board.grid[nr][nc] not in (HIT, MISS):
                        if (nr, nc) not in self.hunt_queue:
                            self.hunt_queue.append((nr, nc))
            if result == "sunk":
                self.hunt_queue = [q for q in self.hunt_queue if enemy_board.grid[q[0]][q[1]] != SUNK]
