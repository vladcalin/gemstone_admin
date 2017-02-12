import sys
import configparser


class ServiceSpecsFileParser(object):
    def __init__(self, install_file, get_global_value=lambda x: None, get_global_keys=lambda: []):
        self.config = configparser.ConfigParser()
        with open(install_file) as f:
            self.config.read_file(f)
        self.get_global_value = get_global_value
        self.get_global_keys = get_global_keys

        self._metadata = {}
        self._install = {"commands": []}
        self._uninstall = {"commands": []}
        self._env = {
            "default": {
                "python": sys.executable
            },
            "runtime": {},
            "env": {}
        }
        self._start = {"commands": []}
        self._stop = {"commands": []}
        self.initial_parse()

    def get_metadata(self):
        pass

    def get_install(self):
        pass

    def get_uninstall(self):
        pass

    def get_env(self):
        pass

    def get_start(self):
        pass

    def get_stop(self):
        pass

    def initial_parse(self):
        # env values from global
        for key in self.get_global_keys():
            self.add_env_value(key, self.get_global_value(key))

        # env values from config
        for key, value in self.config["environment"].items():
            self.add_env_value(key, value)

        # metadata
        for key, value in self.config["metadata"].items():
            self.add_metadata_value(key, value)

        # install
        for command in self.config["install"]["commands"].splitlines():
            self._install["commands"].append(command)

        # uninstall
        for command in self.config["uninstall"]["commands"].splitlines():
            self._uninstall["commands"].append(command)

        # start
        for command in self.config["start"]["commands"].splitlines():
            self._start["commands"].append(command)

        # stop
        for command in self.config["stop"]["commands"].splitlines():
            self._stop["commands"].append(command)

    def add_env_value(self, key, value):
        self._env["env"][key] = value

    def add_runtime_value(self, key, value):
        self._env["runtime"][key] = value

    def add_metadata_value(self, key, value):
        self._metadata[key] = value

    def get_as_json(self):
        return {
            "metadata": self.get_metadata(),
            "install": self.get_install(),
            "uninstall": self.get_uninstall(),
            "environment": self.get_env(),
            "start": self.get_start(),
            "stop": self.get_stop()
        }
