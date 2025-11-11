
#!/usr/bin/env python3
import argparse
from pathlib import Path
from textx import metamodel_from_file, TextXError

def main():
    ap = argparse.ArgumentParser(description="Parse AVALANCHE DSL model")
    ap.add_argument("model", type=str, help="Path to .avalanche model")
    ap.add_argument("--grammar", type=str, default="avalanche.tx")
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()

    grammar_path = Path(args.grammar).resolve()
    model_path = Path(args.model).resolve()

    try:
        mm = metamodel_from_file(str(grammar_path), ignore_case=False, autokwd=True, memoization=True, debug=args.debug)
        model = mm.model_from_file(str(model_path))
    except TextXError as e:
        print("Parse/MetaModel error:\n", e)
        raise SystemExit(1)

    print("Parsed:", model_path.name)
    counters = {}
    for el in getattr(model, 'elements', []):
        t = type(el).__name__
        counters[t] = counters.get(t, 0) + 1

    print("Summary:")
    for k in sorted(counters):
        print(f"  {k:15s} : {counters[k]}")

    print("\nModel OK.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
