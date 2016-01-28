import os
import json
import time
import chalk
import click
import atexit
import platform
import socketserver


class SensedServer(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip().decode('utf-8')
        header = data[:2]
        body = data[2:]
        socket = self.request[1]
        if header == '\x01\x00':
            self._debug(chalk.cyan, 'recieved id request')
            # collect list of sensors, etc.
            sensors = ','.join(self.server.config['sensors'].keys())
            name = self.server.config['name']
            p = name + '|' + sensors
            socket.sendto(bytes(p + '\n', 'utf-8'), self.client_address)
            self._debug(chalk.magenta, 'sent id data')
        elif header == '\x02\x00':
            if len(body) > 0:
                body = body.split(',')
                self._debug(chalk.blue,
                            'recieved request for: {}'.format(repr(body)))
            else:
                self._debug(chalk.blue, 'recieved request for sensor data')
            
            # get data for specified sensors
            self._debug(chalk.red, 'sensor data: ' + repr(r))
            # r = self.to_packet(data) + '|' + int(time.time())
            # socket.sendto(bytes(r + '\n', 'utf-8'), self.client_address)
            self._debug(chalk.yellow, 'sent sensor data')

    def to_packet(self, seq):
        ret = []
        for k in seq:
            ret.append(k + ',' + seq[k])
        return ';'.join(ret) + '\n'

    def _debug(self, f, arg):
        if self.server.config['verbose']:
            f(arg)


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

    _debug(verbose, chalk.blue, 'starting server')
    server = socketserver.UDPServer((cfg['bind'], cfg['port']), SensedServer)
    server.config = cfg

    @atexit.register
    def close():
        chalk.blue('shutting down')
        server.server_close()

    chalk.blue('sensed ready')
    server.serve_forever()


if __name__ == '__main__':
    sensed()
