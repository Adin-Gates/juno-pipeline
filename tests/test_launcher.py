from juno.launcher import build_maya_env
import pytest
import os
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
