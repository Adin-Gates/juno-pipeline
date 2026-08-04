import json

# load_config : takes a path to a JSON file and returns said JSON file as a dict without the "$schema"
def load_config(path):

    with open(path) as f:
        data = json.load(f)

    data.pop("$schema", None)

    return data

# load_schema : takes a path to a JSON file and returns said JSON file as a dict.
def load_schema(path):

    with open(path) as f:
        data = json.load(f)

    return data