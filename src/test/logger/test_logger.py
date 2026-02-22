import logging

import pytest

import bronto.logger as logger_module


@pytest.fixture(autouse=True)
def restore_root_logger():
    root = logging.getLogger()
    original_handlers = list(root.handlers)
    original_level = root.level
    yield
    for handler in list(root.handlers):
        root.removeHandler(handler)
    for handler in original_handlers:
        root.addHandler(handler)
    root.setLevel(original_level)


def test_resolve_level_returns_int_level_as_is():
    assert logger_module._resolve_level(logging.WARNING) == logging.WARNING


def test_resolve_level_reads_named_level_from_env(monkeypatch):
    monkeypatch.setenv("BRONTO_LOG_LEVEL", "debug")
    assert logger_module._resolve_level(None) == logging.DEBUG


def test_resolve_level_reads_numeric_level_from_env(monkeypatch):
    monkeypatch.setenv("BRONTO_LOG_LEVEL", "15")
    assert logger_module._resolve_level(None) == 15


def test_resolve_level_falls_back_to_info_for_unknown_level(monkeypatch):
    monkeypatch.setenv("BRONTO_LOG_LEVEL", "not-a-real-level")
    assert logger_module._resolve_level(None) == logging.INFO


def test_bootstrap_logging_updates_existing_handlers_without_replacing():
    root = logging.getLogger()
    existing_handler = logging.StreamHandler()
    existing_handler.setLevel(logging.WARNING)
    root.addHandler(existing_handler)
    handlers_before = list(root.handlers)
    root.setLevel(logging.WARNING)

    logger_module.bootstrap_logging(level="ERROR", force=False)

    assert root.level == logging.ERROR
    assert root.handlers == handlers_before
    assert all(handler.level == logging.ERROR for handler in handlers_before)


def test_bootstrap_logging_force_replaces_handlers_and_sets_formatter(monkeypatch):
    root = logging.getLogger()
    root.addHandler(logging.NullHandler())
    monkeypatch.setenv("BRONTO_LOG_FORMAT", "%(levelname)s|%(message)s")
    monkeypatch.setenv("BRONTO_LOG_DATE_FORMAT", "%H:%M")

    logger_module.bootstrap_logging(level="INFO", force=True)

    assert len(root.handlers) == 1
    handler = root.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert handler.level == logging.INFO
    assert handler.formatter is not None
    assert handler.formatter._fmt == "%(levelname)s|%(message)s"
    assert handler.formatter.datefmt == "%H:%M"


def test_module_logger_returns_named_logger():
    logger = logger_module.module_logger("bronto.unit")
    assert logger.name == "bronto.unit"
