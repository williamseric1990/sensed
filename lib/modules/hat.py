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


Sensor = Hat
