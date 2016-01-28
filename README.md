# sensed

`sensed` is a sensor network daemon that acts as a provider for sensor and node data.


### How do I install this thing?

    rcm@ubuntustation1 ~> git clone http://github.com/sli/sensed.git
    rcm@ubuntustation1 ~> cd sensed/
    rcm@ubuntustation1 ~> sudo apt-get install python3-pip
    rcm@ubuntustation1 ~> sudo pip3 -r requirements.txt

`sensed` is now ready to use.

### How do I use this thing?

First, see the `--help` output:

    rcm@ubuntustation1 ~/P/lidard> python3 sensed.py --help
    Usage: sensed.py [OPTIONS]

    Options:
      -c, --config TEXT   Configuration file for this instance.
      -n, --name TEXT     Name of his sensed instance. Should be unique on the
                          network. Default: sensed
      -S, --sensors TEXT  Sensor modules to load and enable.
      -i, --host TEXT     IP or hostname of the senselog server. Default:
                          localhost
      -p, --port INTEGER  Port used by clients to recieve data. Default: 3000
      -V, --verbose       Enable verbose output (debugging)
      --help              Show this message and exit.

Next, you'll probably want to take a look at the [example config file](https://github.com/sli/sensed/blob/python/config/config.sample.json). As you'll no doubt notice, a configuration file is not required.