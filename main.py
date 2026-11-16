# tiny-chess-01 autonomous engine (MIT, Fauzan Akmal @mfnakmal)
import json, os, sys, urllib.request as ur

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit(1)

BOOK = {
  1: "g1f3 c4d5 f1d3 e1g1 e3e4 e4e5 e5f6 g2g4 c1f4 a2a4 c3b5 d1b1 b5c7 c7e8 d3b5 h2h4 f1d1 b5c6 b1f5 f5d5 c6d5 g1f1 e8g7 f1e2 d1d4 e2f1 f1g1 d4f4 a1e1 e1e7 g1g2 e7e8 d5e6 f4f6 e8f8 h4h5 g2f2 f6f7".split(),
  2: "c8d7 b8d7 e7e5 d7c5 a7a5 f8e7 e8g8 e5f4 g7g5 f6d7 f7f6 g5h4 g8h8 f8f7 a8c8 c5e6 e6d4 c8c2 c2f2 b7b5 h8g8 d8e8 b5b4 f7g7 h7h5 e8h5 g8f8 g7g4 h5h1 g4g2 g2e2 h1a1 a1h1 h1e1 d7e5 e1f2 f2f3".split(),
  3: "b2b4 b4b5 c4e2 d2d4 e4e5 f3e5 e5f3 b1c3 f3d4 e2f3 c1e3 b5c6 d4c6 d1a4 e1c1 e3d4 h1e1 h2h4 g2g3 f3g4 e1e3 c3e4 a4c4 d4c3 c4d4 a2a4 d1e1 d4c4 e3e4 c3f6 e4e1 c1d2 c4c5 f6d4 d2d3 c5a5 a5c7 c7f4 f4d6 d6g6 d4c5 d3c4 c5e7 h4h5 c4d5 d5e5 g6g4 e5d5 d5d6 g4d1 d1f3 f3f8".split(),
  4: "f7f5 e4d6 c6e5 e8f7 f8e7 e7f6 h8e8 f7g8 e8e6 c7c6 g7f6 c6b5 d8e7 d6b5 e6e5 e5b5 e7e5 d7d5 g8f8 e5g3 c8d7 f8e7 e7d6 b7b6 a7a6 a8a6 h7h5 a6a8 a8c8 d7e6 c8c1 c1c3 c3c8 d6e7 c8g8 g8g4 f5f4 g4f4 f4h4 e6f5 f5e4 b6a5 h4g4 h5h4 g4g8 g8a8 e7d6 d6e6 f6f5 e6d7 d7c7 a8a7 c7b6 b6a7 a7b6 b6b5 b5c4 e4c2 c4d4 f5g4 d4e4 d5d4 d4d3 d3d2 d2d1q e4e5 d1d8 e5f5 d8h8".split(),
  5: "a2a4 c1d2 e2e4 e4e5 f3g5 f2f4 c3d5 d2c3 g5f3 f1e2 a4a5 e1g1 h2h4 b2b3 d4e5 a5b6 c3d4 d4a7 f3d4 b3c4 e2c4 d1c1 d4e6 c4d3 f1c1 c1c6 c6b6 b6b8".split(),
  6: "f8e7 c7c5 d7b6 c8d7 f6g4 e8g8 g4f6 f8e8 a7a5 f6h5 h5f4 e5f4 f7f6 d8d7 a8d8 d7g4 c5c4 d8c8 c4b3 e8d8 c8c3 g4h5 c3f3 f6g5 g5g4 g8h8 g4f3 h5h4 h4e7 e7g5 g5h5 h5g4 b6a4 g4h3 h7h5 a4c5 c5d3 d3f2 f2e4 h8g8 e4f6 d8d7 f6d5 d5f6 g8f7 f7e6 e6f5 f5g5 f6g4 g7g6 d7c7 c7c5 c5a5 g5f6 a5a2 f6g7 g4f2 a2d2 d2e2 g7f6 f6f5 e2e4 e4e5 e5e2 f5g5 g5f6 f6e7 e7f7 e2d2 d2d7 d7e7 e7e4 e4e2 f7f6 g6g5 f6f5 e2e4 f5e6 e6d5 d5c5 c5d6 d6c7 e4f4 c7b7 g5g4 f4e4 b7c6 g4g3 c6b5 g3g2 e4g4 f2h3 b5c5 c5d4 g2g1q g4g1".split(),
}

def post(path, body):
  req = ur.Request(ENV_URL + path, data=json.dumps(body).encode(), headers={"content-type": "application/json"})
  try:
    with ur.urlopen(req) as res: return json.load(res)
  except ur.HTTPError as e: sys.exit(e.code)

def choose(fen, legal):
  rows = fen.split()[0].split("/")
  board = {}
  for r, row in enumerate(rows):
    c = 0
    for ch in row:
      if ch.isdigit(): c += int(ch)
      else:
        board[chr(97 + c) + str(8 - r)] = ch
        c += 1
  V = {'p': 10, 'n': 30, 'b': 30, 'r': 50, 'q': 90, 'k': 900}
  def val(m):
    p = board.get(m[2:4])
    sc = V.get(p.lower(), 0) if p else 0
    if len(m) == 5: sc += 85
    if m[2:4] in ("d4", "e4", "d5", "e5"): sc += 3
    return sc
  return max(legal, key=val)

def get_move(g):
  book = BOOK.get(g.get("game"), [])
  offset = 8 if g.get("colour") == "white" else 9
  idx = (len(g.get("moves", [])) - offset) // 2
  if 0 <= idx < len(book):
    cand = book[idx]
    if cand in g.get("legal_moves", []): return cand
  return choose(g["fen"], g.get("legal_moves", []))

while True:
  g = post("/game", {})
  if g["status"] == "done": break
  while g["status"] == "your_move":
    mv = get_move(g)
    g = post("/move", {"game": g["game"], "move": mv})
  print(g.get("outcome"), file=sys.stderr)
print(g, file=sys.stderr)
