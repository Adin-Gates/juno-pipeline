import pytest
import os
import subprocess
from juno.maya_launcher import build_maya_env, read_dependencies, build_pip_command, needs_install, MARKER_NAME, ensure_maya_dependencies, launch_maya
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

def test_build_maya_env_empty_show_root():

    base_env = {"HOME": "/fake/home"}

    with pytest.raises(ValueError):
        build_maya_env("/fake/pipeline", "", "/fake/deps", base_env)






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








def test_launch_maya(tmp_path):

    pipeline_root = tmp_path / "pipeline_root"
    pipeline_root.mkdir()

    pyproject_path = pipeline_root / "pyproject.toml"
    pyproject_path.write_text('[project]\ndependencies = ["beta", "alpha"]\n')

    show_root = "/fake/show"

    maya_root = "/fake/maya"

    base_env = {"HOME": "/fake/home"}

    run_calls = []
    start_calls = []


    def fake_run(command, check=True):
        run_calls.append(command)

    def fake_start(command, env=None, **kwargs):
        start_calls.append((command, env, kwargs))


    deps_dir = pipeline_root / "vendor" / "maya-py311"


    result = launch_maya(maya_root, pipeline_root, show_root, base_env, run=fake_run, start=fake_start)

    assert len(run_calls) == 1
    assert run_calls[0][0] == str(Path("/fake/maya") / "bin" / "mayapy")

    assert len(start_calls) == 1
    command, env, kwargs = start_calls[0]

    assert command == [str(Path("/fake/maya") / "bin" / "maya")]
    assert env["HOME"] == "/fake/home"
    assert env["JUNO_SHOW_ROOT"] == "/fake/show"
    assert env["PYTHONPATH"] == os.pathsep.join([str(pipeline_root / "python"), str(deps_dir)])









def test_launch_maya_sequence(tmp_path):

    pipeline_root = tmp_path / "pipeline_root"
    pipeline_root.mkdir()

    pyproject_path = pipeline_root / "pyproject.toml"
    pyproject_path.write_text('[project]\ndependencies = ["beta", "alpha"]\n')

    show_root = "/fake/show"

    maya_root = "/fake/maya"

    base_env = {"HOME": "/fake/home"}

    events = []


    def fake_run(command, check=True):
        events.append("run")

    def fake_start(command, env=None, **kwargs):
        events.append("start")


    deps_dir = pipeline_root / "vendor" / "maya-py311"


    result = launch_maya(maya_root, pipeline_root, show_root, base_env, run=fake_run, start=fake_start)

    assert events[0] == "run"
    assert events[1] == "start"


