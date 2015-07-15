var http = require('http').Server(null);
var io = require('socket.io').Server(http);

var config = require('../config/config.json');

var client = function() {
    io.on('connection', function(socket) {

        console.log('-> client connected');

        socket.on('feedback', function(value) {
            if (value) {
                console.log('<- pressed');
                socket.emit('sensors');
            } else {
                console.log('<- released');
            }
        });

        socket.on('sensor-data', function(data) {
            console.log(data);
        });

    });

    http.listen(3000, function() {
        console.log('ready');
    });
}

module.export = client;