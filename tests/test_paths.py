from juno.paths import get_show_root, resolve_template, get_pipeline_root
import pytest
from pathlib import Path

def test_show_root_missing(monkeypatch):
    monkeypatch.delenv("JUNO_SHOW_ROOT", raising=False)
    with pytest.raises(EnvironmentError):
        get_show_root()

def test_show_root_returns_path(monkeypatch):
    monkeypatch.setenv("JUNO_SHOW_ROOT", "/test/show")
    result = get_show_root()
    assert result == Path("/test/show")

def test_pipeline_root_missing(monkeypatch):
    monkeypatch.delenv("JUNO_PIPELINE_ROOT", raising=False)
    with pytest.raises(EnvironmentError):
        get_pipeline_root()

def test_pipeline_root_returns_path(monkeypatch):
    monkeypatch.setenv("JUNO_PIPELINE_ROOT", "/test/show")
    result = get_pipeline_root()
    assert result == Path("/test/show")