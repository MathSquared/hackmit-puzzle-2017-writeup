#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import requests

ENCODE = tuple('abcdefghijklmnopqrstuvwxyz ')


def get_script(url='http://www.scifiscripts.com/scripts/backtothefuture_transcript.txt'):
    r = requests.get(url)
    return r.text.strip()


def process_word(word):
    word = ''.join(c for c in word.lower() if c.isalpha())
    return word or None  # in case word empty


def process_script(script):
    return (process_word(word) for word in script.split())


def find_dict(words):
    cur_idx = 0
    cur_let = 0
    res = {}
    found = set()

    for word in words:
        if not word or word in found:
            continue
        found.add(word)
        if cur_let < len(ENCODE):
            res[(cur_idx, ENCODE[cur_let])] = word

        cur_let += 1
        if cur_let == 32:  # magic
            cur_let = 0
            cur_idx += 1

    return res


def main():
    res = find_dict(process_script(get_script()))
    resarr = ['%3d %s %s' % (idx, ch, word) for ((idx, ch), word) in res.iteritems()]
    resarr.sort()
    for line in resarr:
        print line.encode('utf-8')


if __name__ == '__main__':
    main()
