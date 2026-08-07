import json
from pathlib import Path
from juno.paths import resolve_template, get_pipeline_root, get_show_root
from juno.config import shot_resolver


# scaffold_show : Takes a show_code and title. Creates a new show_code directory in the show directory if the show_code directory doesn't already exist. Creates project.json.
def scaffold_show(show_code, title):

    pipeline_root_dir = get_pipeline_root()

    show_code_dir = resolve_template("show_code_dir",show_code=show_code)

    sequences_dir = resolve_template("sequences_dir",show_code=show_code)

    project_config_file = resolve_template("project_config_file",show_code=show_code)

    project_config_dir = project_config_file.parent

    assets_dir = resolve_template("assets_dir",show_code=show_code)

    schema_path = Path(pipeline_root_dir) / "config" / "schema" / "project.schema.json"

    project_data = {
        "$schema": str(schema_path),
        "show": {"code": show_code, "title": title},
        "pipeline_version": "0.1.0"
    }

    if show_code_dir.exists():
        raise FileExistsError ("Show already exists. Cancelling show scaffolding.")

    if show_code.strip() == "":
        raise ValueError ("Show code is empty.")

    # Creates the show_code directory at the show root
    show_code_dir.mkdir(parents=True,exist_ok=True)

    # Creates the sequences directory
    sequences_dir.mkdir(parents=True,exist_ok=True)

    # Creates the project config directory and file
    project_config_dir.mkdir(parents=True,exist_ok=True)

    # Creates the assets directory
    assets_dir.mkdir(parents=True,exist_ok=True)

    # Write project details in new project.json
    with open(project_config_file, "w") as f:
        json.dump(project_data, f, indent=4)





# scaffold_sequence: Creates a new sequence_code directory in the show_code sequences directory. Doesn't create if it already exists or if show_code directory doesn't exist.
def scaffold_sequence(show_code, sequence_code):

    show_code_dir = resolve_template("show_code_dir",show_code=show_code)

    sequence_code_dir = resolve_template("sequence_code_dir",show_code=show_code, sequence_code=sequence_code)

    if sequence_code.strip() == "":
        raise ValueError ("Sequence code is empty.")

    if not show_code_dir.exists() or show_code.strip() == "":
        raise FileNotFoundError ("Show doesn't exists. Cancelling sequence scaffolding.")

    if sequence_code_dir.exists():
        raise FileExistsError ("Sequence already exists. Cancelling sequence scaffolding.")

    # Creates sequence directory in sequences directory
    sequence_code_dir.mkdir(parents=True,exist_ok=True)






# scaffold_shot : Creates a new shot_code directory in the given show_code / sequences / sequence_code directory. Creates config directory and department directories.
def scaffold_shot(show_code, sequence_code, shot_code):

    show_code_dir = resolve_template("show_code_dir",show_code=show_code)

    sequence_code_dir = resolve_template("sequence_code_dir",show_code=show_code, sequence_code=sequence_code)

    shot_code_dir = resolve_template("shot_code_dir",show_code=show_code, sequence_code=sequence_code, shot_code=shot_code)

    shot_config_file = resolve_template("shot_config_file",show_code=show_code, sequence_code=sequence_code, shot_code=shot_code)

    shot_config_dir = shot_config_file.parent



    if not show_code_dir.exists() or show_code.strip() == "":
        raise FileNotFoundError ("Show doesn't exists. Cancelling shot scaffolding.")

    if not sequence_code_dir.exists() or sequence_code.strip() == "":
        raise FileNotFoundError ("Sequence doesn't exists. Cancelling shot scaffolding.")

    if shot_code_dir.exists():
        raise FileExistsError ("Shot already exists. Cancelling shot scaffolding.")

    # Creates the base shot directory in the sequence
    shot_code_dir.mkdir(parents=True,exist_ok=True)

    # Creates the config directory in the shot file
    shot_config_dir.mkdir(parents=True,exist_ok=True)

    # Resolves project configs and gets list of departments used on this show
    department_list = shot_resolver(show_code, sequence_code, shot_code)["departments"]["shot"]

    # Walks through each department and creates a department directory in the shot directory. Each department directory has a publish and work directory.
    for department in department_list:
        resolve_template("shot_work_dir",show_code=show_code, sequence_code=sequence_code, shot_code=shot_code, department=department).mkdir(parents=True,exist_ok=True)
        resolve_template("shot_publish_dir",show_code=show_code, sequence_code=sequence_code, shot_code=shot_code, department=department).mkdir(parents=True,exist_ok=True)



