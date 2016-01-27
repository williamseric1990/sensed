import os
import json


class SensedServer(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip().decode('utf-8')
        header = data[:2]
        body = data[2:]
        socket = self.request[1]
        if header == '\x01\x00':
            self._Debug(chalk.cyan, 'recieved id request')
            # collect list of sensors, etc.
            #socket.sendto(bytes(p + '\n', 'utf-8'), self.client_address)
            self._Debug(chalk.magenta, 'sent id data')
        elif header == '\x02\x00':
            if len(body) > 0:
                body = body.split(',')
                self._Debug(chalk.blue,
                            'recieved request for: {}'.format(repr(body))
            else:
                self._Debug(chalk.blue, 'recieved request for sensor data')
            
            # get data for specified sensors
            self._Debug(chalk.red, 'scan data: ' + repr(r))
            #socket.sendto(bytes(r + '\n', 'utf-8'), self.client_address)
            self._Debug(chalk.yellow, 'sent sensor data')

    def to_packet(self, seq):
        ret = []
        for k in seq:
            ret.append(k + ',' + seq[k])
        return ';'.join(ret) + '\n'

    def _Debug(self, f, arg):
        if self.server.verbose:
            f(arg)


# Finds a config file in a number of default locations in a
# Linux/Unix environment. Checks in the following places:
#  1. /etc/sensed/
#  2. .
def find_config_posix(name):
    if os.path.isfile('/etc/sensed/config.json'):
        return '/etc/sensed/config.json'
    elif os.path.isfile('./config.json'):
        return './config.json'
    return None


# Finds a config file in a number of default locations in a
# Windows environment. Checks in the following places:
#  1. %APPDATA%\sensed\
#  2. .
def find_config_windows(name):
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


def load_config():
    f = find_config()
    with open(f, 'r') as fq:
        config = json.loads(fp.read())
        return config
    return None

if __name__ == '__main__':
    config = load_config()
    if config:
        pass # start server
    print('could not locate config file')