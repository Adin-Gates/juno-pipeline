import json
from jsonschema import validate, Draft202012Validator
from referencing import Registry, Resource
from jsonschema.exceptions import ValidationError
from pathlib import Path
from juno.utils import load_config, load_schema
from juno.paths import resolve_template, get_show_root, get_pipeline_root


# Takes a given string and returns it with green coloring
def green_text(text):
    return f"\033[92m{text}\033[0m"


# Takes a given string and returns it with red coloring
def red_text(text):
    return f"\033[91m{text}\033[0m"


# validate_config : Takes in a config and it's schema, raises an error if the config isn't in line with the given schema.
def validate_config(data, schema, common_schema):

    registry = Registry().with_resource(
        "common.schema.json",
        Resource.from_contents(common_schema)
    )

    validator = Draft202012Validator(schema, registry=registry)

    try:
        validator.validate(data)
        print("Validated")

    except ValidationError as e:
        raise ValueError(f"Config validation failure at {e.json_path}. Message: {e.message}.")




# extract_deep_value : takes a key and a dictionary, searches a nested dictionary to extract the value of the key if the key exists
def extract_deep_value(deep_key, dictionary):

    for key, value in dictionary.items():

        if str(key) == str(deep_key):
            return value

        elif isinstance(value, dict):              
            deep_value = extract_deep_value(deep_key, value)

            if deep_value is not None:
                return deep_value



# extract refs : given a reference (JSON) string and the common dictionary to search. This will return the referenced value
def extract_refs(ref_string, dict):

    split_string = ref_string.split("/")[1:]

    current = dict

    for i in split_string:
        current = current[i]

    return current


# print_dict is a function that prints out all of the keys and values of a given dictionary, including nested dictionaries.
def print_dict(config, prefix=""):

    if isinstance(config, dict):

        for key, value in config.items():
            new_prefix = f"{prefix} -> {key}" if prefix else key

            if isinstance(value, dict):

                print_dict(value, new_prefix)

            else:
                print(new_prefix, "==", green_text(value))

    else:
        print(red_text("'print_dict' Requires a dictionary. No dictionary given."))
            
        
# deep_merge takes two dictionaries, a base and an override, and replaces the values of the base dictionary with the override. This worked on nested dictionaries.
def deep_merge(base, override):

    result = base.copy()

    for key, value in override.items():

        if isinstance(value, dict):
            result[key] = deep_merge(result[key], value)

        else:
            result[key] = value

    return result


# extract_defaults : Takes in the project schema and the common schema to create a dictionary with all default values
def extract_defaults(schema, common):

    if "default" in schema:
        return schema["default"]


    if "$ref" in schema:
        resolved = extract_refs(schema["$ref"], common)
        return extract_defaults(resolved, common)

    result = {}

    properties = schema.get("properties", {})

    for key, subschema in properties.items():
        extracted = extract_defaults(subschema, common)
        if extracted != {}:
            result[key] = extracted

    return result


# load_defaults : using pathlib this function finds the project.schema and the common.schema and loads in a config with all default values
def load_defaults():

    schema_dir = get_pipeline_root() / "config" / "schema"
    project_schema_path = schema_dir / "project.schema.json"
    common_schema_path = schema_dir / "common.schema.json"


    project_schema = load_config(project_schema_path)
    common_schema = load_config(common_schema_path)

    project_default = extract_defaults(project_schema, common_schema)

    return project_default



# project_config_resolver : currently takes the path to the project and shot jsons and layers them onto the default values to give us a resolved config
def project_config_resolver(project_path, shot_path=None):

    project_default = load_defaults()
    project = load_config(project_path)

    project_schema_path = get_pipeline_root() / "config" / "schema" / "project.schema.json"
    common_schema_path = get_pipeline_root() / "config" / "schema" / "common.schema.json"

    project_schema = load_schema(project_schema_path)
    common_schema = load_schema(common_schema_path)

    validate_config(project, project_schema, common_schema)
    
    project_resolved = deep_merge(project_default, project)

    if shot_path is not None:

        shot = load_config(shot_path)

        shot_schema_path = get_pipeline_root() / "config" / "schema" / "shot.schema.json"
        shot_schema = load_schema(shot_schema_path)

        validate_config(shot, shot_schema, common_schema)

        shot_resolved = deep_merge(project_resolved, shot)
        return shot_resolved

    return project_resolved


# shot_resolver : takes in the show_code, sequence, and shot and then returns the resolved config
def shot_resolver(show_code, sequence_code, shot_code):

    shot_path = resolve_template("shot_config_file",show_code=show_code,sequence_code=sequence_code,shot_code=shot_code)

    project_path = resolve_template("project_config_file",show_code=show_code)

    if shot_path.exists():
        return project_config_resolver(project_path, shot_path)
    else:
        return project_config_resolver(project_path)






if __name__ == "__main__":
    pass