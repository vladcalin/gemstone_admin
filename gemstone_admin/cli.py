import os.path
import sys
import subprocess
import uuid
import urllib.parse

import click
import simplejson as json

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".gemstone_admin")
if not os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        f.write(json.dumps({"env": {}, "installed": {}, "running": {}}))


def read_config_file():
    with open(CONFIG_FILE, "r") as f:
        data = f.read()
        if not data:
            current_config = {"env": {}, "installed": {}, "running": {}}
        else:
            current_config = json.loads(data)
    return current_config


def modify_env_value(key, value):
    current_config = read_config_file()
    current_config["env"][key] = value
    with open(CONFIG_FILE, "w") as f:
        json.dump(current_config, f)


def get_value_from_config(key):
    current_config = read_config_file()
    return current_config["env"].get(key, None)


def extract_name_from_source(source):
    parsed = urllib.parse.urlparse(source)
    return os.path.split(parsed.path)[-1].split(".")[-1]


def register_service(name, source):
    raise NotImplementedError()


@click.group()
def cli():
    pass


@cli.command("install")
@click.argument("source")
@click.option("--name", default=None)
def install(source, name):
    click.echo("Installing {}".format(source))

    if not name:
        name = extract_name_from_source(source)
        click.echo("Extracted name: {}".format(name))

    proc = subprocess.Popen([sys.executable, "-mpip", "install", source],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, error = proc.communicate()

    if proc.returncode != 0:
        click.echo(click.style("Installation failed: pip exit code {}".format(proc.returncode), fg="red"))
        click.echo(click.style("\n" + output + "\n" + error + "\n", fg="red"))
        return

    register_service(source, name)

    click.echo(click.style("Finished", fg="green"))


@cli.command("write_config")
@click.argument("key")
@click.argument("value")
def write_config(key, value):
    modify_env_value(key, value)


@cli.command("read_config")
@click.argument("key")
def read_config(key):
    value = get_value_from_config(key)
    if not value:
        click.echo(click.style("Key does not exist", fg="red"))
    else:
        click.echo(value)
