import os
import json
import chalk
import click
import atexit
import platform

from .lib import SenselogClient


def _debug(verbose, f, arg):
    if verbose:
        f(arg)


# Finds a config file in a number of default locations in a
# Linux/Unix environment. Checks in the following places:
#  1. /etc/sensed/
#  2. .
def find_config_posix():
    if os.path.isfile('/etc/sensed/config.json'):
        return '/etc/sensed/config.json'
    elif os.path.isfile('./config.json'):
        return './config.json'
    return None


# Finds a config file in a number of default locations in a
# Windows environment. Checks in the following places:
#  1. %APPDATA%\sensed\
#  2. .
def find_config_windows():
    if os.path.isfile(os.path.join(os.getenv('APPDATA'),
                      'sensed', 'config.json')):
        return os.path.join(os.getenv('APPDATA'), 'sensed', 'config',
                            'config.json')
    elif os.path.isfile('./config.json'):
        return './config.json'
    return None


# Wrapper for the above two functions that will select
# the proper one automatically.
def find_config():
    if platform.system() == 'Windows':
        return find_config_windows()
    return find_config_posix()


def load_config(fn=None):
    f = fn or find_config()
    with open(f, 'r') as fp:
        config = json.loads(fp.read())
        return config
    return None


@click.command()
@click.option('--config', '-c', default=None,
              help='Configuration file for this instance.')
@click.option('--name', '-n', default='sensed',
              help='Name of his lidard instance. Should be unique on the \
                    network. Default: sensed')
@click.option('--sensors', '-S', default={},
              help='Sensor modules to load and enable.')
@click.option('--port', '-p', default=3000,
              help='Port used by clients to recieve data. Default: 3000')
@click.option('--bind', '-i', default='0.0.0.0',
              help='Binding interface for the socket server. Default: 0.0.0.0')
@click.option('--verbose', '-V', is_flag=True,
              help='Enable verbose output (debugging)')
def sensed(config, name, sensors, port, bind, verbose):
    if config is None:
        _debug(verbose, chalk.green, 'no config found, using defaults')
        nsensors = {}
        for s in sensors:
            nsensors[s]['enabled'] = True

        cfg = {
            'name': name,
            'debug': verbose,
            'bind': bind,
            'port': port,
            'sensors': nsensors
        }
    else:
        _debug(verbose, chalk.green, 'loading config... ')
        cfg = load_config(fn=config)

        if 'sensors' not in cfg:
            cfg['sensors'] = {}
        if 'bind' not in cfg:
            cfg['bind'] = '0.0.0.0'
        if 'port' not in cfg:
            cfg['port'] = port
        if 'name' not in cfg:
            cfg['name'] = 'sensed'

        _debug(verbose, chalk.green, 'done loading')

    # TODO: instantiate enabled sensor modules here

    _debug(verbose, chalk.blue, 'connecting to server')
    client = SenselogClient(cfg)

    @atexit.register
    def close():
        chalk.blue('shutting down')
        client.shutdown()

    chalk.blue('sensed ready')

if __name__ == '__main__':
    sensed()
