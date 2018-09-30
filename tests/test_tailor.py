# -*- coding: utf-8 -*-
import os

import pytest

from pytailor import Tailor

from .config import DevConfig

pytestmark = pytest.mark.unit


def setup_function():
    os.environ["FOO"] = "BAR"


def teardown_function():
    try:
        del os.environ["FOO"]
    except KeyError:
        pass


def test_from_object():
    config = Tailor()
    config.from_object(DevConfig)
    assert "DEBUG" in config
    assert config["DEBUG"] is True


def test_from_dotenv(env_path):
    config = Tailor()
    config.from_dotenv(env_path)
    assert "DEBUG" in config
    assert config["DEBUG"] is True


def test_from_object_and_then_dotenv(env_path):
    config = Tailor()
    config.from_dotenv(env_path)
    config.from_object(DevConfig)
    assert "DEBUG" in config
    assert "TESTING" in config
    assert config["DEBUG"] is True
    assert config["TESTING"] is False


def test_watch_env_var_and_change_after_watching():
    config = Tailor()
    config.watch_env_var("FOO")
    assert config["FOO"] == "BAR"
    os.environ["FOO"] = "BAZ"
    assert config["FOO"] == "BAZ"


def test_env_var_is_set_then_gets_removed():
    config = Tailor()
    config.watch_env_var("FOO")
    del os.environ["FOO"]
    # check original value was backed up
    assert config["FOO"] == "BAR"


def test_user_can_change_value_manually():
    config = Tailor()
    config["FOO"] = "BAZ"
    assert config["FOO"] == "BAZ"


def test_user_can_use_number_types_with_dotenv(env_path):
    config = Tailor()
    config.from_dotenv(env_path)
    assert isinstance(config["MAX_LINES"], int)
    assert config["MAX_LINES"] == 10
    assert isinstance(config["TEMPERATURE"], float)
    assert config["TEMPERATURE"] == 98.2
