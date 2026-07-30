import json
from pathlib import Path
from juno.utils import load_config
from juno.paths import resolve_template, get_pipeline_root, get_show_root


def scaffold_show(show_code, title):

    show_root_dir = get_show_root()

    pipeline_root_dir = get_pipeline_root()

    sequences_dir = resolve_template("sequences_dir",show_code=show_code)

    project_config_file = resolve_template("project_config_file",show_code=show_code)
    project_config_dir = Path(project_config_file).parent

    assets_dir = resolve_template("assets_dir",show_code=show_code)

    schema_path = Path(pipeline_root_dir) / "config" / "schema" / "project.schema.json"

    project_data = {
        "$schema": str(schema_path),
        "show": {"code": show_code, "title": title},
        "pipeline_version": "0.1.0"
    }

    if (Path(show_root_dir) / str(show_code)).exists():
        raise EnvironmentError ("Show already exists. Cancelling show scaffolding.")

    # Creates the show_code directory at the show root
    (Path(show_root_dir) / show_code).mkdir(parents=True,exist_ok=True)

    # Creates the sequences directory
    Path(sequences_dir).mkdir(parents=True,exist_ok=True)

    # Creates the project config directory and file
    Path(project_config_dir).mkdir(parents=True,exist_ok=True)

    # Creates the assets directory
    Path(assets_dir).mkdir(parents=True,exist_ok=True)

    # Write project details in new project.json
    with open(project_config_file, "w") as f:
        json.dump(project_data, f, indent=4)




    








scaffold_show("DEMO_1","THE DEMO FILM")


