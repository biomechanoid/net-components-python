#!/usr/bin/env python

import argparse
import socket


def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError(
                'was expecting %d bytes but only received %d bytes before the socket closed' % (length, len(data)))
        data += more
    return data
    

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    sock.sendall(b'Hi there, server')
    reply = recvall(sock, 16)
    print('The server said', repr(reply))
    sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=8080, help='TCP port (default 8080)')
    args = parser.parse_args()
    client(args.host, args.p)


