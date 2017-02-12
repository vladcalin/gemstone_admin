import sys
import subprocess
import hashlib


class Service(object):
    def __init__(self, name, install_source):
        self.name = name
        self.service_module = name + ".service"
        self.install_source = install_source
        self.info = None

    @property
    def id(self):
        return hashlib.md5(
            self.name.encode() + self.service_module.encode() + self.install_source.encode()).hexdigest()[:10]

    def to_dict(self):
        return {
            "name": self.name,
            "service_module": self.service_module,
            "install_source": self.install_source,
            "id": self.id
        }

    def install(self):
        proc = subprocess.Popen([sys.executable, "-mpip", "install", self.install_source], stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE, universal_newlines=True)

        output, error = proc.communicate()
        if proc.returncode != 0:
            self.info = output + "\n" + error
            return False

        return True
