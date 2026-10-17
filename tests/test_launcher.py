import pytest
import os
import subprocess
from juno.launcher import build_maya_env, read_dependencies, build_pip_command, needs_install, MARKER_NAME, ensure_maya_dependencies
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




def test_ensure_maya_dependencies_fresh_install(tmp_path):

    calls = []

    def fake_run(command, check=False):
        calls.append(command)

    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text('[project]\ndependencies = ["beta", "alpha"]\n')

    deps_dir = tmp_path / "deps"

    mayapy = "/usr/autodesk/maya2026/bin/mayapy"

    result = ensure_maya_dependencies(mayapy, deps_dir, pyproject_path, run=fake_run)

    assert result == True

    assert calls == [[mayapy, "-m", "pip", "install", "--target", str(deps_dir), "beta", "alpha"]]

    assert (deps_dir / MARKER_NAME).read_text() == "alpha\nbeta"


def test_ensure_maya_dependencies_already_installed(tmp_path):

    calls = []

    def fake_run(command, check=False):
        calls.append(command)

    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text('[project]\ndependencies = ["beta", "alpha"]\n')

    deps_dir = tmp_path / "deps"
    deps_dir.mkdir()

    mayapy = "/usr/autodesk/maya2026/bin/mayapy"

    marker = deps_dir / MARKER_NAME
    marker.write_text("alpha\nbeta")

    result = ensure_maya_dependencies(mayapy, deps_dir, pyproject_path, run=fake_run)

    assert result == False
    assert calls == []


def test_ensure_maya_dependencies_mismatched_installed(tmp_path):

    calls = []

    def fake_run(command, check=False):
        calls.append(command)

    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text('[project]\ndependencies = ["beta", "alpha"]\n')

    deps_dir = tmp_path / "deps"
    deps_dir.mkdir()

    mayapy = "/usr/autodesk/maya2026/bin/mayapy"

    marker = deps_dir / MARKER_NAME
    marker.write_text("alpha")

    result = ensure_maya_dependencies(mayapy, deps_dir, pyproject_path, run=fake_run)

    assert result == True

    assert calls == [[mayapy, "-m", "pip", "install", "--target", str(deps_dir), "beta", "alpha"]]

    assert (deps_dir / MARKER_NAME).read_text() == "alpha\nbeta"


def test_ensure_maya_dependencies_pip_fails(tmp_path):

    calls = []

    def fake_run(command, check=False):
        if check:
            raise subprocess.CalledProcessError(1, command)

    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text('[project]\ndependencies = ["beta", "alpha"]\n')

    deps_dir = tmp_path / "deps"
    deps_dir.mkdir()

    mayapy = "/usr/autodesk/maya2026/bin/mayapy"

    marker = deps_dir / MARKER_NAME


    with pytest.raises(subprocess.CalledProcessError):
        ensure_maya_dependencies(mayapy, deps_dir, pyproject_path, run=fake_run)

    assert not (marker.exists())
