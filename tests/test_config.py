from juno.config import deep_merge, extract_refs, extract_defaults, validate_config
from juno.paths import resolve_template, get_show_root, get_pipeline_root
from juno.utils import load_schema, load_config
import pytest



# DEEP MERGE TESTS
def test_nested_override_preserves_siblings():
    base = {"frames": {"handles": {"head": 8, "tail": 8}}}
    override = {"frames": {"handles": {"head": 24}}}
    result = deep_merge(base, override)
    assert result == {"frames": {"handles": {"head": 24, "tail": 8}}}


def test_original_base_not_mutated():
    base = {"frames": {"handles": {"head": 8, "tail": 8}}}
    override = {"frames": {"handles": {"head": 24}}}
    deep_merge(base, override)
    assert base == {"frames": {"handles": {"head": 8, "tail": 8}}}


def test_new_key_from_override_is_added():
    result = deep_merge({"a": 1}, {"b": 2})
    assert result == {"a": 1, "b": 2}


def test_lists_replace_wholesale():
    result = deep_merge({"scales": [0.5, 0.25]}, {"scales": [0.5]})
    assert result == {"scales": [0.5]}


#EXTRACT_REFS TESTS

def test_normal_ref():
    ref = "common.schema.json#/$defs/format"
    dictionary = {"$defs": {"format": {"test": "value"}}}
    result = extract_refs(ref, dictionary)
    assert result == {"test": "value"}


#EXTRACT_DEFULTS TESTS

def test_normal_return_defaults():
    schema = {"properties": {"main": {"default": 5}}}
    common = {}
    result = extract_defaults(schema, common)
    assert result == {"main": 5}


def test_no_default_return():
    schema = {"properties": {"main": {"something": 5}}}
    common = {}
    result = extract_defaults(schema, common)
    assert result == {}


def test_nested_defaults():
    schema = {"properties": {"main": { "properties": {"fps": {"default": 5}}}}}
    common = {}
    result = extract_defaults(schema, common)
    assert result == {"main": {"fps": 5}}


def test_ref_defaults():
    schema = {"properties": {"format": {"$ref": "common.schema.json#/$defs/format"}}}
    common = {"$defs": {"format": {"default": "value"}}}
    result = extract_defaults(schema, common)
    assert result == {"format": "value"}


# VALIDATE CONFIG TESTS

def test_valid_config():
    project = {"show": {"code": "DEMO", "title": "Demo Show"}, "format": {"fps": 24}, "pipeline_version": "0.1.0"}

    project_schema_path = get_pipeline_root() / "config" / "schema" / "project.schema.json"
    common_schema_path = get_pipeline_root() / "config" / "schema" / "common.schema.json"

    project_schema = load_schema(project_schema_path)
    common_schema = load_schema(common_schema_path)

    result = validate_config(project,project_schema,common_schema)
    assert result == None

def test_invalid_config():
    project = {"show": {"title": "Demo Show"}, "format": {"fps": 24}, "pipeline_version": "0.1.0"}

    project_schema_path = get_pipeline_root() / "config" / "schema" / "project.schema.json"
    common_schema_path = get_pipeline_root() / "config" / "schema" / "common.schema.json"

    project_schema = load_schema(project_schema_path)
    common_schema = load_schema(common_schema_path)

    with pytest.raises(ValueError):
        validate_config(project,project_schema,common_schema)


def test_invalid_config_common():
    project = {"show": {"title": "Demo Show"}, "format": {"fps": "twenty-four"}, "pipeline_version": "0.1.0"}

    project_schema_path = get_pipeline_root() / "config" / "schema" / "project.schema.json"
    common_schema_path = get_pipeline_root() / "config" / "schema" / "common.schema.json"

    project_schema = load_schema(project_schema_path)
    common_schema = load_schema(common_schema_path)

    with pytest.raises(ValueError):
        validate_config(project,project_schema,common_schema)