"""Legacy ComfyUI registration for broad compatibility."""

from .nodes.filesystem import FWFileCount
from .nodes.text import FWCountTokens, FWPromptSegmentRanker, FWTextStatistics, FWTrimToTokenBudget

NODE_CLASS_MAPPINGS = {
    "FW_CountTokens": FWCountTokens,
    "FW_TrimToTokenBudget": FWTrimToTokenBudget,
    "FW_PromptSegmentRanker": FWPromptSegmentRanker,
    "FW_TextStatistics": FWTextStatistics,
    "FW_FileCount": FWFileCount,
    # Compatibility aliases for the original Fearnworks node IDs.
    "CountTokens": FWCountTokens,
    "TrimToTokens": FWTrimToTokenBudget,
    "TokenCountRanker": FWPromptSegmentRanker,
    "FileCountInDirectory": FWFileCount,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FW_CountTokens": "🔍 FW Count Tokens",
    "FW_TrimToTokenBudget": "✂️ FW Trim To Token Budget",
    "FW_PromptSegmentRanker": "🔍 FW Prompt Segment Ranker",
    "FW_TextStatistics": "📊 FW Text Statistics",
    "FW_FileCount": "📁 FW File Count",
    "CountTokens": "🔍 FW Count Tokens",
    "TrimToTokens": "✂️ FW Trim To Token Budget",
    "TokenCountRanker": "🔍 FW Prompt Segment Ranker",
    "FileCountInDirectory": "📁 FW File Count",
}
