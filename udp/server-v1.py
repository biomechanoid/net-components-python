#!/usr/bin/env python

import argparse
import socket
from datetime import datetime
import time

MAX_BYTES = 65535

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        text = 'Your data was {} bytes long'.format(len(data))
        data = text.encode('ascii')
        if data is not None:
            time.sleep(5)
            sock.sendto(data, address)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('-p', metavar='PORT', type=int, default=8080, help='UDP port (default 1060)')
    args = parser.parse_args()
    server(args.p)