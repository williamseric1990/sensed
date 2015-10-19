var ioClient = require('socket.io-client')
var util = require('./util')
var config = require('../config/config.json')
var readers = {}

// Connect to all configured hosts
var sockets = []
for (h in config.hosts) {
  h = config.hosts[h]
  var s = ioClient.connect('http://' + h + '/')
  s.emit('identify', 'client')
  sockets[sockets.length] = s
}

var DEBUG = function (message) {
  if (config.debug) {
    console.log(message)
  }
}

/* Load sensor reading modules into a single object for traversable
 * sensor data collection.
 */
for (s in config.sensors) {
  if (config.sensors[s].enabled) {
    readers[s] = require('../modules/' + s)
    DEBUG('Loaded: ' + s + '.js')
  }
}

/* nodeData operates as a singleton */
var nodeData = null

/* getNodeData
 * Collects data about the node's platform. Operates as a singleton
 * and is only run once at daemon start.
 */
var getNodeData = function () {
  if (!nodeData) {
    nodeData = {name: config.name, ip: util.getIP(), hostname: util.getHostname()}
  }

  return nodeData
}

/* getSensorData
 * Collects current sensor data. Can be run on-demand or on a
 * timer.
 */
var getSensorData = function () {
  var ret = {}
  for (r in readers) {
    var s = readers[r]
    ret[s.type] = s.get()
  }
  return ret
}

var combineData = function (node, sensors) {
  var ret = node
  ret.sensors = sensors
  ret.timestamp = Math.floor(new Date() / 1000) // unix timestamp
  return ret
}

var client = function () {
  for (s in sockets) {
    var socket = sockets[s]

    /* sensors signal
     * Emits an object containing only sensor data to the
     * server (probably senselog, could be another node)
     */
    socket.on('sensors', function () {
      var sensors = getSensorData()
      DEBUG('<- sending sensor data to server ' + socket.id)
      socket.emit('sensor-data', combineData({}, sensors))
    })

    /* node signal
     * Emits an object containing only node data to the
     * server (probably senselog, could be another node)
     */
    socket.on('node', function () {
      var node = getNodeData()
      socket.emit('node-data', combineData(node, {}))
    })

    /* all signal
     * Emits an object containing node and sensor data to
     * the server (probably senselog, could be another node)
     */
    socket.on('all', function () {
      var sensors = getSensorData()
      DEBUG('<- sensor data: ' + JSON.stringify(sensors))
      socket.emit('all-data', combineData(nodeData, sensors))
    })
  }
}

getNodeData() // populate nodedata on start

DEBUG('sensed client ready')

module.exports = client
