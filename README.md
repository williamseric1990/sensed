# sensed

[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

`sensed` is a sensor network daemon that acts as a provider for sensor and node data. Uses a simple protocol based around [MessagePack](http://msgpack.org/).

### What is this thing?

Please the [the wiki article](https://github.com/sli/sensed/wiki/What-is-sensed%3F) on the subject.


### How do I install this thing?

    $ sudo apt-get install git python3 python3-pip
    $ git clone http://github.com/sli/sensed.git
    $ cd sensed/
    $ sudo pip3 -r requirements.txt

`sensed` is now ready to use.

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

Next, you'll probably want to take a look at the [example config file](https://github.com/sli/sensed/blob/python/config/config.sample.json). As you'll no doubt notice, a configuration file is not required.

If you're looking for a reference server implementation (there is no "standard" server for `sensed` &mdash; that would all but defeat part the purpose of using `sensed`), you might look into [senselog](https://github.com/sli/senselog).

### Testing mode?

Testing mode simply tells `sensed` to send preconfigured test data from the sensor modules rather than query real sensors. Perhaps surprisingly, this allows you to test your sensor network infrastructure and your `senselog` implementation before deployment.

### License

Distributed under the MIT License (MIT). See `LICENSE` for details.
