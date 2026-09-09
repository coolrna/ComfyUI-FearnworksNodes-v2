"""Tokenizer-independent helpers for ComfyUI CLIP-like objects."""

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class TokenAnalysis:
    """A normalized view of a tokenization result."""

    token_ids: tuple[Any, ...]
    total_tokens: int
    content_tokens: int
    special_tokens: int


def _first_sequence(value: Any) -> Sequence[Any]:
    if isinstance(value, (str, bytes)):
        return value
    if isinstance(value, Sequence):
        if not value:
            return ()
        first = value[0]
        if isinstance(first, Sequence) and not isinstance(first, (str, bytes)):
            return first
        return value
    return tuple(value) if isinstance(value, Iterable) else ()


def _extract_token_sequence(tokens: Mapping[str, Any]) -> Sequence[Any]:
    """Extract the first token sequence without assuming a 'g' encoder key."""
    for value in tokens.values():
        seq = _first_sequence(value)
        if seq:
            return seq
    return ()


def analyze_clip_tokens(clip: Any, text: str) -> TokenAnalysis:
    """Tokenize text and normalize the result across encoder layouts.

    Unlike the original implementation, this does not assume ``tokens['g'][0]``.
    A token value of zero is treated as padding when possible; all other values
    are retained. Special-token identification remains tokenizer-dependent and
    therefore defaults to zero when the CLIP object exposes no metadata.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if clip is None or not hasattr(clip, "tokenize"):
        raise TypeError("clip must provide a tokenize(text) method")

    tokens = clip.tokenize(text)
    if not isinstance(tokens, Mapping):
        raise TypeError("clip.tokenize() must return a mapping of token streams")

    sequence = tuple(_extract_token_sequence(tokens))
    content = tuple(token for token in sequence if token != 0)
    return TokenAnalysis(
        token_ids=content,
        total_tokens=len(content),
        content_tokens=len(content),
        special_tokens=0,
    )
