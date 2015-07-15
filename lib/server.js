var Gpio = require('onoff').Gpio;
var ioClient = require('socket.io-client');

var config = require('../config/config.json');

var readers = {};
var socket = ioClient.connect('http://' + config.host + '/');

var server = function() {
    /* Load sensor reading modules */
    for (s in config.sensors) {
        s = config.sensors[s];
        readers[s] = require('../modules/' + s);
    }

    var button = new Gpio(23, 'in', 'both');

    var exit = function() {
        console.log('cleaning up...')
        button.unexport();
        process.exit();
    }

    console.log('ready');

    button.watch(function(err, value) {
        if (err) {
            console.log(err);
        }

        console.log('button toggled, ' + value);
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
}

module.exports = server;