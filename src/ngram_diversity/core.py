from collections import Counter
from typing import Sequence, List
import unicodedata

def tokenize(text: str, lowercase: bool = True) -> List[str]:
    if lowercase:
        text = text.lower()
    # 記号 
    punctuation = {'\n', '\r', '\t', '!', '"', '#', '$', '%', '&', "'", '(', ')', 
                   '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', 
                   '[', '\\', ']', '^', '_', '`', '{', '|', '}', '。', '、', '・', 
                   '「', '」', '『', '』', '【', '】','─', '…', '〜', 'ー'}

    # Unicode正規化
    text = unicodedata.normalize('NFKC', text)
    # 文字単位。空白は除く
    return [c for c in text if not c.isspace() and c.isprintable() and c not in punctuation]

def ngram_counts(tokens: Sequence[str], n: int) -> Counter:
    if n <= 0:
        raise ValueError("n must be >= 1")
    return Counter(tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1))

def diversity_ratio(tokens: Sequence[str], n: int) -> float:
    counts = ngram_counts(tokens, n)
    total = sum(counts.values())
    return (len(counts) / total) if total else 0.0
