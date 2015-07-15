var i2c = require('i2c-bus');

var address = 0x1d;
var type = 'humidity';

var get = function() {
	return 0;
}

module.exports = { get: get, address: address, type: type };
