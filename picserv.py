#!/usr/bin/env python3

from socketserver import socket
import _thread
import sys
import os
import string


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
            print('client accepted on port {0!s}'.format(self.port))
            with open(self.data_path, 'r') as f:
                content = f.read()
                contentsize = len(content)
                clientsocket.send(bytes('HTTP/1.1 200 OK', 'utf-8'))
                clientsocket.send(bytes('Content-type: text/html;'
                                        'charset=utf-8', 'utf-8'))
                clientsocket.send(bytes('Accept-ranges: bytes', 'utf-8'))
                clientsocket.send(bytes('Content-length: {0!s}'
                                        .format(contentsize), 'utf-8'))
                sent = 0
                while sent < contentsize:
                    sent += clientsocket.send((bytes(content[sent:], 'utf-8')))
            clientsocket.close()
            print('removed client on port {0!s}'.format(self.port))


def main():
    for port in sys.argv[2:]:
        ps = PicServ(int(port), sys.argv[1])
        print('starting picserv instance on port {0!s}'.format(port))
        ps.start_async()
    input()


if __name__ == "__main__":
    main()
