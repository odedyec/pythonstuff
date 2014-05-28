
import socket, select, sys


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


class TCPClient:

    def __init__(self):
        self._host = "localhost"
        self._port = 5000
        self._s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._s.settimeout(2)

    def connect_to_port(self, host="localhost", port=5000):
        self._host = host
        self._port = port
        try:
            self._s.connect((self._host, self._port))
            return 1
        except:
            print "Unable to connect"
            return 0

    def kill_port(self):
        self._s.close()

    def read_socket(self):
        socket_list = [sys.stdin, self._s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list,[],[])
        for sock in read_sockets:
            if sock == self._s:
                data = sock.recv(4096)
                if not data:
                    print '\nDisconnected from chat server'
                    return 0

                else:
                    sys.stdout.write(data)
                    prompt()
            else:
                msg = sys.stdin.readline()
                if msg[0] == 'k' and msg[1] == '\n':
                    return 0
                self.send_msg(msg)
        return 1

    def send_msg(self,msg):
        self._s.send(msg)
        prompt()




import string,sys


if __name__ == "__main__":
    client = TCPClient()
    client.connect_to_port()

    while 1:
        if not client.read_socket():
            break
    print "Closing port "
    client.kill_port()
    print "port closed"