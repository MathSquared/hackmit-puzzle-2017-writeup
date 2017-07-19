#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

from decode import decode
from decode import decode_of


codes = {x: i for i, x in enumerate('abcdefghijklmnopqrstuvwxyz ')}


def seqdiff(a, b):
    return [(i, ai, bi) for i, (ai, bi) in enumerate(zip(a, b)) if ai != bi]


def place_in_all(host, guest):
    res = []
    orig = decode_of(*host)[0]
    if not orig:
        return None
    for i in range(len(host)):
        adapt = host[:]
        adapt[i] = guest
        new = decode_of(*adapt)[0]
        res.append(new and seqdiff(orig, new))
    return res


def codify(word):
    return [codes[ch] for ch in word]
