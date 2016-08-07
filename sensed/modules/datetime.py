import datetime
from sensed.Map import Map


class Datetime(object):
    def __init__(self, config):
        self.config = config['sensed-modules-datetime']
        if 'all' in self.config.formats:
            self.config.formats = ['unix', 'iso', '12h', '24h']
        elif 'none' in config.formats:
            self.config.formats = None

    def get_data(self):
        datetimes = Map()

        if self.config.formats:
            now = datetime.datetime.now()
            if 'unix' in self.config.formats:
                datetimes.unix = now.timestamp()
            if 'iso' in self.config.formats:
                datetimes.iso = now.isoformat()
            if '12h' in self.config.formats:
                datetimes.h12 = now.strftime('%I:%M:%S%p')
            if '24h' in self.config.formats:
                datetimes.h24 = now.strftime('%H:%M:%S')

        return datetimes

    def test(self):
        return self.get_data()

Sensor = Datetime
