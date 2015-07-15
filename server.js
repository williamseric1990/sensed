var http = require('http').Server(null);
var io = require('socket.io')(http);


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
        console.log(JSON.stingify(data, null, 2))
    });

});

http.listen(3000, function() {
    console.log('ready');
});
