from pathlib import Path
from typing import Optional, Literal
import sys, json, typer
from .core import tokenize, ngram_counts, diversity_ratio

def _read_text(path: Optional[Path]) -> str:
    if path is None or str(path) == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")

def main(
    path: Optional[Path] = typer.Argument(
        None, help="Path to a text file. Use '-' or omit to read from stdin."
    ),
    n: int = typer.Option(2, min=1, help="Size of n-grams."),
    # by: Literal["word", "char"] = typer.Option("word", help="Tokenization strategy."),
    lower: bool = typer.Option(True, help="Lowercase before tokenization."),
    top: int = typer.Option(10, min=1, help="Show top-k n-grams."),
    to_json: bool = typer.Option(False, "--json", help="Output JSON."),
) -> None:
    text = _read_text(path)
    tokens = tokenize(text, 
                      # by=by,
                      lowercase=lower)
    counts = ngram_counts(tokens, n)
    ratio = diversity_ratio(tokens, n)

    if to_json:
        payload = {
            "n": n,
            # "tokenizer": by,
            "lowercase": lower,
            "total_ngrams": sum(counts.values()),
            "unique_ngrams": len(counts),
            "diversity": ratio,
            "top": [
                {"ngram": "".join(t), "count": c, "composition_ratio(%)": c / sum(counts.values()) * 100}
                # {"ngram": " ".join(t) if by == "word" else "".join(t), "count": c}
                for t, c in counts.most_common(top)
            ],
        }
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        # typer.echo(f"n={n} | tokenizer={by} | lower={lower}")
        typer.echo(f"n={n} | lower={lower}")
        typer.echo(f"diversity={ratio:.4f}  (unique {len(counts)} / total {sum(counts.values())})")
        typer.echo("top:")
        for t, c in counts.most_common(top):
            gram = "".join(t)
            # gram = " ".join(t) if by == "word" else "".join(t)
            typer.echo(f"  {gram}\t{c}")
            typer.echo(f"  composition_ratio(%): {c / sum(counts.values()):.4f*100}")

def _main() -> None:
    typer.run(main)

if __name__ == "__main__":
    _main()
