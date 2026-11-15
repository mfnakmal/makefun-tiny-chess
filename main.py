# tiny-chess-01 autonomous engine (MIT, Fauzan Akmal @mfnakmal)
# Deterministic positional & tactical engine in < 4,096 bytes of Python 3.13
# Optimized with MVV-LVA capture scoring and center-weight positional bonuses.
import json
import os
import sys
import urllib.error
import urllib.request

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")

# Centipawn piece values
VAL = {"p": 100, "n": 320, "b": 330, "r": 500, "q": 900, "k": 20000}

# Square center weights for positional play
CENTER = {
    "d4": 30, "e4": 30, "d5": 30, "e5": 30,
    "c4": 15, "f4": 15, "c5": 15, "f5": 15,
    "d3": 10, "e3": 10, "d6": 10, "e6": 10,
    "c3": 10, "f3": 10, "c6": 10, "f6": 10
}

def post(path, body):
    """POST a JSON body to the env and return its JSON answer."""
    req = urllib.request.Request(
        ENV_URL + path,
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")

def board_of(fen):
    """Parse FEN into a square->piece map."""
    board = {}
    for i, row in enumerate(fen.split()[0].split("/")):
        file = 0
        for c in row:
            if c.isdigit():
                file += int(c)
            else:
                board["abcdefgh"[file] + str(8 - i)] = c
                file += 1
    return board

def choose(fen, legal):
    """Pick best move using MVV-LVA, promotions, and positional center control."""
    board = board_of(fen)
    turn = "w" if " w " in fen else "b"

    def score(move):
        src, dst = move[:2], move[2:4]
        mover = board.get(src, "p").lower()
        victim = board.get(dst)
        
        # En passant check
        if victim is None and mover == "p" and src[0] != dst[0]:
            victim = "p"

        # MVV-LVA capture value
        capture_score = (VAL.get(victim.lower(), 0) * 10 - VAL.get(mover, 0)) if victim else 0
        
        # Promotion bonus
        promo_bonus = 0
        if len(move) == 5:
            promo_char = move[4].lower()
            promo_bonus = VAL.get(promo_char, 0) * 5

        # Center control positional bonus
        pos_bonus = CENTER.get(dst, 0)
        # Advance pawns and minor pieces toward center
        if mover in ("n", "b") and src[1] in ("1", "8"):
            pos_bonus += 20

        # Discourage moving king in early game
        if mover == "k" and not victim:
            pos_bonus -= 40

        total = capture_score + promo_bonus + pos_bonus
        # Deterministic tie break on move string
        return (-total, move)

    return min(legal, key=score)

while True:
    g = post("/game", {})
    if g["status"] == "done":
        break
    while g["status"] == "your_move":
        best_move = choose(g["fen"], g["legal_moves"])
        g = post("/move", {"game": g["game"], "move": best_move})
    print(f"game {g['game']}: {g['outcome']} by {g['reason']}", file=sys.stderr)

print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost", file=sys.stderr)
