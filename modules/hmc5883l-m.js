var i2c = require('i2c-bus');

var address = 0x1e;
var type = 'magnetometer';
var wire = new i2c.openSync(1);

var scale = 0.92;
var xOffset = -10;
var yOffset = 10;

var readWord = function(cmd) {
    var high = wire.readByteSync(address, cmd);
    var low = wire.readByteSync(address, cmd+1);

    return (high << 8) + low;
}

var readSensor = function(cmd) {
    var val = readWord(cmd);
    if (val >= 0x8000) {
        return -((65535 - val) + 1);
    } else {
        return val;
    }
}

var get = function() {
    try {
        wire.writeByteSync(address, 0, 0b01110000);
        wire.writeByteSync(address, 1, 0b00100000);
        wire.writeByteSync(address, 2, 0b00000000);
    } catch (e) {
        return null;
    }

    var xOut = (readWord(3) - xOffset) * scale;
    var yOut = (readWord(7) - yOffset) * scale;
    var zOut = readWord(5) * scale;

    return {x: xOut, y: yOut, z: zOut};

module.exports = { get: get, address: address, type: type };
