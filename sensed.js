var config = require('./config/config.json')

var DEBUG = function (message) {
  if (config.debug == true) {
    console.log(message)
  }
}

if (config.client) {
  require('./lib/client')()
}

if (config.server) {
  require('./lib/server')()
}
