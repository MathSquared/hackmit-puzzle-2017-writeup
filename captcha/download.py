#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import code
import os
import sys

import base64
import requests


def download():
    r = requests.get('https://captcha.delorean.codes/u/MathSquared/challenge')
    return r.json()['images']


def to_dict(images):
    res = {}
    for image in images:
        name, b64 = image['name'], image['jpg_base64']
        jpg = base64.b64decode(b64)
        res[name] = jpg
    return res


def write(name, dat):
    with open(name, 'wb') as fimg:
        fimg.write(dat)


def write_name(imgs, name, base=None):
    base = base or os.getcwd()
    write(os.path.join(base, name + '.jpg') if base else name + '.jpg', imgs[name])


def write_all(imgs, base=None):
    for name, jpg in imgs.iteritems():
        write(os.path.join(base, name + '.jpg') if base else name + '.jpg', jpg)


def main():
    dirout = sys.argv[1] if len(sys.argv) > 1 else None
    imgs = to_dict(download())

    if dirout:
        write_all(imgs, dirout)
    else:
        print 'imgs'
        print 'write(name, dat)'
        print 'write_name(imgs, name, base=None)'
        print 'place_name(name, base=None)'
        print 'write_all(base=None)'
        print 'place_all(imgs, base=None)'
        print
        print 'Have fun!'
        print

        code.interact(local={
            'imgs': imgs,
            'write': write,
            'write_name': write_name,
            'place_name': lambda name, base: write_name(imgs, name, base),
            'write_all': write_all,
            'place_all': lambda base: write_all(imgs, base),
        })


if __name__ == '__main__':
    main()
