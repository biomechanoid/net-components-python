#!/usr/bin/env python

import argparse
import random
import socket
import sys

MAX_BYTES = 65535


def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    hostname = sys.argv[2]
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))
    print('peer name is {}'.format(sock.getpeername()))
    delay = 0.1  # seconds
    text = 'This is another message'
    data = text.encode('ascii')
    while True:
        sock.send(data)
        print('Waiting up to {} seconds for a reply', delay)
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
            print('here')
        except socket.timeout:
            delay *= 2  # wait even longer for the next request -> exponential back-off,
            print('increase', delay)
            if delay > 2.0:
                raise RuntimeError('I think the server is down')
        else:
            break  # we are done, and can stop looping
    print('The server says {!r}'.format(data.decode('ascii')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                                 ' pretending packets are often dropped')
    parser.add_argument('host', help='interface the server listens at;'
                                     'host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=8080,
                        help='UDP port (default 8080)')
    args = parser.parse_args()
    client(args.host, args.p)

