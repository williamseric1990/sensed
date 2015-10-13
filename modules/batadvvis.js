var SSH = require('simple-ssh')
var config = require('../config/config.json').batadvvis

var type = 'batadv-vis'

var get = function () {
  var meshMap

  var ssh = new SSH({
    host: config.host,
    user: config.user,
    password: config.password
  })

  ssh.exec('batadv-vis -f json', {
    out: function (stdout) {
      stdout = stdout.split('\n')
      delete stdout[stdout.length - 1]

      var meshMap = []

      for (line in stdout) {
        line = stdout[line]
        meshMap[meshMap.length] = JSON.parse(line)
      }
    }
  }).start()

  return meshMap
}

module.export = { get: get, type: type }
