var Gpio = require('onoff').Gpio;
var config = require('./config/config.json');
var ioClient = require('socket.io-client');

var readers = {};

var socket = ioClient.connect('http://192.168.1.101:3000/');

/* Load sensor reading modules */
for (s in config.sensors) {
	s = config.sensors[s];
	readers[s] = require('./modules/' + s);
}

var button = new Gpio(23, 'in', 'both');
var led = new Gpio(24, 'out');

var exit = function() {
    console.log('cleaning up...')
    led.unexport();
    button.unexport();
    process.exit();
}

console.log('ready');

button.watch(function(err, value) {
    if (err) {
        console.log(err);
    }

    console.log('button toggled, ' + value);
    led.writeSync(value);
    socket.emit('feedback', value);
});

socket.on('sensors', function() {
    var ret = {};
    for (r in readers) {
        var s = readers[r];
        ret[s.type] = s.get();
    }
    console.log('Sending sensor data to client ' + socket.id);
    socket.emit('sensor-data', ret);
});

process.on('SIGINT', exit);
