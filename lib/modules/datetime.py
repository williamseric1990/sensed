import datetime

class Datetime(object):
    def __init__(self):
        pass

    def get_data(self):
        now = datetime.datetime.now()
        return {'unix': now.timestamp(),
                'iso': now.isoformat(),
                '12h': now.strftime('%I:%M:%S%p'),
                '24h': now.strftime('%H:%M:%S')}

    def test(self):
        return {'unix': 1469814873.595497,
                'iso': '2016-07-29T13:54:33.595497',
                '12h': '01:54:33PM',
                '24h': '13:54:33'}

Sensor = Datetime