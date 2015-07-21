var com = require('serialport');

var type = 'gps';

var parseRMC = function(rmc) {
    var ret = {};
    rmc = rmc.split(',');

    var time = parseTime(rmc[1]);
    ret.time = time;

    /* Check GPS data status.
     * A = active (good data), continue
     * V = void (invalid data), return only time
     */
    var status = rmc[2];
    if (status.toLowerCase() == 'v') {
        ret.void = true;
        return ret;
    }

    ret.void = false;

    ret.latitude = parseLatitude(data[3], data[4]);
    ret.longitude = parseLongitude(data[5], data[6]);

    ret.speed = rmc[7]; // note: speed is in knots
    ret.angle = rmc[8];

    ret.date = parseDate(rmc[9]);

    ret.checksum = rmc[rmc.length-1];

    return ret;
}

var parseTime = function(time) {
    time = time.split('.');
    var hours = time[0].substr(0, 2);
    var minutes = time[0].substr(2, 2);
    var seconds = time[0].substr(4, 2);
    var milliseconds = time[1];

    return {hours: hours, minutes: minutes, seconds: seconds, milliseconds: milliseconds};
}

var parseLatitude = function(latitude, direction) {
    var deg = latitude.substr(0, 2);
    var min = latitude.substr(2);

    return {degrees: deg, minutes: min, direction: direction};
}

var parseLongitude = function(longitude, direction) {
    var deg = longitude.substr(0, 3);
    var min = longitude.substr(3);

    return {degrees: deg, minutes: min, direction: direction};
}

var parseDate = function(date) {
    var month = date.substr(0, 2);
    var day = date.substr(2, 2);
    var year = date.substr(4);

    return {month: month, day: day, year: year};
}

var get = function() {
    /* TODO: read rmc (recommended minimum coordinates) from serial
     * RMC line header: $GPRMC
     * Discard all other lines
     */

    var ret = parseRMC(rmc);
    return ret;
}

module.exports = {get: get, type: type, address: null};