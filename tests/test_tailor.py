# -*- coding: utf-8 -*-
import os

import pytest

from pytailor import Tailor

from .config import DevConfig

pytestmark = pytest.mark.unit


def setup_function():
    try:
        del os.environ["FOO"]
    except KeyError:
        pass
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


def test_watch_env_var_that_doesnt_exist_raises_warning():
    config = Tailor()
    with pytest.warns(RuntimeWarning) as warn:
        config.watch_env_var("BAR")

    assert len(warn) == 1
    assert "not found" in warn[0].message.args[0]


def test_watch_env_var_that_doesnt_exist_but_exists_in_config_object():
    config = Tailor()
    config["BAR"] = "BAZ"
    config.watch_env_var("BAR")
    assert "BAR" in config
    assert config["BAR"] == "BAZ"


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


def test_dunder_str():
    expected = "{'DEBUG': True}"
    config = Tailor()
    config["DEBUG"] = True
    assert str(config) == expected


def test_dunder_eq():
    config_one = Tailor()
    config_one["DEBUG"] = True

    config_two = Tailor()
    config_two["DEBUG"] = True

    assert config_one == config_two


def test_dunder_ne():
    config_one = Tailor()
    config_one["DEBUG"] = True

    config_two = Tailor()
    config_two["DEBUG"] = False

    assert config_one != config_two
