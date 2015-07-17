var ioClient = require('socket.io-client');
var config = require('../config/config.json');
var socket = ioClient.connect('http://' + config.host + '/');
var readers = {};

/* Load sensor reading modules */
for (s in config.sensors) {
    s = config.sensors[s];
    readers[s] = require('../modules/' + s);
}

/* nodeData operates as a singleton */
var nodeData = null;

var getNodeData = function() {
    if (!nodeData) {
        // TODO: construct nodeData object
        nodeData = {};
    }

    return nodeData;
}

var getSensorData = function() {
    var ret = {};
    for (r in readers) {
        var s = readers[r];
        ret[s.type] = s.get();
    }
}

var client = function() {
    socket.on('sensors', function() {
        var ret = getSensorData();
        console.log('Sending sensor data to server ' + socket.id);
        socket.emit('sensor-data', {sensors: ret});
    });

    socket.on('node', function() {
        socket.emit('node-data', getNodeData());
    });

    socket.on('all', function() {
        var ret = getNodeData();
        ret.sensors = getSensorData();
        socket.emit('all-data', ret);
    });
}

module.exports = client;