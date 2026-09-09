from fearnworks_nodes.core.text import rank_prompt_segments, text_statistics
from fearnworks_nodes.core.tokens import analyze_clip_tokens


class MockClip:
    def tokenize(self, text):
        # Deliberately use a non-'g' key to prove the analyzer does not depend
        # on the archived implementation's hard-coded encoder layout.
        return {"tokens": [[49406, *range(1, len(text.split()) + 1), 49407, 0, 0]]}


def test_token_analysis_does_not_require_g_key():
    result = analyze_clip_tokens(MockClip(), "one two three")
    assert result.total_tokens == 5
    assert result.token_ids[0] == 49406


def test_rank_segments_and_words():
    result = rank_prompt_segments("long phrase, short")
    assert result["segments"][0][0] == "long phrase"
    assert result["segments"][0][1] == 0  # supplied counter is deterministic


def test_unicode_text_statistics():
    stats = text_statistics("你好 world\nsecond")
    assert stats["characters"] == 15
    assert stats["words"] == 2
    assert stats["lines"] == 2
    assert stats["unique_characters"] <= stats["characters"]
