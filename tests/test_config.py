from juno.config import deep_merge


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