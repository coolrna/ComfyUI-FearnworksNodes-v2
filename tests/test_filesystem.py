from pathlib import Path

from fearnworks_nodes.nodes.filesystem import FWFileCount


def test_file_count_missing_directory(tmp_path: Path):
    count, status, exists = FWFileCount().execute(str(tmp_path / "missing"), "*.png", False, False)
    assert count == 0
    assert exists is False
    assert "does not exist" in status


def test_file_count_patterns_and_case(tmp_path: Path):
    (tmp_path / "a.PNG").write_text("x")
    (tmp_path / "b.jpg").write_text("x")
    count, _, exists = FWFileCount().execute(str(tmp_path), "*.png,*.jpg", False, False)
    assert exists is True
    assert count == 2
