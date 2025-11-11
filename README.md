
# AVALANCHE DSL 0.1.5 (hotfix)

**Fix:** Grammatikfehler in `NFP` korrigiert (`op_fps=*(` → `op_fps=...`),
`RelGE`/`RelLE` wieder explizit als benannte Regeln eingeführt.

Weitere Stabilitätsmaßnahmen aus 0.1.4 bleiben erhalten (loop-safe Actor/Spatial,
`RelOp`-Priorisierung, `expect`-Expr etc.).

## Quickstart
pip install textX pytest
python tools/parse_model.py examples/demo.avalanche
pytest -q
