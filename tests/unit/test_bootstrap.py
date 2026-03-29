from __future__ import annotations

from pathlib import Path

import pytest

from local_agentic_rag import bootstrap
from local_agentic_rag.config import load_config
from tests.conftest import write_test_config


def test_bootstrap_checks_handle_missing_ollama_without_shell_which(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    docs_path = tmp_path / "docs"
    docs_path.mkdir()
    config_path = write_test_config(tmp_path, docs_path)
    app_config = load_config(config_path)

    monkeypatch.setattr(bootstrap.shutil, "which", lambda _: None)

    def fail_if_subprocess_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("subprocess.run should not be called when ollama is missing")

    monkeypatch.setattr(bootstrap.subprocess, "run", fail_if_subprocess_run)

    report = bootstrap.run_bootstrap_checks(app_config)

    assert report.ollama_installed is False
    assert any("Ollama is not installed" in note for note in report.notes)