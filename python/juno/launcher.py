import os
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








