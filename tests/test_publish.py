from juno.publish import next_version, publish
import pytest
from pathlib import Path
from juno.paths import get_show_root


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


def test_publish_good(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))

    work_directory = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_work")
    publish_directory = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish")
    publish_directory.mkdir(parents=True)
    work_directory.mkdir(parents=True)

    source = (work_directory / "test_geo.usd")
    source.write_text("testing content")

    publish(source, "TEST", "A", "010", "fx", "testing_comment")

    assert (tmp_path / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish" / "v001" / "test_geo.usd").exists()
    assert (tmp_path / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish" / "v001" / "metadata.json").exists()


def test_publish_good_v003(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))

    work_directory = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_work")
    publish_directory_v001 = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish" / "v001")
    publish_directory_v002 = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish" / "v002")
    publish_directory_v001.mkdir(parents=True)
    publish_directory_v002.mkdir(parents=True)
    work_directory.mkdir(parents=True)

    source = (work_directory / "test_geo.usd")
    source.write_text("testing content")

    publish(source, "TEST", "A", "010", "fx", "testing_comment")

    assert (tmp_path / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish" / "v003" / "test_geo.usd").exists()
    assert (tmp_path / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish" / "v003" / "metadata.json").exists()


def test_publish_source_not_found(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))

    source = "test"

    with pytest.raises(FileNotFoundError):
        publish(source, "BOBO", "A", "010", "cfx", "comment")


def test_publish_override_permission_file(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))

    work_directory = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_work")
    publish_directory = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish")
    publish_directory.mkdir(parents=True)
    work_directory.mkdir(parents=True)

    source = (work_directory / "test_geo.usd")
    source.write_text("testing content")

    published_file = publish(source, "TEST", "A", "010", "fx", "testing_comment")

    with pytest.raises(PermissionError):
        published_file.write_text("trying to overwrite")


def test_publish_override_permission_metadata(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))

    work_directory = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_work")
    publish_directory = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish")
    publish_directory.mkdir(parents=True)
    work_directory.mkdir(parents=True)

    source = (work_directory / "test_geo.usd")
    source.write_text("testing content")

    published_file = publish(source, "TEST", "A", "010", "fx", "testing_comment")

    with pytest.raises(PermissionError):
        (published_file.parent / "metadata.json").write_text("trying to overwrite")