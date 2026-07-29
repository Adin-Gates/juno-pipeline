import os
import json
from juno.utils import load_config
from pathlib import Path



# get_show_root : extracts the show root form the environemt
def get_show_root():
    show_root = os.environ.get("JUNO_SHOW_ROOT")

    if show_root is None:
        raise EnvironmentError("No show root found.")


    return Path(show_root)


# resolve_template : given a template name string and tokens that naming scheme needs this will generate the corrent path
def resolve_template(template_name, **tokens):

    template_path = Path(__file__).parent.parent.parent / "config" / "templates.json"

    template_dict = load_config(template_path)

    template = template_dict[template_name]

    result = template.format(**tokens)

    show_root = get_show_root()

    return show_root / result
