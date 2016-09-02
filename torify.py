"""
Redirects all TCP traffic from a python application over TOR.

Usage:

    python -mtorify [options] tsttor.py [...]

options:

    --proxy PROXY, -p PROXY   Where to find the TOR socks5 proxy
    --nocheck, -n             Skip TOR connection check


Use as module
=============

    import torify

    torify.set_tor_proxy("127.0.0.1", 9150) # use tor from TorBrowser
    torify.use_tor_proxy()


"""
from __future__ import print_function
import socks
import socket
import sys

try:
    # first try the python2 module
    from urllib2 import urlopen
except:
    # then try the python3 module
    from urllib.request import urlopen

need_check = True

def set_tor_proxy(addr, port):
    socks.setdefaultproxy(socks.SOCKS5, addr, port)

def disable_tor_check():
    global need_check
    need_check = False

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

# todo: implement real socks resolve request.
# for now just fail
def sockshostbyname(host):
    raise socket.gaierror(socket.EAI_NONAME, 'nodename nor servname provided, or not known')
def sockshostbyname_ex(host):
    raise socket.gaierror(socket.EAI_NONAME, 'nodename nor servname provided, or not known')
def sockshostbyaddr(addr):
    raise socket.herror(1, "Unknown host")
def socksgetaddrinfo(*args):
    raise socket.gaierror(socket.EAI_NONAME, 'nodename nor servname provided, or not known')


def verify_tor_connection():
    """ Verify TOR connection by connecting to check.torproject.org """

    content = urlopen('https://check.torproject.org/').read()

    # <h1 class="off">  - not using tor
    # <h1 class="not">  - using tor without torbrowser
    # <h1 class="on">  - using tor with torbrowser
    return content.find(b'class="off"')==-1


def use_tor_proxy():
    """ Modify the socket mdoule to use the TOR proxy """
    if not socks.get_default_proxy():
        # when proxy was not explicitly set, use 127.0.0.1:9050
        set_tor_proxy('127.0.0.1', 9050)

    socket.socket = socks.socksocket
    socket.gethostbyname = sockshostbyname
    socket.gethostbyaddr = sockshostbyaddr
    socket.gethostbyname_ex = sockshostbyname_ex
    socket.getaddrinfo = socksgetaddrinfo
    socket.create_connection = create_connection
    # getfqdn  uses gethostbyaddr 

    # Now all relevant functions are replaced with torified versions
    # lets test the connection.

    if need_check and not verify_tor_connection():
        print("Tor NOT enabled - exiting", file=sys.stderr)
        sys.exit(1)


if __name__=="__main__":
    # this module was loaded using the `-m` switch, exec the first argument
    import argparse
    parser = argparse.ArgumentParser(description='python torifier')
    parser.add_argument('--proxy', '-p', type=str, help='Where to find the TOR socks5 proxy')
    parser.add_argument('--nocheck', '-n', action='store_true', help='Skip TOR connection check')
    parser.add_argument('ARGV', type=str, nargs=argparse.REMAINDER, help='The python script with arguments which should be torified')
    args = parser.parse_args()

    if args.proxy:
        addr, port = args.proxy.split(':',1)
        set_tor_proxy(addr, int(port))
    if args.nocheck:
        disable_tor_check()

    use_tor_proxy()

    sys.argv = args.ARGV

    with open(sys.argv[0]) as f:
        code = compile(f.read(), sys.argv[0], 'exec')
        exec(code, globals(), locals())

