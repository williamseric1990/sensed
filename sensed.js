var config = require('./config/config.json');

if (config.client) {
    require('./lib/client')();
}

if (config.server) {
    require('./lib/server')();
}
