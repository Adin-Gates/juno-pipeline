from juno.config import deep_merge, extract_refs, extract_defaults



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