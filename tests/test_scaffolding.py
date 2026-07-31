from pathlib import Path
import pytest
from juno.scaffolding import scaffold_show,scaffold_sequence,scaffold_shot


# Set up a fixture for the environment variables
@pytest.fixture
def juno_env(tmp_path, monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", str(tmp_path))
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", str(Path(__file__).parent.parent))
    return tmp_path



# SHOW SCAFFOLDING TESTS
def test_scaffold_show_good_path(juno_env):

    scaffold_show("TEST","Test Show")

    assert(juno_env / "TEST").exists()
    assert(juno_env / "TEST" / "sequences").exists()
    assert(juno_env / "TEST" / "config" / "project.json").exists()


def test_scaffold_show_existing_show(juno_env):

    scaffold_show("TEST","Test Show")

    with pytest.raises(FileExistsError):
        scaffold_show("TEST","Test Show")


# SEQUENCE SCAFFOLDING TESTS
def test_scaffold_sequence_good_path(juno_env):

    scaffold_show("TEST","Test Show")
    scaffold_sequence("TEST", "A")

    assert(juno_env / "TEST" / "sequences" / "A").exists()


def test_scaffold_sequence_show_missing(juno_env):

    with pytest.raises(FileNotFoundError):
        scaffold_sequence("TEST", "A")


def test_scaffold_sequence_existing_sequence(juno_env):

    scaffold_show("TEST", "Test Show")
    scaffold_sequence("TEST", "A")

    with pytest.raises(FileExistsError):
        scaffold_sequence("TEST", "A")



# SHOT SCAFFOLDING TESTS
def test_scaffold_shot_good_path(juno_env):

    scaffold_show("TEST","Test Show")
    scaffold_sequence("TEST", "A")
    scaffold_shot("TEST","A","150")

    assert(juno_env / "TEST" / "sequences" / "A" / "150").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "config").exists()

    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "prv").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "prv" / "_work").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "prv" / "_publish").exists()

    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "lay").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "lay" / "_work").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "lay" / "_publish").exists()

    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "anm").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "anm" / "_work").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "anm" / "_publish").exists()

    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "cfx").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "cfx" / "_work").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "cfx" / "_publish").exists()

    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "fx").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "fx" / "_work").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "fx" / "_publish").exists()

    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "lgt").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "lgt" / "_work").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "lgt" / "_publish").exists()

    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "cmp").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "cmp" / "_work").exists()
    assert(juno_env / "TEST" / "sequences" / "A" / "150" / "cmp" / "_publish").exists()


def test_scaffold_shot_show_missing(juno_env):

    with pytest.raises(FileNotFoundError):
        scaffold_shot("TEST", "A", "150")


def test_scaffold_shot_sequence_missing(juno_env):

    scaffold_show("TEST","Test Show")

    with pytest.raises(FileNotFoundError):
        scaffold_shot("TEST", "A", "150")


def test_scaffold_shot_existing_shot(juno_env):

    scaffold_show("TEST","Test Show")
    scaffold_sequence("TEST", "A")
    scaffold_shot("TEST","A", "150")

    with pytest.raises(FileExistsError):
        scaffold_shot("TEST", "A", "150")