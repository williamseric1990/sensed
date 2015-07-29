var i2c = require('i2c-bus');
var sleep = require('sleep');

var address = 0x60;
var type = 'barometer';
var wire = new i2c.openSync(1);

var readA0 = function() {
    var a0 = (wire.readByteSync(address, 0x04) << 8) | wire.readByteSync(address, 0x05);
    var a0d = a0;
    if (a0 & 0x8000) {
        a0d = -((~a0 & 0xffff) + 1);
    }
    var a0f = a0d / 8;
    return a0f;
};

var readB1 = function() {
    var b1 = (wire.readByteSync(address, 0x06) << 8) | wire.readByteSync(address, 0x07);
    var b1d = b1;
    if (b1 & 0x8000) {
        b1d = -((~b1 & 0xffff) + 1);
    }
    var b1f = b1d / 8192;
    return b1f;
};

var readB2 = function() {
    var b2 = (wire.readByteSync(address, 0x08) << 8) | wire.readByteSync(address, 0x09);
    var b2d = b2;
    if (b2 & 0x8000) {
        b2d = -((~b2 & 0xfff) + 1);
    }
    var b2f = b2d / 16384;
    return b2f;
};

var readC12 = function() {
    var c12 = (wire.readByteSync(address, 0x0a) << 8) | wire.readByteSync(address, 0x0b);
    var c12d = c12;
    if (c12 & 0x8000) {
        c12d = -((~c12 & 0xffff) + 1);
    }
    var c12f = c12d / 16777216;
    return c12f;
};

var readRaws = function() {
    wire.writeByteSync(address, 0x12, 0x0);
    sleep.sleep(3);

    var rawpres = (wire.readByteSync(address, 0x00) << 2) | (wire.readByteSync(address, 0x01) >> 6);
    var rawtemp = (wire.readByteSync(address, 0x02) << 2) | (wire.readByteSync(address, 0x03) >> 6);

    return {pres: rawpres, temp: rawtemp};
};

var get = function() {
    var a0f = readA0();
    var b1f = readB1();
    var b2f = readB2();
    var c12 = readC12();
    var raws = readRaws();

    var pcomp = a0f + (b1f + c12 * raws.temp) * raws.pres + b2f * raws.temp;
    var pres = pcomp / 15.737 + 50;
    var temp = 25 - (raws.temp - 498) / 5.35;

    return {pressure: pres, temperature: temp};
};

module.exports = { get: get, address: address, type: type };
