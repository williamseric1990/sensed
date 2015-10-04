var ADC = require('adc-pi-gpio');

var cfg = {
    tolerance: 2,
    interval: 300,
    channels: [0],
    SPICLK: 12,
    SPIMISO: 16,
    SPIMOSI: 18,
    SPICS: 22
}

var adc = new ADC(cfg);

var address = 'adc.0'
var type = 'audio';
var realtime = true;

var get = function() {
    var val = 0;
    adc.read(0, function(data) {
        val = data;
    });
    
    return val;
}

var destroy = function() {
    adc.close();
}

module.exports = { get: get, destroy: destroy, address: address, type: type, realtime: realtime };
