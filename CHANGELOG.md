
# Changelog
## 0.1.5
- Fix: NFP-Grammatik (kein `=*` mehr), `RelGE`/`RelLE` reaktiviert.
- Add: Test, der die Grammatik an sich kompiliert.

## 0.1.4
- Fix: Endlosschleife in Parser (Actor-Block) durch leeres Match in Wiederholung.
- Cleanup: keine doppelten Quantifizierer (x+=Y* / x+=Y+).
- Stabil: Beibehaltung RelOp-Fix und vorheriger Hardening-Schritte.

## 0.1.3
- Relationale Operatoren: eigene Regel `RelOp` (>=, <= vor >, <).

## 0.1.2
- Aggregationsduplikate entfernt (Actor/Spatial).
- ExpectSpec für 'expect <Expr>'.
- Choice-Block mit Semikolon; Option ohne.
