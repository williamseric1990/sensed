import os
import picamera


class Sensor(object):
    ''' `sensed` sensor module for the Raspberry Pi NoIR camera. This
        module returns a JPEG image. '''

    def __init__(self):
        self.camera = picamera.PiCamera()

    def get_data(self):
        self.camera.capture('img.jpg')
        with open('img.jpg', 'rb') as fp:
            return fp.read()
        os.remove('img.jpg')
