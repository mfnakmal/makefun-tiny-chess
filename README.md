# makefun-tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/mfnakmal/makefun-tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/mfnakmal/makefun-tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

Autonomous 4KB Python chess engine built for make.fun's [tiny-chess-01](https://make.fun/bounty/tiny-chess-01) bounty ($500 prize pool).

## Implementation
- Fits strictly within the 4,096 bytes constraint (`main.py`)
- Evaluates MVV-LVA (Most Valuable Victim - Least Valuable Attacker) tactical exchanges
- Applies center-square positional bonuses for pawn structure and piece development
- Fully deterministic search adhering to Python 3.13 standard library

## Run
```bash
python3 main.py
```

