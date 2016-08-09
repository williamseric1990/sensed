![sensed](https://raw.githubusercontent.com/sli/sensed/gh-pages/logo.png)

[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/) [![Build Status](https://travis-ci.org/sli/sensed.svg?branch=python-module)](https://travis-ci.org/sli/sensed) [![codecov](https://codecov.io/gh/sli/sensed/branch/master/graph/badge.svg)](https://codecov.io/gh/sli/sensed)

`sensed` is a sensor network daemon that acts as a provider for sensor and node data. Uses a simple protocol based around [MessagePack](http://msgpack.org/).

### What is this thing?

Please the [the wiki article](https://github.com/sli/sensed/wiki/What-is-sensed%3F) on the subject.

### Requirements

As `sensed` makes use of the typing module, Python 3.5 or newer is required. Beyond that, all dependencies are in the included `requirements.txt` file.

### How do I install this thing?

    $ sudo pip3 install sensed

### How do I use this thing?

First, see the `--help` output:

    $ python3 sensed.py --help
    Usage: sensed.py [OPTIONS]

    Options:
      -c, --config TEXT   Configuration file for this instance.
      -n, --name TEXT     Name of his sensed instance. Default: sensed
      -S, --sensors TEXT  Sensor modules to load and enable.
      -i, --host TEXT     IP or hostname to bind to. Default: 0.0.0.0
      -p, --port INTEGER  Port to bind to. Default: 3000
      -V, --verbose       Enable verbose output (debugging)
      -t, --test          Enable test mode.
      --help              Show this message and exit.

Next, you'll probably want to take a look at the [example config file](https://github.com/sli/sensed/blob/python-module/docs/config.sample.json). As you'll no doubt notice, a configuration file is not required.

The client library is included in this version of `sensed`.

### Testing mode?

Testing mode simply tells `sensed` to send preconfigured test data from the sensor modules rather than query real sensors. Perhaps surprisingly, this allows you to test your sensor network infrastructure and your `senselog` implementation before deployment.

### License

Distributed under the MIT License (MIT). See `LICENSE` for details.
