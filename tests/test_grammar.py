
from pathlib import Path
from textx import metamodel_from_file

def test_grammar_compiles():
    root = Path(__file__).resolve().parents[1]
    mm = metamodel_from_file(str(root/'avalanche.tx'), ignore_case=False, autokwd=True, memoization=True)
    assert mm is not None
