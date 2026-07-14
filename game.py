import random

from base_game import BaseGame

SIZE = 10
SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
STRIP_SHIPS = [4, 4, 3, 3, 2, 2, 1]

EMPTY = 0
SHIP = 1
HIT = 2
MISS = 3
SUNK = 4
DEAD = 5
MINE = 6
MINE_HIT = 7

# Specific ship shapes for strip mode, in placement order:
STRIP_SHIP_SHAPES = [
    [(0,0), (0,1), (1,0), (1,1)],  # 4-deck square
    [(0,1), (0,2), (1,0), (1,1)],  # 4-deck shifted square
    [(0,0), (1,0), (1,1)],          # 3-deck L-shape
    [(0,0), (0,1), (0,2)],          # 3-deck straight
    [(0,0), (0,1)],                 # 2-deck straight
    [(0,0), (1,1)],                 # 2-deck diagonal
    [(0,0)],                        # 1-deck single
]

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
        self.mines = []

    def _neighbors_occupied(self, r, c):
        """True if any cell in the 3x3 area around (r, c) holds a ship or mine."""
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    if self.grid[nr][nc] in (SHIP, MINE):
                        return True
        return False

    def _fill_dead_zone(self, r, c):
        """Mark every empty cell in the 3x3 area around (r, c) as a dead zone."""
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    if self.grid[nr][nc] == EMPTY:
                        self.grid[nr][nc] = DEAD

    def can_place(self, cells):
        for r, c in cells:
            if not (0 <= r < SIZE and 0 <= c < SIZE):
                return False
            if self.grid[r][c] != EMPTY:
                return False
            if self._neighbors_occupied(r, c):
                return False
        return True

    def place_ship(self, cells):
        ship = Ship(cells)
        for r, c in cells:
            self.grid[r][c] = SHIP
        self.ships.append(ship)

    def place_mine(self, r, c):
        if self.grid[r][c] != EMPTY:
            return False
        if self._neighbors_occupied(r, c):
            return False
        self.grid[r][c] = MINE
        self.mines.append((r, c))
        return True

    def _mark_dead_zone(self, ship):
        for sr, sc in ship.cells:
            self._fill_dead_zone(sr, sc)

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
        elif self.grid[r][c] == MINE:
            # Keep the cell visually distinct from a normal hit so the shooter
            # can see they struck a mine instead of a ship.
            self.grid[r][c] = MINE_HIT
            self._fill_dead_zone(r, c)
            return "mine"
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
        if v == MINE:
            return "⬜" if hide_ships else "💣"
        if v == MINE_HIT:
            return "💣"
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
            return [EMPTY if v in (SHIP, MINE) else v for row in self.grid for v in row]
        return [v for row in self.grid for v in row]

    def to_dict(self):
        return {
            'grid': self.grid,
            'ships': [s.to_dict() for s in self.ships],
            'mines': [list(m) for m in self.mines],
        }

    @staticmethod
    def from_dict(data):
        board = Board()
        board.grid = data['grid']
        board.ships = [Ship.from_dict(s) for s in data['ships']]
        board.mines = [tuple(m) for m in data.get('mines', [])]
        return board

class Game(BaseGame):
    def __init__(self, code, player1_id, player2_id=None, solo=False, strip=False, difficulty=2):
        super().__init__(code, player1_id, player2_id, solo, difficulty)
        self.strip = strip
        self.board1 = Board()
        self.board2 = Board()
        self.bot_ai = BotAI(difficulty=difficulty) if solo else None
        self.turn = 1
        self.phase = "placing1"
        self.ready = {1: False, 2: False}
        # Rematch opt-in after a finished game. Both participants must agree
        # before the same game (same code) restarts for another round.
        self.rematch = {1: False, 2: False}
        # Per-player "stake" photo, committed before the game starts
        # (both participants must upload one to confirm placement).
        self.strip_stakes = {1: "", 2: ""}

    def switch_turn(self):
        self.turn = 3 - self.turn

    def current_player(self):
        return self.player1_id if self.turn == 1 else self.player2_id

    def board_for(self, player_id):
        return self.board1 if player_id == self.player1_id else self.board2

    def opponent_board(self, player_id):
        return self.board2 if player_id == self.player1_id else self.board1

    def request_rematch(self, uid):
        """Opt in to a rematch on the same code.

        Returns True if the game has restarted (both players agreed, or a solo
        game which restarts immediately), False if this player's vote was
        recorded but the opponent has not yet agreed, and None if a rematch
        cannot be requested in the current state.
        """
        if self.phase != "finished":
            return None
        if self.solo:
            self.reset_for_rematch()
            return True
        pnum = self.player_num(uid)
        if pnum not in (1, 2):
            return None
        self.rematch[pnum] = True
        if self.rematch[1] and self.rematch[2]:
            self.reset_for_rematch()
            return True
        return False

    def reset_for_rematch(self):
        """Restart the same game (same code) for another round.

        Boards, turn, readiness and rematch votes are cleared. Player ids,
        strip mode, difficulty and code are preserved so participants continue
        without re-entering the code. Strip stakes are cleared so each round
        commits a fresh photo (the previous one may already be revealed).
        """
        self.board1 = Board()
        self.board2 = Board()
        self.turn = 1
        self.phase = "placing"
        self.ready = {1: False, 2: False}
        self.rematch = {1: False, 2: False}
        if self.strip:
            self.strip_stakes = {1: "", 2: ""}
        if self.solo:
            if self.strip:
                auto_place_strip_ships(self.board2)
            else:
                auto_place_ships(self.board2)
            self.ready[2] = True

    def trigger_mine_explosion(self, shooter_uid):
        board = self.board_for(shooter_uid)
        viable = [ship for ship in board.ships if len(ship.hits) < len(ship.cells)]
        if not viable:
            return None
        ship = random.choice(viable)
        unhit = [cell for cell in ship.cells if cell not in ship.hits]
        if not unhit:
            return None
        target = random.choice(unhit)
        board.receive_shot(target[0], target[1])
        return {"r": target[0], "c": target[1]}

    def to_dict(self):
        return {
            'code': self.code,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'solo': self.solo,
            'strip': self.strip,
            'difficulty': self.difficulty,
            'strip_stakes': {str(k): v for k, v in self.strip_stakes.items()},
            'created_at': self.created_at,
            'board1': self.board1.to_dict(),
            'board2': self.board2.to_dict(),
            'turn': self.turn,
            'phase': self.phase,
            'ready': {str(k): v for k, v in self.ready.items()},
            'rematch': {str(k): v for k, v in self.rematch.items()},
            'bot_ai': self.bot_ai.to_dict() if self.bot_ai else None,
        }

    @staticmethod
    def from_dict(data):
        game = Game.__new__(Game)
        game._from_dict_common(data)
        game.strip = data.get('strip', False)
        game.strip_stakes = {int(k): v for k, v in data.get('strip_stakes', {1: "", 2: ""}).items()}
        game.board1 = Board.from_dict(data['board1'])
        game.board2 = Board.from_dict(data['board2'])
        game.turn = data['turn']
        game.phase = data['phase']
        game.ready = {int(k): v for k, v in data.get('ready', {}).items()}
        game.rematch = {int(k): v for k, v in data.get('rematch', {1: False, 2: False}).items()}
        if data.get('bot_ai'):
            game.bot_ai = BotAI.from_dict(data['bot_ai'])
        elif game.solo:
            game.bot_ai = BotAI(difficulty=game.difficulty)
        else:
            game.bot_ai = None
        if game.solo and game.player2_id is None:
            game.player2_id = 0
        return game


def auto_place_strip_ships(board: Board) -> None:
    for _ in range(100):
        board.grid = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
        board.ships = []
        board.mines = []
        for shape in STRIP_SHIP_SHAPES:
            placed = False
            for _ in range(1000):
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
            for _ in range(1000):
                r = random.randint(0, SIZE - 1)
                c = random.randint(0, SIZE - 1)
                if board.place_mine(r, c):
                    return
            return
    raise RuntimeError("auto_place_strip_ships: failed to place all ships after 100 attempts")


def auto_place_ships(board: Board) -> None:
    for _ in range(100):
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
    raise RuntimeError("auto_place_ships: failed to place all ships after 100 attempts")

# Cells a ship is still allowed to occupy when enumerating placements.
# HIT is included: a known hit must belong to a remaining ship, so valid
# placements are required to cover it (this is what makes the density
# concentrate on a found ship instead of spreading randomly).
_BOT_OPEN = (EMPTY, SHIP, MINE, HIT)
# Cells that provably cannot hold a ship.
_BOT_BLOCKED = (MISS, SUNK, DEAD)


class BotAI:
    """Difficulty-aware Sea Battle opponent.

    All tiers share one strong engine - a probability-density solver over the
    *remaining* ships that accounts for known hits, sunk ships and mines, fully
    exploits the "ships never touch" rule (see ``_compute_blocked``) and locks
    onto a found ship to finish it quickly.  The difficulty knob is a single
    "skill" probability ``_P_OPT``: on each shot the bot plays that optimal
    move with probability ``p``; otherwise it plays a weaker (random) move.
    This produces a smooth, monotonic ladder with Expert at full strength and
    each lower tier a controlled ~step weaker:

      4 Expert - p = 1.00, always the optimal density move (strongest).
      3 Hard   - p = 0.45.
      2 Medium - p = 0.20.
      1 Easy   - p = 0.05, still competent but clearly the easiest.

    The exact ``p`` values are calibrated (see the benchmark) so the average
    shots-to-clear form an evenly spaced ladder: roughly 54.6 / 57.5 / 61.1 /
    64.4 shots for Expert / Hard / Medium / Easy - about +3 shots (~one player
    turn's edge) per step down, i.e. the "100 / 90 / 80 / 70" gradation.
    """

    # Probability of playing the optimal move at each difficulty (1..4).
    # Calibrated in the accompanying benchmark for an even, monotonic ladder.
    _P_OPT = {1: 0.05, 2: 0.20, 3: 0.45, 4: 1.00}

    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.shots = set()
        self.hunt_queue = []
        self.ship_mode = False
        self._strip = False
        self._blocked = frozenset()

    def reset_for_board(self, board):
        self.shots = set()
        self.hunt_queue = []
        self.ship_mode = False
        self._strip = False
        self._blocked = frozenset()

    # -- Easy ---------------------------------------------------------------
    def _random_shot(self, enemy_board):
        available = [
            (r, c) for r in range(SIZE) for c in range(SIZE)
            if self._open_unshot(enemy_board, r, c)
        ]
        return random.choice(available) if available else None

    # -- Medium -------------------------------------------------------------
    def _neighbours(self, r, c):
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                yield nr, nc

    def _compute_blocked(self, enemy_board, strip):
        """Cells that provably cannot hold a ship, from the game's rules.

        Two deductions, both exploiting that ships never touch (a 3x3 clearance
        is enforced around every ship and mine at placement time):

        * Mines: the whole 3x3 neighbourhood of a *discovered* mine (MINE_HIT)
          is ship-free.
        * Non-adjacency (normal mode only): any cell diagonally adjacent to a
          HIT is water.  A hit belongs to a straight ship, whose own cells are
          orthogonally contiguous, and no *other* ship may touch it even
          diagonally - so a diagonal neighbour of a hit can never be a ship.
          This is NOT valid in strip mode, where a single ship may itself have
          diagonally-placed cells (e.g. the diagonal 2-decker).
        """
        blocked = set()
        grid = enemy_board.grid
        for r in range(SIZE):
            for c in range(SIZE):
                v = grid[r][c]
                if v == MINE_HIT:
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                                blocked.add((nr, nc))
                elif v == HIT and not strip:
                    for dr, dc in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < SIZE and 0 <= nc < SIZE:
                            blocked.add((nr, nc))
        return blocked

    def _open_unshot(self, enemy_board, r, c):
        if (r, c) in self.shots or not (0 <= r < SIZE and 0 <= c < SIZE):
            return False
        if enemy_board.grid[r][c] not in _BOT_OPEN:
            return False
        # Cells provably water from the "ships never touch" rule (mines +
        # diagonal-of-hit); precomputed once per shot in ``_blocked``.
        if (r, c) in self._blocked:
            return False
        return True

    def _target_shot(self, enemy_board):
        """Orientation-aware hunting for the Medium tier.

        Once a ship is found (one or more HIT cells) we no longer spray the
        four orthogonal neighbours blindly.  Adjacent hits are grouped into
        clusters; when a cluster is a straight line we only fire at its two
        open ends, which finishes a damaged ship in far fewer shots than naive
        neighbour hunting and avoids wasting shots perpendicular to the ship.
        """
        active = [
            (r, c) for r in range(SIZE) for c in range(SIZE)
            if enemy_board.grid[r][c] == HIT
        ]
        if not active:
            return self._random_shot(enemy_board)

        # Group HIT cells into orthogonally-connected clusters.
        active_set = set(active)
        clusters = []
        seen = set()
        for cell in active:
            if cell in seen:
                continue
            stack = [cell]
            cluster = []
            while stack:
                cur = stack.pop()
                if cur in seen:
                    continue
                seen.add(cur)
                cluster.append(cur)
                for n in self._neighbours(*cur):
                    if n in active_set and n not in seen:
                        stack.append(n)
            clusters.append(cluster)

        candidates = []
        for cl in clusters:
            if len(cl) == 1:
                r, c = cl[0]
                for n in self._neighbours(r, c):
                    if self._open_unshot(enemy_board, *n):
                        candidates.append(n)
                continue
            rows = {r for r, _ in cl}
            cols = {c for _, c in cl}
            if len(rows) == 1:
                r = next(iter(rows))
                cs = sorted(c for _, c in cl)
                for end in (cs[0] - 1, cs[-1] + 1):
                    if self._open_unshot(enemy_board, r, end):
                        candidates.append((r, end))
            elif len(cols) == 1:
                c = next(iter(cols))
                rs = sorted(r for r, _ in cl)
                for end in (rs[0] - 1, rs[-1] + 1):
                    if self._open_unshot(enemy_board, end, c):
                        candidates.append((end, c))
            else:
                # Non-collinear cluster (e.g. an L-shaped hit pattern): try
                # every open orthogonal neighbour of every hit in the cluster.
                for cell in cl:
                    for n in self._neighbours(*cell):
                        if self._open_unshot(enemy_board, *n) and n not in candidates:
                            candidates.append(n)

        if candidates:
            return random.choice(candidates)
        return self._random_shot(enemy_board)

    # -- Hard / Expert: probability density ---------------------------------
    def _remaining_ship_lengths(self, enemy_board):
        if enemy_board.ships:
            return [len(s.cells) for s in enemy_board.ships if not s.sunk]
        return list(SHIPS)

    def _remaining_ship_shapes(self, enemy_board):
        if enemy_board.ships:
            return [list(s.cells) for s in enemy_board.ships if not s.sunk]
        return [list(s) for s in STRIP_SHIP_SHAPES]

    def _mine_blocked(self, enemy_board):
        """Deprecated: superseded by ``_compute_blocked``.  Kept as a thin
        wrapper so any external caller/tests keep working."""
        return self._compute_blocked(enemy_board, False)

    def _ship_placement_lists(self, enemy_board, strip):
        """One entry per remaining ship; each entry lists every legal placement
        (a list of cells) for that ship on the current board."""
        blocked = self._blocked

        def open_ok(r, c):
            return enemy_board.grid[r][c] in _BOT_OPEN and (r, c) not in blocked

        if strip:
            lists = []
            for shape in self._remaining_ship_shapes(enemy_board):
                minr = min(r for r, _ in shape)
                maxr = max(r for r, _ in shape)
                minc = min(c for _, c in shape)
                maxc = max(c for _, c in shape)
                pls = []
                for r0 in range(-minr, SIZE - maxr):
                    for c0 in range(-minc, SIZE - maxc):
                        cells = [(r + r0, c + c0) for r, c in shape]
                        if all(open_ok(r, c) for r, c in cells):
                            pls.append(cells)
                lists.append(pls)
            return lists
        lists = []
        for length in self._remaining_ship_lengths(enemy_board):
            pls = []
            for r in range(SIZE):
                for c in range(SIZE - length + 1):
                    cells = [(r, c + i) for i in range(length)]
                    if all(open_ok(nr, nc) for nr, nc in cells):
                        pls.append(cells)
            for r in range(SIZE - length + 1):
                for c in range(SIZE):
                    cells = [(r + i, c) for i in range(length)]
                    if all(open_ok(nr, nc) for nr, nc in cells):
                        pls.append(cells)
            lists.append(pls)
        return lists

    def _density(self, enemy_board, strip, focus_hits=None):
        """Probability that each open cell belongs to *some* remaining ship.

        We combine the per-ship placement counts with the independence
        approximation ``1 - prod(1 - p_ship(cell))``.  Unlike a naive sum of
        placement counts this correctly accounts for the fact that several
        remaining ships compete for the same space, so it concentrates fire on
        the cells that are genuinely most likely to hide a ship.

        When ``focus_hits`` is given we condition on the event that a ship runs
        through one of those cells, which makes the bot finish a found ship
        before spreading out again.
        """
        ships = self._ship_placement_lists(enemy_board, strip)
        survive = [[1.0] * SIZE for _ in range(SIZE)]
        for pls in ships:
            total = 0
            cnt = [[0] * SIZE for _ in range(SIZE)]
            for pl in pls:
                if focus_hits is not None and not any(cell in focus_hits for cell in pl):
                    continue
                total += 1
                for r, c in pl:
                    if (r, c) not in self.shots:
                        cnt[r][c] += 1
            if total == 0:
                continue
            for r in range(SIZE):
                for c in range(SIZE):
                    if self._open_unshot(enemy_board, r, c):
                        survive[r][c] *= (1.0 - cnt[r][c] / total)
        density = [[0.0] * SIZE for _ in range(SIZE)]
        for r in range(SIZE):
            for c in range(SIZE):
                if self._open_unshot(enemy_board, r, c):
                    density[r][c] = 1.0 - survive[r][c]
        return density

    def _best_in(self, density):
        best = -1.0
        for r in range(SIZE):
            for c in range(SIZE):
                if density[r][c] > best:
                    best = density[r][c]
        if best <= 0.0:
            return None
        # Among equally-likely cells, break ties smartly instead of always
        # taking the top-left one: prefer central cells (they touch more
        # placements on later shots) and then a fixed checkerboard parity.
        eps = 1e-9
        center = (SIZE - 1) / 2.0
        best_cell, best_key = None, None
        for r in range(SIZE):
            for c in range(SIZE):
                if density[r][c] >= best - eps:
                    key = (abs(r - center) + abs(c - center), (r + c) % 2)
                    if best_key is None or key < best_key:
                        best_key, best_cell = key, (r, c)
        return best_cell

    def _smart_shot(self, enemy_board, strip):
        active_hits = {
            (r, c) for r in range(SIZE) for c in range(SIZE)
            if enemy_board.grid[r][c] == HIT
        }
        # Lock onto a found ship (focus on known hits) so the bot finishes
        # damaged ships as fast as possible instead of probing elsewhere.
        focus = active_hits if active_hits else None
        density = self._density(enemy_board, strip, focus_hits=focus)
        best = self._best_in(density)
        if best is not None:
            return best
        return self._target_shot(enemy_board)

    def _weak_shot(self, enemy_board):
        """A deliberately sub-optimal move used to weaken the lower tiers.

        We fall back to a pure random open shot.  This costs the bot the
        density solver's efficient search (and, occasionally, an in-progress
        hunt), which is exactly what makes an easier tier easier - while the
        optimal branch keeps every tier looking competent most of the time.
        """
        return self._random_shot(enemy_board)

    def choose_shot(self, enemy_board, strip=False):
        # Precompute, once per shot, the cells provably water from the rules so
        # every helper (search, hunt and the density solver) shares them.
        self._strip = strip
        self._blocked = self._compute_blocked(enemy_board, strip)
        # Single skill knob: play the optimal density move with probability p,
        # otherwise a weaker random move.  Expert (p = 1.0) is always optimal.
        p = self._P_OPT.get(self.difficulty, 1.0)
        if p >= 1.0 or random.random() < p:
            return self._smart_shot(enemy_board, strip)
        return self._weak_shot(enemy_board)

    def register_shot(self, r, c, result, enemy_board):
        self.shots.add((r, c))
        if result in ("hit", "sunk", "mine"):
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    if (nr, nc) not in self.shots and enemy_board.grid[nr][nc] in _BOT_OPEN:
                        if (nr, nc) not in self.hunt_queue:
                            self.hunt_queue.append((nr, nc))
            if result == "sunk":
                self.hunt_queue = [
                    q for q in self.hunt_queue
                    if enemy_board.grid[q[0]][q[1]] not in (SUNK, DEAD)
                ]

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
