var Gpio = require('onoff').Gpio;
var config = require('./config/config.json');
var ioClient = require('socket.io-client');

var readers = {};

var socket = ioClient.connect('http://127.0.0.1:3000/');

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

process.on('SIGINT', exit);
