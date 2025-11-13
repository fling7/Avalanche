
from pathlib import Path

from textx import metamodel_from_file

from tools.build_new_speech import build_new_speech_grammar

def test_grammar_compiles():
    root = Path(__file__).resolve().parents[1]
    mm = metamodel_from_file(str(root/'avalanche.tx'), ignore_case=False, autokwd=True, memoization=True)
    assert mm is not None


def test_new_speech_compiles(tmp_path):
    root = Path(__file__).resolve().parents[1]
    grammar_path = build_new_speech_grammar(root)
    assert grammar_path.exists()
    mm = metamodel_from_file(str(grammar_path), ignore_case=False, autokwd=True, memoization=True)
    assert mm is not None
