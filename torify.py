"""
Usage:

    python -mtorify tsttor.py

redirects all TCP traffic from a python application over TOR.
"""
from __future__ import print_function
import socks
import socket
import sys

try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket
socket.create_connection = create_connection

content = urlopen('https://check.torproject.org/').read()

# <h1 class="off">  - not using tor
# <h1 class="not">  - using tor without torbrowser
# <h1 class="on">  - using tor with torbrowser
if content.find(b'class="off"')!=-1:
    print("Tor NOT enabled - exiting", file=sys.stderr)
    sys.exit(1)

sys.argv = sys.argv[1:]

with open(sys.argv[0]) as f:
    code = compile(f.read(), sys.argv[0], 'exec')
    exec(code, globals(), locals())

