#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import code
import json

import h5py


mj = json.load(open('model.json'))

mh = h5py.File('model.hdf5', 'r')


def main():
    code.interact(local=globals())


if __name__ == '__main__':
    main()
