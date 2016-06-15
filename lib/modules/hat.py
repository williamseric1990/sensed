from sense_hat import SenseHat


class Hat(object):
    ''' `sensed` sensor module for the Raspberry Pi Sense HAT. This
        module returns a dictionary of all built in sensors. '''

    def __init__(self):
        self.sense = SenseHat()

    def get_data(self):
        # Environmental sensors
        humid = self.sense.humidity
        temp = self.sense.temperature
        temp_h = self.sense.get_temperature_from_humidity()
        temp_p = self.sense.get_temperature_from_pressure()
        press = self.sense.pressure

        # IMU (inertial measurement unit) sensors
        orient_r = self.sense.orientation_radians
        orient_d = self.sense.orientation_degrees
        compass = self.sense.compass
        compass_r = self.sense.compass_raw
        gyro = self.sense.gyroscope
        gyro_r = self.sense.gyroscope_raw
        accel = self.sense.accelerometer
        accel_r = self.sense.accelerometer_raw

        return {'environment': {'humidity': humid,
                                'temperature': temp,
                                'temperature_h': temp_h,
                                'temperature_p': temp_p,
                                'pressure': press},
                'imu': {'orientation_rad': orient_r,
                        'orientation_deg': orient_d,
                        'compass': compass,
                        'compass_r': compass_r,
                        'gyroscope': gyro,
                        'gyroscope_r': gyro_r,
                        'accelerometer': accel,
                        'accelerometer_raw': accel_r}}

    def test(self):
        return {'environment': {'humidity': 1.0,
                                'temperature': 2.0,
                                'temperature_h': 2.1,
                                'temperature_p': 2.2,
                                'pressure': 3},
                'imu': {'orientation_rad': 4.0,
                        'orientation_deg': 4.1,
                        'compass': 5.0,
                        'compass_r': 5.1,
                        'gyroscope': 6.0,
                        'gyroscope_r': 6.1,
                        'accelerometer': 7.0,
                        'accelerometer_raw': 7.1}}


Sensor = Hat
