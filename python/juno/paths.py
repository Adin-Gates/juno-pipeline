import os
import json
from juno.utils import load_config
from pathlib import Path



# get_show_root : extracts the show root form the environent
def get_show_root():
    show_root = os.environ.get("JUNO_SHOW_ROOT")

    if show_root is None:
        raise EnvironmentError("No show root found.")


    return Path(show_root)


# get_pipeline_root : extracts the pipeline root from the environment
def get_pipeline_root():
    pipeline_root = os.environ.get("JUNO_PIPELINE_ROOT")

    if pipeline_root is None:
        raise EnvironmentError("No pipeline root found.")


    return Path(pipeline_root)



# resolve_template : given a template name string and tokens that naming scheme needs this will generate the corrent path
def resolve_template(template_name, **tokens):

    #template_path = Path(__file__).parent.parent.parent / "config" / "templates.json"

    template_path = get_pipeline_root() / "config" / "templates.json"

    template_dict = load_config(template_path)

    template = template_dict[template_name]

    result = template.format(**tokens)

    show_root = get_show_root()

    return show_root / result



def get_show_title(show_code):

    config_file_path = resolve_template("project_config_file",show_code=show_code)

    project_config = load_config(config_file_path)

    title = project_config["show"]["title"]

    return title


def list_shows():

    show_root = get_show_root()
    all_entries = show_root.iterdir()
    show_list = []

    for i in all_entries:
        if i.is_dir():
            show_code = i.name
            show_list.append(show_code)

    return show_list


def list_sequences(show_code):

    sequences_dir = resolve_template("sequences_dir",show_code=show_code)
    all_entries = sequences_dir.iterdir()
    sequence_list = []

    for i in all_entries:
        if i.is_dir():
            sequence_code = i.name
            sequence_list.append(sequence_code)

    return sequence_list


def list_shots(show_code, sequence_code):

    sequence_code_dir = resolve_template("sequence_code_dir",show_code=show_code, sequence_code=sequence_code)
    all_entries = sequence_code_dir.iterdir()
    shot_list = []

    for i in all_entries:
        if i.is_dir():
            shot_code = i.name
            shot_list.append(shot_code)

    return shot_list


