import os
import picamera


class Camera(object):
    ''' `sensed` sensor module for the Raspberry Pi NoIR camera. This
        module returns a JPEG image. '''

    def __init__(self):
        self.camera = picamera.PiCamera()

    def get_data(self):
        self.camera.capture('img.jpg')
        with open('img.jpg', 'rb') as fp:
            return {'camera': fp.read()}
        os.remove('img.jpg')

    def test(self):
        return {'camera': 'testdata'}


Sensor = Camera
