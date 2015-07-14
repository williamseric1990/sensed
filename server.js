var http = require('http').Server(null);
var io = require('socket.io')(http);


io.on('connection', function(socket) {

    console.log('-> client connected');

    socket.on('feedback', function(value) {
        if (value) {
            console.log('<- pressed');
        } else {
            console.log('<- released');
        }
    });

});

http.listen(3000, function() {
    console.log('ready');
});