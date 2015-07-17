var ioClient = require('socket.io-client');
var config = require('../config/config.json');
var socket = ioClient.connect('http://' + config.host + '/');
var readers = {};

/* Load sensor reading modules into a single object for traversable
 * sensor data collection.
 */
for (s in config.sensors) {
    s = config.sensors[s];
    readers[s] = require('../modules/' + s);
}

/* nodeData operates as a singleton */
var nodeData = null;

/* getNodeData
 * Collects data about the node's platform. Operates as a singleton
 * and is only run once at daemon start.
 */
var getNodeData = function() {
    if (!nodeData) {
        // TODO: construct nodeData object
        nodeData = {};
    }

    return nodeData;
}

/* getSensorData
 * Collects current sensor data. Can be runn on-demand or on a
 * timer.
 */
var getSensorData = function() {
    var ret = {};
    for (r in readers) {
        var s = readers[r];
        ret[s.type] = s.get();
    }
}

var client = function() {
    /* sensors signal
     * Emits an object containing only sensor data to the
     * server (probably senselog, could be another node)
     */
    socket.on('sensors', function() {
        var ret = getSensorData();
        console.log('Sending sensor data to server ' + socket.id);
        socket.emit('sensor-data', {sensors: ret});
    });


    /* node signal
     * Emits an object containing only node data to the
     * server (probably senselog, could be another node)
     */
    socket.on('node', function() {
        socket.emit('node-data', getNodeData());
    });


    /* all signal
     * Emits an object containing node and sensor data to
     * the server (probably senselog, could be another node)
     */
    socket.on('all', function() {
        var ret = getNodeData();
        ret.sensors = getSensorData();
        socket.emit('all-data', ret);
    });
}

module.exports = client;