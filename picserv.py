#!/usr/bin/env python3

from socketserver import socket
import _thread
import sys
import os
import string
import time
import re
import ssl


class PicServ:
    """ Simple webserver script to handle GET requests """
    def __init__(self, addr, port, root_path):
        self.root_path = root_path  # './webres'
        self.port = port
        self.addr = addr
        self.server_socket = socket.socket(family=socket.AF_INET,
                                           type=socket.SOCK_STREAM)
        # TODO: implement TLS
        # SSLContext.wrap_socket()
        # ssl.wrap_socket(self.server_socket, keyfile, certfile)

    def start_async(self):
        _thread.start_new_thread(self.start, ())

    def stop(self):
        self.active = False
        self.server_socket.close()

    def start(self):
        self.server_socket.bind((self.addr, self.port))
        self.server_socket.listen(5)
        self.active = True
        print('PicServ instance started on  {0!s}:{1!s}'.format(self.addr,
                                                                self.port))
        try:
            while self.active:
                (client_socket, address) = self.server_socket.accept()
                print('client connected on port {0!s}, starting new thread'
                      .format(self.port))
                _thread.start_new_thread(self._process_request, (client_socket,
                                                                 address))
        finally:
            self.server_socket.close()

    def _process_request(self, socket, address):
        print('client connected on {0!s}:{1!s}'.format(address, self.port))
        try:
            # TODO: get rid of the decode - just use the plain bytes
            # to prevent decoding errors
            msg = self._receive_msg(socket).decode('utf-8')
            print('message received:')
            print(msg)
            if msg[:3] == 'GET':
                # send requested resource to client
                # get requested resource path from msg
                print('GET request received')
                req_source_path = self._get_path(msg)
                if (self._exists_resource(req_source_path) or
                        req_source_path == '/'):
                    print('requested resource:')
                    print(req_source_path)
                    file_bytes = self._get_res_file_bytes(req_source_path)
                    self._send(socket, file_bytes)
            # else:
                # not yet supported
        finally:  # be sure to close the socket
            socket.close()

    def _get_path(self, msg):
        msg_parts = re.findall('[^ ]*', msg)
        filtered_msg_parts = []
        for s in msg_parts:
            if len(s) > 0:
                filtered_msg_parts.append(s)
        if len(filtered_msg_parts) >= 3:
            return filtered_msg_parts[1]
        else:
            print('unable to read message')

    def _exists_resource(self, path):
        complete_path = self.root_path + path
        return os.path.isfile(complete_path)

    def _get_res_file_bytes(self, path):
        file_bytes = None
        if path == '/':
            path = '/index.html'
        with open(self.root_path + path, 'rb') as f:
            file_bytes = f.read()
        return file_bytes

    def _receive_msg(self, socket):
        # recvbytes = []
        # recv = [0]
        # while len(recv) != 0 and recv != 0:
        # TODO: check if there is a message to be received by the host...
        # else the server will wait forever
        recv = socket.recv(4096)  # TODO: find a way to be sure that all bytes
        #                                 were received
        #   print(recv)
        #   recvbytes += recv
        # print('msg completely received')
        return recv

    def _send(self, socket, msg_bytes):
            msg_size = len(msg_bytes)

            totalsent = 0
            while totalsent < msg_size:
                sent = socket.send(msg_bytes[totalsent:])
                if sent == 0:
                    print('Client closed connection')
                totalsent += sent
            print('removed client on port {0!s}'.format(self.port))


def main():
    addr = ''
    root_path = ''
    ports = []

    if (len(sys.argv) == 1):
        addr = socket.gethostname()
        root_path = './webres'
        ports.append(80)
    elif len(sys.argv) < 4:
        print('At least 3 arguments were expected: root_path, addr and port')
    else:
        addr = sys.argv[2]
        root_path = sys.argv[1]
        ports = sys.argv[3:]
    servers = []
    try:
        for port in ports:
            ps = PicServ(addr, int(port), root_path)
            ps.start_async()
            servers.append(ps)
        input()
    finally:  # be sure to stop the servers
        for s in servers:
            s.stop()


if __name__ == "__main__":
    main()
