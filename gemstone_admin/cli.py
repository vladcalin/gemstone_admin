import os.path
import uuid
import urllib.parse
import subprocess
import sys
import datetime
import pickle
import base64

import tabulate
import click
import simplejson as json

from gemstone_admin.structs import Service, Configuration

GEMSTONE_DIR = os.path.join(os.path.expanduser("~"), ".gemstone")
CONFIG_FILE = os.path.join(GEMSTONE_DIR, ".admin")

if not os.path.isdir(GEMSTONE_DIR):
    os.mkdir(GEMSTONE_DIR)

if not os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        f.write(json.dumps({"env": {}, "installed": {}, "running": {}}))


def read_config_file():
    return Configuration.from_file(CONFIG_FILE)


def modify_env_value(key, value):
    current_config = read_config_file()
    current_config.add_env_value(key, value)
    current_config.save_to_file(CONFIG_FILE)


def get_value_from_config(key):
    current_config = read_config_file()
    return current_config.get_env_value(key)


def get_keys_from_config():
    current_config = read_config_file()
    return current_config.list_env_keys()


def register_service(service):
    current_config = read_config_file()
    current_config.add_service(service)
    current_config.save_to_file(CONFIG_FILE)


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


@click.command("reset")
def reset():
    os.remove(CONFIG_FILE)


cli.add_command(config)
cli.add_command(service)
cli.add_command(instance)
cli.add_command(reset)


# region service

@click.command("install", help="Installs a service from the given source")
@click.argument("install_source")
@click.option("--module_name", default=None)
def service_install(install_source, module_name):
    click.echo("Installing from {}".format(install_source))

    if not module_name:
        click.echo("No name specified. Assuming {}".format(install_source))
        module_name = install_source

    click.echo("Module name: {}".format(module_name))
    click.echo("Service module: {}.service".format(module_name))

    service = Service(module_name, install_source)
    if service.install():
        register_service(service)
        click.echo(click.style("Finished", fg="green"))
    else:
        click.echo(click.style(service.info, fg="red"))


@click.command("uninstall", help="Uninstalls a service")
@click.argument("name")
def service_uninstall(name):
    pass


@click.command("list", help="Lists all installed services")
def service_list():
    current_config = read_config_file()
    service_data = []
    for service in current_config.iter_services():
        service_data.append(
            [service.id, service.name, service.service_module, service.config_module, service.install_source])

    click.echo(
        tabulate.tabulate(service_data, headers=("Id", "Name", "Service module", "Config module", "Install source")))


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
    for k in current_config.list_env_keys():
        items.append((k, current_config.get_env_value(k)))
    items.sort(key=lambda x: x[0])
    print(tabulate.tabulate(items, headers=["Key", "Value"]))


config.add_command(write_config)
config.add_command(read_config)
config.add_command(list_config)

# endregion
