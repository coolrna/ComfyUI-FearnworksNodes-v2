"""Pure text utilities used by the ComfyUI adapters."""

import re
from collections import Counter
from typing import Any, Callable, Dict, List, Sequence, Tuple


def _segments(text: str, separator: str = ",") -> List[str]:
    return [part.strip() for part in text.split(separator) if part.strip()]


def rank_prompt_segments(
    text: str,
    token_counter: Callable[[str], int],
    separator: str = ",",
) -> Dict[str, Any]:
    """Rank comma-separated prompt segments and their words by token count."""
    segments = _segments(text, separator)
    ranked_segments = sorted(
        ((segment, token_counter(segment)) for segment in segments),
        key=lambda item: (-item[1], item[0].lower()),
    )

    words = re.findall(r"\S+", text)
    ranked_words = sorted(
        ((word, token_counter(word)) for word in words),
        key=lambda item: (-item[1], item[0].lower()),
    )
    return {"segments": ranked_segments, "words": ranked_words}


def text_statistics(text: str) -> Dict[str, Any]:
    """Return useful deterministic statistics for arbitrary Unicode text."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    words = re.findall(r"\S+", text, flags=re.UNICODE)
    non_whitespace = [char for char in text if not char.isspace()]
    counts = Counter(text)
    return {
        "characters": len(text),
        "characters_no_whitespace": len(non_whitespace),
        "words": len(words),
        "lines": text.count("\n") + 1 if text else 0,
        "paragraphs": len([p for p in text.split("\n\n") if p.strip()]),
        "unique_characters": len(counts),
    }
