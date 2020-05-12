#!/usr/bin/env python

import argparse
import random
import socket
import sys

MAX_BYTES = 65535


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening socket at', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        rand = random.random()
        print(rand)
        if rand < 0.4:
            print('Pretending to drop packet from {}'.format(address))
            continue
        text = data.decode('ascii')
        print('The client at {} says {!r}', address, text)
        message = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(message.encode('ascii'), address)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                                 ' pretending packets are often dropped')
    parser.add_argument('host', help='interface the server listens at;'
                                     'host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=8080,
                        help='UDP port (default 8080)')
    args = parser.parse_args()
    server(args.host, args.p)

