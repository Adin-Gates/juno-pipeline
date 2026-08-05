from juno.publish import next_version
import pytest
from pathlib import Path



def test_next_version_empty_dir(tmp_path):
    result = next_version(tmp_path)
    assert result == "v001"

def test_next_version_v004(tmp_path):

    (tmp_path / "v001").mkdir()
    (tmp_path / "v002").mkdir()
    (tmp_path / "v003").mkdir()
    
    result = next_version(tmp_path)
    assert result == "v004"


def test_next_version_v002(tmp_path):

    (tmp_path / "v001").mkdir()

    result = next_version(tmp_path)
    assert result == "v002"

def test_next_version_gap(tmp_path):

    (tmp_path / "v001").mkdir()
    (tmp_path / "v003").mkdir()
    
    result = next_version(tmp_path)
    assert result == "v004"
