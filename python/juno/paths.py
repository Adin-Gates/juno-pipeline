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
