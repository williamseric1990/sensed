/* i2c-m - Minimal I2C implementation
 * This library implements a generic I2C object that
 * works on the raw device. In theory, this should be
 * sufficient to support any i2c device.
 */
var fs = require('fs');
var ioctl = require('ioctl');

var I2C_SLAVE = 0x0703;

var i2cm = function(device, bus) {

	var this.fr,
		this.fw;

	this.init = function(device, bus) {
		this.fr = fs.openSync('/dev/i2c-' + device, 'rb');
		this.fw = fs.openSync('/dev/i2c-' + device, 'wb');

		this.fr = ioctl(this.fr, I2C_SLAVE, device);
		this.fw = ioctl(this.fw, I2C_SLAVE, device);
	}

	this.write = function(bytes) {
		this.fw.write(bytes);
	}

	this.read = function(length) {
		return this.fr.read(length);
	}

	this.close = function() {
		this.fw.close();
		this.fr.close();
	}

	this.init(device, bus);

};

module.exports = i2cm;