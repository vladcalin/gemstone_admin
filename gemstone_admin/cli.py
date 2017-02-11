import os.path
import sys
import subprocess
import uuid
import urllib.parse

import tabulate
import click
import simplejson as json
import yaml

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


@click.group(help='Global configuration management')
def config():
    pass


@click.group(help='Service configuration')
def service():
    pass


@click.group(help='Running microservice instances')
def instance():
    pass


cli.add_command(config)
cli.add_command(service)
cli.add_command(instance)


# region service

@click.command("install", help="Installs a service from the given source")
@click.argument("install_file")
def service_install(install_file):
    click.echo("Installing from {}".format(install_file))

    with open(install_file) as f:
        config = yaml.load(f)

    print(config)

    click.echo(click.style("Finished", fg="green"))


@click.command("uninstall", help="Uninstalls a service")
@click.argument("name")
def service_uninstall(name):
    pass


@click.command("list", help="Lists all installed services")
def service_list():
    pass


service.add_command(service_install)
service.add_command(service_uninstall)
service.add_command(service_list)


# endregion

# region config

@click.command("write")
@click.argument("key")
@click.argument("value")
def write_config(key, value):
    modify_env_value(key, value)


@click.command("read")
@click.argument("key")
def read_config(key):
    value = get_value_from_config(key)
    if not value:
        click.echo(click.style("Key does not exist", fg="red"))
    else:
        click.echo(value)


@click.command("list")
def list_config():
    current_config = read_config_file()
    items = []
    for k, v in current_config["env"].items():
        items.append((k, v))
    items.sort(key=lambda x: x[0])
    print(tabulate.tabulate(items, headers=["Key", "Value"], tablefmt="grid"))


config.add_command(write_config)
config.add_command(read_config)
config.add_command(list_config)

# endregion
