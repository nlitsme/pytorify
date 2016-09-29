"""
Unittest for torify.

The test uses a dummy socks server, so no actvie tor process is needed
"""

import unittest
import socket
import struct

try:
    # python2
    from thread import start_new_thread
except:
    # python3
    from _thread import start_new_thread

try:
    # first try the python2 module
    from urllib2 import urlopen
except:
    # then try the python3 module
    from urllib.request import urlopen


class SocksServer:
    """ A simple Socks v5 Server, which response with '<html/>' to all requests """
    NEED_MORE = 0
    NEXT_STEP = 1
    ERROR = 2
    DONE = 3

    def listen(self):
        self.svrsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.svrsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.svrsocket.listen(1)
        self.svraddr = self.svrsocket.getsockname()
        self.data = b''
        start_new_thread(self.acceptor, ())
        return self.svraddr

    def acceptor(self):
        while True:
            self.conn, addr = self.svrsocket.accept()
            #print("new conn from", addr)
            self.process = self.checkversion

            while True:
                self.read()
                #print("got data", self.data)
                while True:
                    rc = self.process()
                    if rc!=self.NEXT_STEP:
                        break
                    #print("next step", self.process)
                if rc!=self.NEED_MORE:
                    break
                #print("need more", self.process)
            #print("done")
            self.conn.close()

    def read(self):
        self.data += self.conn.recv(1024)

    def checkversion(self):
        if len(self.data)==0:
            return self.NEED_MORE
        if self.data[:1]==b'\x04':
            self.process = self.socks4request
            return self.NEXT_STEP
        elif self.data[:1]==b'\x05':
            self.process = self.socks5authlist
            return self.NEXT_STEP
        else:
            print("unknown socks version:", b2a_hex(self.data))
            return self.ERROR

    def socks4request(self):
        self.close()

    def socks5authlist(self):
        if len(self.data)<2:
            return self.NEED_MORE
        v, n = struct.unpack_from("BB", self.data, 0)
        if len(self.data)<2+n:
            return self.NEED_MORE
        methods = self.data[2:2+n]
        self.data = self.data[2+n:]

        if methods.find(b'\x00')>=0: # noauth
            self.conn.send(b'\x05\x00')
            self.process = self.socks5request
            return self.NEXT_STEP
        self.write(b'\x05\xff')
        return self.DONE

    def socks5status(self, code):
        self.conn.send(struct.pack('!BBBBLH', 5, code, 0, 1, 0, 0))

    def socks5request(self):
        if len(self.data)<8:
            return self.NEED_MORE
        v, cmd, rsv, atyp = struct.unpack_from('BBBB', self.data, 0)
        if atyp==1:  # ipv4
            if len(self.data)<10:
                return self.NEED_MORE
            addr, port = struct.unpack_from('!4sH', self.data, 4)
            self.data = self.data[6+4:]
        elif atyp==3:  # ipv4
            alen, = struct.unpack_from('B', self.data, 4)
            if len(self.data)<7+alen:
                return self.NEED_MORE
            addr, port = struct.unpack_from('!%dsH' % alen, self.data, 5)
            self.data = self.data[7+alen:]
        elif atyp==4:  # ipv6
            if len(self.data)<6+16:
                return self.NEED_MORE
            addr, port = struct.unpack_from('!16sH', self.data, 4)
            self.data = self.data[6+16:]
        else:
            self.socks5status(1)
            return self.DONE

        if cmd==1:  # connect
            self.socks5connect(addr, port)
            return self.DONE
        else:
            # unsupported: 2 = bind, 3 = udp
            self.socks5status(7)
            return self.DONE
    def socks5connect(self, addr, port):
        #print("todo: connect to ", addr, port, self.data)
        self.socks5status(0)    # always ok
        self.read()
        #print("... ", self.data)
        self.conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 7\r\n\r\n<html/>')


class TestTorify(unittest.TestCase):
    def test_torify(self):
        s5server = SocksServer()
        addr, port = s5server.listen()

        import torify
        torify.set_tor_proxy(addr, port)
        torify.disable_tor_check()    #  our socks test server does not support https yet.

        # try without tor
        response = urlopen('http://example.com')
        self.assertNotEqual(response.read(), b'<html/>')

        # try with tor
        torify.use_tor_proxy()
        response = urlopen('http://example.com')
        self.assertEqual(response.read(), b'<html/>')

