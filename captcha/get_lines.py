#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name,no-member

import os

import numpy as np
import scipy
from scipy import misc

import decipher


def main():
    ls = os.listdir('samples')
    acc = np.zeros((50, 100)).astype('int') + 1
    for path in ls[0:100]:
        im = decipher.threshold(scipy.misc.imread('samples/' + path))
        acc *= im / 255
    scipy.misc.imsave('lines.png', acc)
    np.save('lines.npy', acc)

    np.set_printoptions(threshold='nan')
    with open('lines.py', 'w') as fout:
        print >>fout, 'import numpy as np'
        print >>fout, 'lines = np.\\'
        print >>fout, repr(acc).replace('uint8', 'np.uint8')


if __name__ == '__main__':
    main()
