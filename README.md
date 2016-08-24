# pytorify
module which makes sure all sockets use the TOR proxy at port 9050

Requirements
============

 * PySocks
 * TOR, with socks5 proxy at localhost, port 9050

Usage
=====

python -mtorify yourmodule.py --with args

Works with python2 and python3.

TODO
====

 * block UDP traffic.
 * redirect name lookups.
