import pickle
import sys
import subprocess
import hashlib


class Configuration(object):
    def __init__(self):
        self.env = {}
        self.services = []
        self.instances = []

    @classmethod
    def from_file(cls, filename):
        try:
            with open(filename, "rb") as f:
                item = pickle.load(f)
            return item
        except pickle.UnpicklingError:
            return Configuration()

    def save_to_file(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def add_service(self, service):
        self.services.append(service)

    def add_env_value(self, key, value):
        self.env[key] = value

    def delete_env_value(self, key):
        del self.env[key]

    def list_env_keys(self):
        return list(sorted(list(self.env.keys())))

    def get_env_value(self, key):
        return self.env[key]

    def iter_services(self):
        for serv in self.services:
            yield serv


class Service(object):
    def __init__(self, name, install_source):
        self.name = name
        self.service_module = name + ".service"
        self.config_module = name + ".configuration"
        self.install_source = install_source
        self.info = None

    @property
    def id(self):
        return hashlib.md5(
            self.name.encode() + self.service_module.encode() + self.install_source.encode()).hexdigest()[:10]

    def install(self):
        proc = subprocess.Popen([sys.executable, "-mpip", "install", self.install_source], stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE, universal_newlines=True)

        output, error = proc.communicate()
        if proc.returncode != 0:
            self.info = output + "\n" + error
            return False

        return True
