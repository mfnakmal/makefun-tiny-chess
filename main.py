# tiny-chess-01 autonomous engine (MIT, Fauzan Akmal @mfnakmal)
import json, os, sys, urllib.request as ur

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit(1)
VAL = {"p": 100, "n": 320, "b": 330, "r": 500, "q": 900, "k": 20000}
KD = (-21, -19, -12, -8, 8, 12, 19, 21)
SL = {"b": (-11, -9, 9, 11), "r": (-10, -1, 1, 10), "q": (-11, -10, -9, -1, 1, 9, 10, 11)}
CT = {'d4': 35, 'e4': 35, 'd5': 35, 'e5': 35, 'c4': 20, 'f4': 20, 'c5': 20, 'f5': 20, 'd3': 15, 'e3': 15, 'd6': 15, 'e6': 15, 'c3': 12, 'f3': 12, 'c6': 12, 'f6': 12}

def post(path, body):
  req = ur.Request(
    ENV_URL + path,
    data=json.dumps(body).encode(),
    headers={"content-type": "application/json"}
  )
  try:
    with ur.urlopen(req) as res:
      return json.load(res)
  except ur.HTTPError as e:
    sys.exit(e.code)

def sq_of(uci):
  return (8 - int(uci[1]) + 2) * 10 + (ord(uci[0]) - ord("a") + 1)

def parse_fen(fen):
  b = ["#"] * 120
  parts = fen.split()
  for r in range(8):
    for c in range(8):
      b[(r + 2) * 10 + (c + 1)] = " "
  for r, row in enumerate(parts[0].split("/")):
    c = 0
    for ch in row:
      if ch.isdigit():
        c += int(ch)
      else:
        b[(r + 2) * 10 + (c + 1)] = ch
        c += 1
  return b, parts[1] == "w"

def eval_pos(b, w):
  score = 0
  for sq in range(120):
    p = b[sq]
    if p in (" ", "#"):
      continue
    pw = p.isupper()
    pt = p.lower()
    if pt not in VAL:
      continue
    val = VAL[pt]
    r, f = (sq // 10) - 2, (sq % 10) - 1
    uci_sq = chr(ord("a") + f) + str(8 - r)
    val += CT.get(uci_sq, 0)
    if pt in ("n", "b") and ((pw and r < 7) or (not pw and r > 0)):
      val += 20
    if pt == "k" and ((pw and r == 7 and f in (1, 2, 6)) or (not pw and r == 0 and f in (1, 2, 6))):
      val += 40
    score += val if pw else -val
  return score if w else -score

def apply_move(b, move):
  nb = list(b)
  src, dst = sq_of(move[:2]), sq_of(move[2:4])
  p = nb[src]
  nb[src] = " "
  if p.upper() == "K" and abs(src - dst) == 2:
    rsrc = src + 3 if dst > src else src - 4
    rdst = src + 1 if dst > src else src - 1
    nb[rdst], nb[rsrc] = nb[rsrc], " "
  if len(move) == 5:
    p = move[4].upper() if p.isupper() else move[4].lower()
  if p.upper() == "P" and nb[dst] == " " and (src % 10 != dst % 10):
    nb[(src // 10) * 10 + (dst % 10)] = " "
  nb[dst] = p
  return nb

def opp_caps(b, w):
  opp_w, caps, pstep = not w, [], (-10 if not w else 10)
  for sq in range(120):
    p = b[sq]
    if p in (" ", "#") or p.isupper() != opp_w:
      continue
    pt = p.lower()
    if pt == "p":
      for d in (pstep - 1, pstep + 1):
        t = b[sq + d]
        if t not in (" ", "#") and t.isupper() == w:
          caps.append((sq, sq + d))
    elif pt == "n":
      for d in KD:
        t = b[sq + d]
        if t not in (" ", "#") and t.isupper() == w:
          caps.append((sq, sq + d))
    elif pt in SL:
      for d in SL[pt]:
        curr = sq + d
        while b[curr] != "#":
          if b[curr] != " ":
            if b[curr].isupper() == w:
              caps.append((sq, curr))
            break
          curr += d
  return caps

def choose(fen, legal_moves):
  b, w = parse_fen(fen)
  best_val, best_move = -999999, legal_moves[0]
  for m in legal_moves:
    nb = apply_move(b, m)
    score = eval_pos(nb, w)
    w_ref = 0
    for o_src, o_dst in opp_caps(nb, w):
      cap_val = VAL.get(nb[o_dst].lower(), 0)
      att_val = VAL.get(nb[o_src].lower(), 0)
      gain = cap_val - (att_val if cap_val > att_val else 0)
      if gain > w_ref:
        w_ref = gain
    net = score - w_ref
    if net > best_val or (net == best_val and m < best_move):
      best_val, best_move = net, m
  return best_move

while True:
  g = post("/game", {})
  if g["status"] == "done":
    break
  while g["status"] == "your_move":
    g = post("/move", {"game": g["game"], "move": choose(g["fen"], g["legal_moves"])})
  print(g.get("outcome"), file=sys.stderr)
print(g, file=sys.stderr)
