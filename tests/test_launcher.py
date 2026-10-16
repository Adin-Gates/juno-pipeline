import pytest
import os
from juno.launcher import build_maya_env, read_dependencies, build_pip_command, needs_install, MARKER_NAME
from pathlib import Path



def test_build_maya_env():

    base_env = {"HOME": "/fake/home"}

    result = build_maya_env("/fake/pipeline", "/fake/show", "/fake/deps", base_env)

    assert result["JUNO_PIPELINE_ROOT"] == "/fake/pipeline"
    assert result["JUNO_SHOW_ROOT"] == "/fake/show"
    assert result["PYTHONPATH"] == os.pathsep.join([str(Path("/fake/pipeline") / "python"), "/fake/deps"])

def test_build_maya_env_base_env():

    base_env = {"HOME": "/fake/home"}

    result = build_maya_env("/fake/pipeline", "/fake/show", "/fake/deps", base_env)

    assert result["HOME"] == "/fake/home"

def test_build_maya_env_existing_pythonpath():

    base_env = {"HOME": "/fake/home", "PYTHONPATH": "/fake/old"}

    result = build_maya_env("/fake/pipeline", "/fake/show", "/fake/deps", base_env)

    assert result["PYTHONPATH"] == os.pathsep.join([str(Path("/fake/pipeline") / "python"), "/fake/deps", "/fake/old"])







def test_read_dependencies(tmp_path):

    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\ndependencies = ["alpha", "beta"]\n')

    result = read_dependencies(pyproject)

    assert result == ["alpha", "beta"]

def test_read_dependencies_doesnt_exist(tmp_path):

    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\ntest = ["alpha", "beta"]\n')

    with pytest.raises(KeyError):
        read_dependencies(pyproject)

def test_read_dependencies_empty(tmp_path):

    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\ndependencies = []\n')

    with pytest.raises(ValueError):
        read_dependencies(pyproject)






def test_build_pip_command():

    result = build_pip_command("/usr/autodesk/maya2026/bin/mayapy", "/fake/deps_dir", ["jsonschema", "referencing"])

    assert result == ['/usr/autodesk/maya2026/bin/mayapy', '-m', 'pip', 'install', '--target', '/fake/deps_dir', 'jsonschema', 'referencing']








def test_needs_install_no_marker(tmp_path):

    result = needs_install(tmp_path, ["test1","test2"])

    assert result == True


def test_needs_install_works(tmp_path):

    marker = tmp_path / MARKER_NAME
    marker.write_text("test1\ntest2")

    result = needs_install(tmp_path, ["test1","test2"])

    assert result == False


def test_needs_install_marker_wrong(tmp_path):

    marker = tmp_path / MARKER_NAME
    marker.write_text("test1\ntest2")

    result = needs_install(tmp_path, ["test1","test2","test3"])

    assert result == True