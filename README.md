# Brain Reps (Math + DSA)

This repo is your **artifact trail** for:
- **Math for AI** notes + exercises
- **DSA practice** in **Python** (and optionally Java)
- Tests + clean rewrites for every DSA problem

## Daily workflow (recommended)
1. **Math (60 min)**  
   - Notes in `math/` (one file per day)
2. **DSA (60 min)**  
   - Implement in `dsa/python/solutions/`  
   - Add tests in `dsa/python/tests/`  
   - Do a **clean rewrite** after you pass tests

## Folder structure
- `math/` — math notes & worked examples
- `dsa/python/solutions/` — Python solutions
- `dsa/python/tests/` — Python tests (pytest)
- `dsa/java/` — optional Java implementations
- `templates/` — reusable templates

## Conventions
**Commit message format**
- `math: day-XX <topic>`
- `dsa(py): day-XX <problem>`
- `dsa(java): day-XX <problem>`
- `chore: ...`

**File naming**
- Math: `math/day-01.md`
- DSA Python: `dsa/python/solutions/day-01_two_sum.py`
- DSA Python tests: `dsa/python/tests/test_day_01_two_sum.py`

## Python testing
Install:
```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -U pip pytest
```

Run:
```bash
pytest -q
```

---

Start date: 2026-01-28
