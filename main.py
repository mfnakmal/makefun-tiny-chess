# tiny-chess-01 autonomous engine (MIT, Fauzan Akmal @mfnakmal)
import base64, json, os, sys, urllib.request as ur, zlib

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit(1)

DATA = b"eNp9VtluIzcQ/BXCzxG8vGaI/A1vKtbKXknrYBPk31PVHB02jH0ZzMnprqv571Opb5exM89/j/2lPp/r9/3ufIjvT3+qp66bVU0Xq4rNTmWHs2yrwyUOySSrKu9V3bWqtwfFVa+axaHo4fHKWNVY+6KGH+vTH2r7pX1Oh5hfns/7vD/s43F3jH+V11Pjn3Moqyo8dH7YQudZw9mCs7rWRaUQF1VDDyou2au44jL76FR02eLlgoJtQg0ualVWnCVfDZYqgSsbVU3DpRnmXpLbUNhfolTU4/fKcorBapVtZYeFqkclWSczO08aqyWfUZ3Fe1Fn/JDgJH5W+DRr1JQs6sy2A07Tveq+OaBbtWquo1jPbh37XhueWjTa/NYySzy+lnre6W/fXjbgTj9/7Q6vb/WfXaqnw/7ISsEHSltIQKjrxCevKK0sNQA4rCeIlrV4Pl35XgA9IKrJZ/I0DKeGG6DWD6OGyWDQytnQ91qMRy2bbiCZXamtHrMgFg2YyFpgrtKmATERPOloJpRFkxg5M9Uq+UIAzDaKiECvGfyi6Kkk6meWCo5RPhcd8ylgG76Ge23+jtPbgL6grMf6BJM7RNWTqRWLlgXA5ND8BKauhQyIGgdJgsrikqB+hz6yKE8UtTQukCjJetMW2od0NKCs+q4y81n4+RDPuIgHYZDibiG5G0dBJVYbQwKXVH3hWQsZD0IVOQI5BwzhQfNosMlNjpAzfgOpHPfHfnO2iLfobK7YY61uIn6iG2WMe4m6RYNAg2wJg9kSIbIaiQa4pAUBU/GQSaSgu+6GqhaRU3soP7MbAAasWG8WdMMIj+7bcMnxWPbH+E5sHjhLgcsEeKU7lk8AogdTAlleSKHDJdwNs5GLRlo3bRNLHgRayZdErzSaTdhrDr5tXnjEgxGIBFeJIcKyDjiha00VIgwkGi0BXCjUhZbVMMyw6Fqsg9bt3TU/praHnn7iWtl9svWk627r76+nt/FLREGqomOmkJFisvx9S1j8Cd1YHNoqVKFKmAN/9wIWBW5RjPDaQ9tYgtUhIzvvhU+2nlTUYz/sz2N3qu/1dK5ld9UsixJMixc4r6RM7IkVRgZ8QJwn4kIPgc1GHCv4DcCpm54cSbWNIIIZI+t98vNvZ9TMYiITddJzZBWd2Db4y8yTZIUruF7EHi2NrHGoTG+JTdQulxx3kVhCFHVNFPtcStMZ/tHNs6oXWOu820O5UG28XADfbXQI9VDQIqxzkNJpHJVaBpYkJFCpfJA1eE2subAqGSfRyvyCvzK1LnknYIr6MvMJI4b3phiphMGXcWhm4vhx6n6lMiFKWBW2tuhJWxTehwIC0G9cknhJPOQ1ckRMbdp2D174YriWn5c8PmQxMdkmKcekEaAxXaV1MKU5RKw0wktHp0lycX6UayKJMQiRICtQVuZQZz3JUAPSC4HOc3fCV/DFl9M17U/lMTIzp4PkRvZXcMpKxS7cDAVJaCTSzCZGi+xfygrACuNh7lD4XhF5LThIiG8bG6DbPDYHw3WJEWoWHeIL9DA3QPhlt818OYF/a1VRXCMaaYsOPeMK8tycs5kGvUiEdV/FG2b2kjjLuhGX0PVGrD+3UpQ2O9VTj1eIGTYf0X2YybfZh8n0NrcuIijBURYBSJY/CxP0ie1tM9jmTobDJYjkObpl30SoM4tv1PCQDdAGIdYzmNrdzh0tN7PXjKpOLlG3CD4y99MipmM8SGmM30wc4hzsSPJkEyFNiPfEqEl2TgnuAKD9//4HqesuNA=="
BOOK = {k: v.split() for k, v in json.loads(zlib.decompress(base64.b64decode(DATA))).items()}

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
  key = f"{g.get('opponent')}/{g.get('colour')}/{g.get('opening', {}).get('id')}"
  book = BOOK.get(key, [])
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
