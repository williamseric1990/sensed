var config = require('./config/config.json');

if (config.client) {
	var Gpio = require('onoff').Gpio;
	var ioClient = require('socket.io-client');

	var readers = {};
	var socket = ioClient.connect('http://' + config.host + '/');

	/* Load sensor reading modules */
	for (s in config.sensors) {
		s = config.sensors[s];
		readers[s] = require('./modules/' + s);
	}

	var button = new Gpio(23, 'in', 'both');

	var exit = function() {
	    console.log('cleaning up...')
	    button.unexport();
	    process.exit();
	}

	console.log('ready');

	button.watch(function(err, value) {
	    if (err) {
	        console.log(err);
	    }

	    console.log('button toggled, ' + value);
	    led.writeSync(value);
	    socket.emit('feedback', value);
	});

	socket.on('sensors', function() {
	    var ret = {};
	    for (r in readers) {
	        var s = readers[r];
	        ret[s.type] = s.get();
	    }
	    console.log('Sending sensor data to client ' + socket.id);
	    socket.emit('sensor-data', ret);
	});

	process.on('SIGINT', exit);
}

if (config.server) {
	var http = require('http').Server(null);
	var io = require('socket.io').Server(http);

	io.on('connection', function(socket) {

	    console.log('-> client connected');

	    socket.on('feedback', function(value) {
	        if (value) {
	            console.log('<- pressed');
	            socket.emit('sensors');
	        } else {
	            console.log('<- released');
	        }
	    });

	    socket.on('sensor-data', function(data) {
	        console.log(data);
	    });

	});

	http.listen(3000, function() {
	    console.log('ready');
	});
}
