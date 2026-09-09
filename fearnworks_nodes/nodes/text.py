"""Legacy-schema ComfyUI adapters.

The algorithms live in ``fearnworks_nodes.core``. Keeping this adapter thin makes
it straightforward to add a V3 ``comfy_api`` extension without duplicating logic.
"""

from ..core.text import rank_prompt_segments, text_statistics
from ..core.tokens import analyze_clip_tokens


class FWCountTokens:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "clip": ("CLIP",),
            "text": ("STRING", {"forceInput": True, "multiline": True}),
        }}

    RETURN_TYPES = ("INT", "STRING")
    RETURN_NAMES = ("token_count", "report")
    FUNCTION = "execute"
    CATEGORY = "Fearnworks/Text"

    def execute(self, clip, text):
        result = analyze_clip_tokens(clip, text)
        report = f"Total tokens: {result.total_tokens}\nContent tokens: {result.content_tokens}"
        return (result.total_tokens, report)


class FWTrimToTokenBudget:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "clip": ("CLIP",),
            "text": ("STRING", {"forceInput": True, "multiline": True}),
            "max_tokens": ("INT", {"default": 75, "min": 0, "max": 100000}),
        }}

    RETURN_TYPES = ("STRING", "STRING", "INT", "INT", "BOOLEAN")
    RETURN_NAMES = ("accepted_text", "overflow_text", "accepted_tokens", "overflow_tokens", "was_trimmed")
    FUNCTION = "execute"
    CATEGORY = "Fearnworks/Text"

    def execute(self, clip, text, max_tokens):
        parts = [p.strip() for p in text.split(",") if p.strip()]
        accepted, overflow = [], []
        used = 0
        for part in parts:
            count = analyze_clip_tokens(clip, part).total_tokens
            if used + count <= max_tokens:
                accepted.append(part)
                used += count
            else:
                overflow.append(part)
        accepted_text = ", ".join(accepted)
        overflow_text = ", ".join(overflow)
        overflow_tokens = analyze_clip_tokens(clip, overflow_text).total_tokens if overflow_text else 0
        return (accepted_text, overflow_text, used, overflow_tokens, bool(overflow))


class FWPromptSegmentRanker:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "clip": ("CLIP",),
            "text": ("STRING", {"forceInput": True, "multiline": True}),
        }}

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "Fearnworks/Text"

    def execute(self, clip, text):
        result = rank_prompt_segments(text, lambda value: analyze_clip_tokens(clip, value).total_tokens)
        segments = "\n".join(f"{count:4d} | {value}" for value, count in result["segments"])
        words = "\n".join(f"{count:4d} | {value}" for value, count in result["words"])
        return (f"Sorted Segments\n{segments}\n\nSorted Words\n{words}",)


class FWTextStatistics:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"text": ("STRING", {"forceInput": True, "multiline": True})}}

    RETURN_TYPES = ("STRING", "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("report", "characters", "words", "lines", "unique_characters")
    FUNCTION = "execute"
    CATEGORY = "Fearnworks/Text"

    def execute(self, text):
        stats = text_statistics(text)
        report = "\n".join(f"{key}: {value}" for key, value in stats.items())
        return (report, stats["characters"], stats["words"], stats["lines"], stats["unique_characters"])
