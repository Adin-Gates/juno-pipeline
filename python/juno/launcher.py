import os
import tomllib
import subprocess
import sys
import argparse
from pathlib import Path
from juno.utils import green_text, red_text


def build_maya_env(pipeline_root, show_root, deps_dir, base_env):

    if not show_root:
        raise ValueError("build_maya_env: show_root is 'None' or otherwise not valid")

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



def ensure_maya_dependencies(mayapy, deps_dir, pyproject_path, run=subprocess.run):

    dependencies_list = read_dependencies(pyproject_path)

    if not needs_install(deps_dir, dependencies_list):
        return False

    Path(deps_dir).mkdir(parents=True, exist_ok=True)

    command = build_pip_command(mayapy, deps_dir, dependencies_list)

    run(command, check=True)

    marker_path = Path(deps_dir) / MARKER_NAME

    marker_content = "\n".join(sorted(dependencies_list))

    marker_path.write_text(marker_content)

    return True

    
    
def launch_maya(maya_root, pipeline_root, show_root, base_env, run=subprocess.run, start=subprocess.Popen):


    mayapy = Path(maya_root) / "bin" / "mayapy"
    maya_program = Path(maya_root) / "bin" / "maya"

    deps_dir = Path(pipeline_root) / "vendor" / "maya-py311"
    pyproject_path = Path(pipeline_root) / "pyproject.toml"

    ensure_maya_dependencies(mayapy, deps_dir, pyproject_path, run=run)

    env = build_maya_env(pipeline_root,show_root,deps_dir,base_env)

    return start([str(maya_program)], env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)








if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--maya-root", default="/usr/autodesk/maya2026")
    parser.add_argument("--pipeline-root", default=Path(__file__).parent.parent.parent)
    parser.add_argument("--show-root", default=os.environ.get("JUNO_SHOW_ROOT"))

    args = parser.parse_args()   

    print("")
    print(f"Launching {green_text('Juno Maya')} Instance...")
    print("")
    print(f"Given Maya root -> {args.maya_root}")
    print(f"Given Juno Pipeline root -> {args.pipeline_root}")
    print(f"Given Show root -> {args.show_root}")

    launch_maya(args.maya_root, args.pipeline_root, args.show_root, dict(os.environ))

    print("")
    print(f"Starting {green_text('Juno Maya')} Instance...")

    
    









