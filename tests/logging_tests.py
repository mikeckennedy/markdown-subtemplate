from markdown_subtemplate import logging
from markdown_subtemplate.logging import LogLevel


def test_default_log_level():
    log = logging.get_log()
    assert log.log_level == LogLevel.info


def test_can_change_log_level():
    log = logging.get_log()

    level = log.log_level
    try:
        log.log_level = LogLevel.error
        assert log.log_level == LogLevel.error
    finally:
        log.log_level = level


def test_should_log_yes():
    log = logging.get_log()
    assert log.should_log(LogLevel.info, "MSG")
    assert log.should_log(LogLevel.error, "MSG")


def test_should_log_no():
    log = logging.get_log()
    assert not log.should_log(LogLevel.verbose, "MSG")
    assert not log.should_log(LogLevel.trace, "MSG")


def test_logging_off():
    log = logging.get_log()
    level = log.log_level
    try:
        log.log_level = LogLevel.off
        assert not log.should_log(LogLevel.error, 'MSG')
        assert not log.should_log(LogLevel.verbose, 'MSG')
    finally:
        log.log_level = level
