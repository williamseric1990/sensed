var ioClient = require('socket.io-client')
var config = require('../config/config.json')
var readers = {}

// Connect to all configured hosts
var sockets = []
for (h in config.hosts) {
  h = config.hosts[h]
  sockets[sockets.length] = ioClient.connect('http://' + h + '/')
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
    // TODO: construct nodeData object
    nodeData = {name: config.name}
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

var emitToAll = function (event, data) {
  for (s in sockets) {
    sockets[s].emit(event, data)
  }
}

var client = function () {
  /* sensors signal
   * Emits an object containing only sensor data to the
   * server (probably senselog, could be another node)
   */
  socket.on('sensors', function () {
    var sensors = getSensorData()
    DEBUG('<- sending sensor data to server ' + socket.id)
    emitToAll('sensor-data', combineData({}, sensors))
  })

  /* node signal
   * Emits an object containing only node data to the
   * server (probably senselog, could be another node)
   */
  socket.on('node', function () {
    var node = getNodeData()
    emitToAll('node-data', combineData(node, {}))
  })

  /* all signal
   * Emits an object containing node and sensor data to
   * the server (probably senselog, could be another node)
   */
  socket.on('all', function () {
    var sensors = getSensorData()
    DEBUG('<- sensor data: ' + JSON.stringify(sensors))
    emitToAll('all-data', combineData(nodeData, sensors))
  })
}

getNodeData() // populate node data on start

DEBUG('sensed client ready')

module.exports = client
