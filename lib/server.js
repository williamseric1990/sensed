var http = require('http').Server(null);
var io = require('socket.io').Server(http);
var config = require('../config/config.json');

var DEBUG = function(message) {
    if (config.debug) {
        console.log(message);
    }
}

var server = function() {
    io.on('connection', function(socket) {

        DEBUG('-> client connected');

        /* Prototype feedback feature - customize at will */
        socket.on('feedback', function(value) {
            if (value) {
                DEBUG('on');
            } else {
                DEBUG('off');
            }
        });

        /* Data is discarded - placeholder for future features */
        socket.on('sensor-data', function(data) {
            DEBUG(data);
        });

        /* Data is discarded - placeholder for future features */
        socket.on('node-data', function(data) {
            DEBUG(data);
        });

        /* Data is discarded - placeholder for future features */
        socket.on('all-data', function(data) {
            DEBUG(data);
        });

    });

    http.listen(3000, function() {
        DEBUG('sensed server ready');
    });
}

module.export = server;
