import os
import sys
import json
import time
import chalk
import click
import atexit
import platform
import importlib
import socketserver

from lib.SensedServer import SensedServer


__version__ = '1.0'


def _debug(msg, tag='\\\\\\/'):
    if tag == 'INFO':
        disp = chalk.blue
    elif tag == 'WARN':
        disp = chalk.yellow
    elif tag == 'ERROR':
        disp = chalk.red
    elif tag == 'BANNER':
        disp = chalk.cyan
        tag = '\\\\\\/'
    else:
        disp = chalk.green

    tag = '[{}]'.format(tag).rjust(7)
    msg = '[{}] {} :: {}'.format(time.asctime(), tag, msg)
    disp(msg)


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
              help='Name of his sensed instance. Default: sensed')
@click.option('--sensors', '-S', default={},
              help='Sensor modules to load and enable.')
@click.option('--host', '-i', default='0.0.0.0',
              help='IP or hostname to bind to. Default: 0.0.0.0')
@click.option('--port', '-p', default=3000,
              help='Port to bind to. Default: 3000')
@click.option('--debug', '-d', default=3,
              help='Set debug level. Default: 3')
@click.option('--test', '-t', is_flag=True,
              help='Enable test mode.')
@click.option('--ci', is_flag=True, help="CI Testing.")
def sensed(config, name, sensors, host, port, debug, test, ci):
    if config is None:
        nsensors = {}
        for s in sensors:
            nsensors[s]['enabled'] = True

        cfg = {
            'name': name,
            'debug': 3,
            'host': host,
            'port': port,
            'sensors': nsensors,
            'test': test
        }
    else:
        cfg = load_config(fn=config)

        if cfg['debug']:
            verbose = True

        _debug('Loaded config', tag='INFO')

        if 'sensors' not in cfg:
            _debug(verbose, chalk.yellow, 'no sensors configured, disabling')
            cfg['sensors'] = {}
        if 'host' not in cfg:
            _debug(verbose, chalk.yellow,
                   'no host configured, defaulting to localhost')
            cfg['host'] = 'localhost'
        if 'port' not in cfg:
            _debug(verbose, chalk.yellow,
                   'no port configured, defaulting to 3000')
            cfg['port'] = 3000
        if 'name' not in cfg:
            _debug(verbose, chalk.yellow,
                   'no name configured, defaulting to sensed')
            cfg['name'] = 'sensed'
        if 'test' not in cfg:
            cfg['test'] = False

    _debug('Initializing sensed server', tag='INFO')
    server = socketserver.UDPServer((cfg['host'], cfg['port']),
                                    SensedServer)

    if len(cfg['sensors']) > 0:
        _debug('Loading modules:', tag='INFO')
        server.sensors = {}
        for sensor in cfg['sensors']:
            if cfg['sensors'][sensor]['enabled'] is True:
                try:
                    smod = importlib.import_module('lib.modules.{}'
                                                   .format(sensor))
                    server.sensors[sensor] = smod.Sensor(cfg)
                    _debug(' * {}'.format(sensor), tag='INFO')
                except Exception as e:
                    _debug(' ! {}: {}'.format(sensor, e), tag='ERROR')

    server.config = cfg

    _debug('sensed v{} ready'.format(__version__), tag='BANNER')
    if cfg['test'] == True:
        _debug('test mode is active', tag='WARN')

    if ci is True:
        _debug('testing successful, terminating')
        server.server_close()
        sys.exit(0)
    else:
        @atexit.register
        def close():
            _debug('shutting down')
            server.shutdown()
        server.serve_forever()

if __name__ == '__main__':
    sensed()
