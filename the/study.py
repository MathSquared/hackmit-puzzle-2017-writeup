#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import code

from base import *


UNCOVER_LIST = ('bob', 'you', 'was', 'can', 'not', 'way', 'slip', 'oh', 'ever', 'isnt', 'what', 'how', 'sponsoring', 'um', 'want', 'worry', 'embarrassment', 'or', 'deloreon', 'down', 'disintegrate', 'readout')


def get_pairs(host, guests):
    res = []
    for guest in guests:
        placed = place_in_all(host, guest)
        for i, diff in enumerate(placed):
            if diff:
                res += [tuple([host[i], guest] + list(entry)) for entry in diff]
    return res


def format_pairs(pairs):
    res = []
    for hw,gw,i,hc,gc in pairs:
        res.append('%3d %s %s' % (i, hc, hw))
        res.append('%3d %s %s' % (i, gc, gw))
    return res


def attempt_uncover(word, basis=UNCOVER_LIST, lower=0):
    for i in range(lower, len(basis) + 1):
        query = basis[:i] + (word,)
        outp = decode_of(*query)[0]
        if outp:
            return i, outp[i]
    else:
        return None, None


def attempt_uncover_all(words, basis=UNCOVER_LIST, lower=0):
    found = set()
    our_basis = basis
    res = []
    # Keep going until we can't anymore
    for _ in range(len(words)):
        for word in words:
            if word not in found:
                idx, ch = attempt_uncover(word, our_basis, lower)
                if idx is not None:
                    print '%3d %s %s' % (idx, ch, word)
                    found.add(word)
                    our_basis += (word,)
                    res.append((word, idx, ch))
                    break
                else:
                    print '--- - %s' % word
        else:  # no more
            return res
    return res, tuple(our_basis)


def main():
    code.interact(local=globals())


if __name__ == '__main__':
    main()
