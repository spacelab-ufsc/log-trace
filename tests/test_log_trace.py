"""Unit tests for log_trace.

The module talks to a serial port, so only the pure helpers are covered here:
ANSI stripping and the error/info routing of save_logs. Neither needs hardware.
"""

import logging
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import log_trace


class TestRemoveAnsiColor:
    def test_plain_text_is_unchanged(self):
        assert log_trace.remove_ansi_color("booting EPS") == "booting EPS"

    def test_strips_the_error_colour_used_by_the_firmware(self):
        line = f"{log_trace.ERROR_CODE}EPS fault\033[0m"
        assert log_trace.remove_ansi_color(line) == "EPS fault"

    def test_strips_several_codes_in_one_line(self):
        line = "\033[1;32mOK\033[0m \033[1;31mFAIL\033[0m"
        assert log_trace.remove_ansi_color(line) == "OK FAIL"

    def test_keeps_the_text_around_the_codes(self):
        line = "[\033[1;31m12345\033[0m] watchdog reset"
        assert log_trace.remove_ansi_color(line) == "[12345] watchdog reset"

    def test_empty_string(self):
        assert log_trace.remove_ansi_color("") == ""


class TestSaveLogs:
    def test_coloured_error_line_is_logged_as_error(self, caplog):
        with caplog.at_level(logging.DEBUG):
            log_trace.save_logs(f"{log_trace.ERROR_CODE}antenna timeout\033[0m")

        assert caplog.records[0].levelno == logging.ERROR

    def test_plain_line_is_logged_as_info(self, caplog):
        with caplog.at_level(logging.DEBUG):
            log_trace.save_logs("antenna deployed")

        assert caplog.records[0].levelno == logging.INFO

    def test_the_colour_codes_are_not_written_to_the_log_file(self, caplog):
        with caplog.at_level(logging.DEBUG):
            log_trace.save_logs(f"{log_trace.ERROR_CODE}EPS fault\033[0m")

        assert "\033" not in caplog.records[0].getMessage()
        assert caplog.records[0].getMessage() == "EPS fault"


def test_setup_logging_creates_the_directory_and_file(tmp_path):
    log_dir = tmp_path / "logs"

    log_trace.setup_logging("obdh", str(log_dir))

    assert (log_dir / "obdh.log").is_file()
