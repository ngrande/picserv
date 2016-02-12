#!/usr/bin/env python3

from socketserver import socket
import _thread
import sys
import os
import string
import time


class PicServ:
    def __init__(self, port, data_path):
        self.port = port
        self.data_path = data_path
        self.serversocket = socket.socket(family=socket.AF_INET,
                                          type=socket.SOCK_STREAM)

    def start_async(self):
        _thread.start_new_thread(self.start, ())

    def start(self):
        self.serversocket.bind(('', self.port))
        self.serversocket.listen(5)
        while True:
            (clientsocket, address) = self.serversocket.accept()
            _thread.start_new_thread(self._send, (clientsocket,))

    def _send(self, socket):
            print('client accepted on port {0!s}'.format(self.port))
            with open(self.data_path, 'rb') as f:

                # content = f.read()
                contentsize = os.path.getsize(self.data_path)
                # content = f.read()
                # contentsize = len(content)
                # socket.send(bytes('HTTP/1.1 200 OK', 'utf-8'))
                # socket.send(bytes('Content-type: image/gif;', 'utf-8'))
                #                         'charset=utf-8', 'utf-8'))
                # socket.send(bytes('Accept-ranges: bytes', 'utf-8'))
                # socket.send(bytes('Content-length: {0!s}'
                #                   .format(contentsize), 'utf-8'))
                # totalsent = 0
                # while totalsent < contentsize:
                socket.sendfile(f)
                #   if sent == 0:
                #       print('Client closed connection')
                #   totalsent += sent
            time.sleep(0.01)  # workaround... TODO: find better solution
            socket.close()
            print('removed client on port {0!s}'.format(self.port))


def main():
    for port in sys.argv[2:]:
        ps = PicServ(int(port), sys.argv[1])
        print('starting picserv instance on port {0!s}'.format(port))
        ps.start_async()
    input()


if __name__ == "__main__":
    main()
