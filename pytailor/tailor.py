# -*- coding: utf-8 -*-
import os

from .helpers import dotenv_to_dict, str_to_py


class Tailor(dict):
    def __init__(self):
        self.env_store = dict()
        self.store = dict()

    def __getitem__(self, key):
        rv = None
        if key in self.env_store:
            # environment variables always take precedence
            try:
                env_value = os.environ[key]
                rv = str_to_py(env_value)
            except KeyError:
                # system environment variable no longer exists
                # does a saved config value exist?
                if key in self.store:
                    rv = self.store[key]
                else:
                    # seems the user deleted their environment variable and
                    # don't have it configured in a file
                    rv = self.env_store[key]
        else:
            rv = self.store[key]

        return rv

    def __setitem__(self, key, val):
        self.store.__setitem__(key, val)

    def __contains__(self, item):
        return item in self.store

    def __str__(self):
        return str(self.store)

    def from_object(self, obj: object):
        """Read configuration from an object."""
        _store = {
            key: value
            for key, value in obj.__dict__.items()
            if not key.startswith("__")
        }
        for name, value in _store.items():
            self.store[name] = value

    def from_dotenv(self, path: str):
        """Load configuration from specified .env path."""
        _store = dotenv_to_dict(path)
        for name, value in _store.items():
            self.store[name] = value

    def watch_env_var(self, name: str):
        """Set configuration and watch a system wideenvironment variable."""
        value = os.environ[name]
        mod_value = str_to_py(value)
        self.env_store[name] = mod_value
