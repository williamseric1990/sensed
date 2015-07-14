var i2c = require('i2c');
var address = 0x1e;

var wire = new i2c(address, {device: '/dev/i2c-1'});

var scale = 0.92;
var xOffset = -10;
var yOffset = 10;

var readWord = function(adr) {
	wire.readByte(function(err, high) {
		wire.readByte(function(err, low) {
			var val = (high << 8) + low;
			return val;
		});
	});
}

var readSensor = function(adr) {
	var val = readWord(adr);
	if (val >= 0x8000) {
		return -((65535 - val) + 1);
	} else {
		return val;
	}
}

var writeByte = function(adr) {
	return; // TODO
}

var get = function() {
	wire.writeByte(0, 0b01110000);
	wire.writeByte(1, 0b00100000);
	wire.writeByte(2, 0b00000000);

	var xOut = (readWord(3) - xOffset) * scale;
	var yOut = (readWord(7) - yOffset) * scale;
	var zOut = readWord(5) * scale;

	var bearing = Math.atan2(yOut, xOut);
	if (bearing < 0) {
		bearing += 2 * Math.PI;
	}

	return bearing * (180 / Math.PI);
}

module.exports = { get: get, address: address };