from juno.publish import next_version, publish, list_publishes, latest_publish, get_publish_metadata
import pytest
from pathlib import Path
from juno.paths import get_show_root


# NEXT_VERSION TESTING

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



# LIST_PUBLISHES TESTING

def test_list_publishes_good(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))

    publish_v001 = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish" / "v001")
    publish_v001.mkdir(parents=True)

    publish_v002 = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish" / "v002")
    publish_v002.mkdir(parents=True)

    results = list_publishes("TEST", "A", "010", "fx")
    assert results == ["v001","v002"]


def test_list_publishes_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))

    publish_v001 = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish")
    publish_v001.mkdir(parents=True)

    results = list_publishes("TEST", "A", "010", "fx")
    assert results == []


def test_list_publishes_directory_not_found():

    with pytest.raises(FileNotFoundError):
        list_publishes("TEST", "A", "010", "fx")




# LATEST_PUBLISH TESTING 

def test_latest_publish_good(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))

    publish_v001 = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish" / "v001")
    publish_v001.mkdir(parents=True)

    publish_v002 = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish" / "v002")
    publish_v002.mkdir(parents=True)

    results = latest_publish("TEST", "A", "010", "fx")
    assert results == "v002"


def test_latest_publish_no_versions(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))

    publish_v001 = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish")
    publish_v001.mkdir(parents=True)


    results = latest_publish("TEST", "A", "010", "fx")
    assert results == ""


def test_latest_publish_directory_not_found():

    with pytest.raises(FileNotFoundError):
        latest_publish("TEST", "A", "010", "fx")




# PUBLISH TESTING

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




# GET_PUBLISH_METADATA TESTING

def test_get_publish_metadata_good(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))

    work_directory = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_work")
    publish_directory = (get_show_root() / "TEST" / "sequences" / "A" / "010" / "fx" / "_publish")
    publish_directory.mkdir(parents=True)
    work_directory.mkdir(parents=True)

    source = (work_directory / "test_geo.usd")
    source.write_text("testing content")

    publish(source, "TEST", "A", "010", "fx", "testing_comment")

    result = get_publish_metadata("TEST","A","010","fx","v001")

    assert result["version"] == "v001"
    assert "timestamp" in result
    assert result["source"] == str(work_directory / "test_geo.usd")
    assert result["comment"] == "testing_comment"
    assert "user" in result
    