from socketserver import socket
import _thread
import sys
import string


class PicServ:
    def __init__(self, port):
        self.port = port
        self.serversocket = socket.socket(family=socket.AF_INET,
                                          type=socket.SOCK_STREAM)

    def start_async(self):
        _thread.start_new_thread(self.start, ())
        # self.listenThread = threading.Thread(self.start)
        # self.listenThread.start()
        # threading.Thread(self.start(port)).start()

    def start(self):
        self.serversocket.bind(('', self.port))
        self.serversocket.listen(5)

        while True:
            (clientsocket, address) = self.serversocket.accept()
            print('client accepted on port {0!s}'.format(self.port))
            clientsocket.send(bytes('<html><h1>Hello Client!</h1></html>',
                                    'utf-8'))
            clientsocket.close()
            print('removed client on port {0!s}'.format(self.port))


def main():
    for port in sys.argv[1:]:
        ps = PicServ(int(port))
        print('starting picserv instance on port {0!s}'.format(port))
        ps.start_async()
    input()


if __name__ == "__main__":
    main()
