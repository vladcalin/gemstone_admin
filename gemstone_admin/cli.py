import os.path
import sys

import click
import simplejson as json

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".gemstone_admin")
if not os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        f.write(json.dumps({"env": {}, "installed": {}, "running": {}}))


def modify_env_value(key, value):
    with open(CONFIG_FILE, "r") as f:
        data = f.read()
        if not data:
            current_config = {"env": {}, "installed": {}, "running": {}}
        else:
            current_config = json.loads(data)

    current_config["env"][key] = value

    with open(CONFIG_FILE, "w") as f:
        json.dump(current_config, f)


def get_value_from_config(key):
    with open(CONFIG_FILE, "r") as f:
        data = f.read()
        if not data:
            current_config = {"env": {}, "installed": {}, "running": {}}
        else:
            current_config = json.loads(data)

    return current_config["env"].get(key, None)


@click.group()
def cli():
    pass


@cli.command("install")
@click.argument("source")
def install(source):
    click.echo("Installing {}".format(source))


@cli.command("write_config")
@click.argument("key")
@click.argument("value")
def config(key, value):
    modify_env_value(key, value)


@cli.command("read_config")
@click.argument("key")
def read_config(key):
    value = get_value_from_config(key)
    if not value:
        click.echo(click.style("Key does not exist", fg="red"))
    else:
        click.echo(value)
