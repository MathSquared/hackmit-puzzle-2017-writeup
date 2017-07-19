#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import sys

import requests


def decode(inp):
    payload = {'username': 'MathSquared', 'codeword': inp}
    r = requests.post('https://the.delorean.codes/api/decode', payload)
    rj = r.json()
    return rj['message'], rj['message_bits'], rj['answer'], rj['well_formed']


def decode_of(*args):
    return decode(' '.join(args))


def main():
    inp = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else raw_input()
    msg = decode(inp)
    print msg[0] or '--'

if __name__ == '__main__':
    main()
