var http = require('http').Server(null);
var io = require('socket.io').Server(http);
var config = require('../config/config.json');

var server = function() {
    io.on('connection', function(socket) {

        console.log('-> client connected');

        /* Prototype feedback feature - customize at will */
        socket.on('feedback', function(value) {
            if (value) {
                console.log('<- pressed');
                socket.emit('sensors');
            } else {
                console.log('<- released');
            }
        });

        /* Data is discarded - placeholder for future features */
        socket.on('sensor-data', function(data) {
            console.log(data);
        });

        /* Data is discarded - placeholder for future features */
        socket.on('node-data', function(data) {
        	console.log(data);
        });

        /* Data is discarded - placeholder for future features */
        socket.on('all-data', function(data) {
        	console.log(data);
        });

    });

    http.listen(3000, function() {
        console.log('ready');
    });
}

module.export = server;