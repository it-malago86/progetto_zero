import tempfile
from pathlib import Path
from organizer import safe_move, find_category_by_extension, DEFAULT_RULES

def test_find_category():
    assert find_category_by_extension(".jpg", DEFAULT_RULES) == "images"
    assert find_category_by_extension(".unknownext", DEFAULT_RULES) is None

def test_safe_move_and_collision(tmp_path):
    src_dir = tmp_path / "src"
    tgt_dir = tmp_path / "tgt"
    src_dir.mkdir()
    tgt_dir.mkdir()
    # crea file di prova
    f1 = src_dir / "test.txt"
    f1.write_text("hello")
    # sposta
    dest = safe_move(f1, tgt_dir, dry_run=False)
    assert dest is not None
    assert dest.exists()
    # crea nuovo file con stesso nome e sposta -> collisione e rename
    f2 = src_dir / "test.txt"
    f2.write_text("hello2")
    dest2 = safe_move(f2, tgt_dir, dry_run=False)
    assert dest2 is not None and dest2 != dest
