
from pathlib import Path
from textx import metamodel_from_file

def test_parse_demo():
    root = Path(__file__).resolve().parents[1]
    mm = metamodel_from_file(str(root/'avalanche.tx'), ignore_case=False, autokwd=True, memoization=True)
    model = mm.model_from_file(str(root/'examples'/'demo.avalanche'))
    assert model is not None
