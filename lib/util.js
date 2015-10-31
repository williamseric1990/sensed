var os = require('os')

/* getIP
 * Returns the current IP address.
 */
var getIP = function() {
  var ifaces = os.networkInterfaces()

  for (ifname in Object.keys(ifaces)) {
    ifname = Object.keys(ifaces)[ifname]

    for (iface in ifaces[ifname]) {
      iface = ifaces[ifname][iface]

      if (iface.internal === true) continue

      return iface.address
    }
  }
}

/* getHostname
 * Returns the current hostname.
 */
var getHostname = function() {
  return os.hostname()
}

module.exports = { getIP: getIP, getHostname: getHostname }
