import os
import tomllib
from pathlib import Path


def build_maya_env(pipeline_root, show_root, deps_dir, base_env):

    maya_env = dict(base_env)

    maya_env["JUNO_PIPELINE_ROOT"] = str(pipeline_root)
    maya_env["JUNO_SHOW_ROOT"] = str(show_root)

    entries = [
        str(Path(pipeline_root) / "python"),
        str(deps_dir),
    ]

    base_pythonpath = base_env.get("PYTHONPATH")

    if base_pythonpath:
        entries.append(base_pythonpath)

    maya_env["PYTHONPATH"] = os.pathsep.join(entries)

    return maya_env


def read_dependencies(pyproject_path):

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    dependencies_list = data["project"]["dependencies"]

    if not dependencies_list:
        raise ValueError("No dependencies found on pyproject.toml")

    else:
        return dependencies_list



def build_pip_command(mayapy, deps_dir, dependencies):

    install_string_list = [str(mayapy),"-m","pip","install","--target",str(deps_dir)]

    for package in dependencies:
        install_string_list.append(package)

    return install_string_list


MARKER_NAME = ".juno-deps"


# needs_install returns True if the dependencies need to be installed and False if they do not.
def needs_install(deps_dir, dependencies):

    marker_path = Path(deps_dir) / MARKER_NAME

    if not marker_path.exists():
        return True

    marker_content = marker_path.read_text()

    expected_content = "\n".join(sorted(dependencies))

    return marker_content != expected_content



def ensure_maya_dependencies







if __name__ == "__main__":
    print(needs_install("/fake/deps_dir",["test1","test2"]))








