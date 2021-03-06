"""
A simple test of our current TOR enabled status.

compare the output of:

    python tsttor.py

and

    python -mtorify tsttor.py

and not the printed `torstatus`
 * `not` means the connection is over TOR, but does not use torbrowser
 * `off` means the connection did not use TOR

"""
from __future__ import print_function
import sys
import argparse
import re
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

print("argv", sys.argv)
print("name", __name__)
content = urlopen('https://check.torproject.org/').read()
m = re.search(b'<h1 class="(\w+)">', content)
if m:
    print("torstatus: ", m.group(1))
else:
    print("failed to check tor status")

# <h1 class="off">  - not using tor
# <h1 class="not">  - using tor without torbrowser
# <h1 class="on">  - using tor with torbrowser

