#!/usr/bin/env python3

from socketserver import socket
import _thread
import sys
import os
import string
import time
import re


class PicServ:
    """ Simple webserver script to handle GET reqeusts """
    def __init__(self, port, rootpath):
        self.rootpath = rootpath  # './webres'
        self.port = port
        self.serversocket = socket.socket(family=socket.AF_INET,
                                          type=socket.SOCK_STREAM)

    def start_async(self):
        _thread.start_new_thread(self.start, ())

    def start(self):
        print('PicServ instance started on port {0!s}'.format(self.port))
        self.serversocket.bind(('', self.port))
        self.serversocket.listen(5)
        while True:
            (clientsocket, address) = self.serversocket.accept()
            print('client connected on port {0!s}, starting new thread'
                  .format(self.port))
            _thread.start_new_thread(self._process_request, (clientsocket,
                                                             address))

    def _process_request(self, socket, address):
        print('client connected on {0!s}:{1!s}'.format(address, self.port))
        msg = self._receive_msg(socket).decode('utf-8')
        print('message received:')
        print(msg)
        if msg[:3] == 'GET':
            # send requested resource to client
            # get requested resource path from msg
            print('GET request received')
            reqsrcpath = self._get_path(msg)
            if self._exists_resource(reqsrcpath) or reqsrcpath == '/':
                print('requested resource:')
                print(reqsrcpath)
                fbytes = self._get_res_file_bytes(reqsrcpath)
                self._send(socket, fbytes)
        # else:
            # not yet supported
        socket.close()

    def _get_path(self, msg):
        msgparts = re.findall('[^ ]*', msg)
        fmsgparts = []
        for s in msgparts:
            if len(s) > 0:
                fmsgparts.append(s)
        if len(fmsgparts) >= 3:
            return fmsgparts[1]
        else:
            print('unable to read message')

    def _exists_resource(self, path):
        completepath = self.rootpath + path
        return os.path.isfile(completepath)

    def _get_res_file_bytes(self, path):
        fbytes = None
        if path == '/':
            path = '/index.html'
        with open(self.rootpath + path, 'rb') as f:
            fbytes = f.read()
        return fbytes

    def _receive_msg(self, socket):
        # recvbytes = []
        # recv = [0]
        # while len(recv) != 0 and recv != 0:
        recv = socket.recv(2048)  # TODO: find a way to be sure that all bytes
        #                                 were received
        #   print(recv)
        #   recvbytes += recv
        # print('msg completely received')
        return recv

    def _send(self, socket, data):
            datasize = len(data)
            totalsent = 0
            while totalsent < datasize:
                sent = socket.send(data[totalsent:])
                if sent == 0:
                    print('Client closed connection')
                totalsent += sent
            print('removed client on port {0!s}'.format(self.port))


def main():
    if len(sys.argv) < 3:
        print('At least 2 arguments were expected: root_path and port')
    for port in sys.argv[2:]:
        ps = PicServ(int(port), sys.argv[1])
        ps.start_async()
    input()


if __name__ == "__main__":
    main()
