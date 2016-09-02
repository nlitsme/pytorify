# pytorify

Module which makes sure all sockets use the TOR proxy at port 9050

This module works with both python2 and python3.

When using this module:
 * Name lookups are blocked.
 * No UDP traffic is possible.
 * All TCP traffic is redirected through tor.

## Requirements

 * PySocks
 * TOR, with socks5 proxy at localhost, port 9050

## Usage

`torify` can be used either in two ways, either loaded from the
python commandline using the `-m` switch. Or as a imported module.


### From the commandline:

    python -mtorify [options] yourmodule.py [...with args...]

Several options can be passed to `torify`:

    --proxy PROXY, -p PROXY   Where to find the TOR socks5 proxy
    --nocheck, -n             Skip TOR connection check

By default `torify` uses 127.0.0.1:9050 as the socks proxy for TOR.


### As a module

    import torify
    torify.use_tor_proxy()

optionally you can call these function to configure the tor proxy.

    torify.set_tor_proxy("127.0.0.1", 9150) # use tor from TorBrowser
    torify.disable_tor_check()


## TODO

 * instead of blocking name lookups, resolve names using socks namelookup.


## AUTHOR

Willem Hengeveld <itsme@xs4all.nl>
