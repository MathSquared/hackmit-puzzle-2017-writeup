#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import sys

import numpy as np
import scipy

import brain


def main():
    outname = sys.argv[1] if len(sys.argv) > 1 else 'result.png'
    fname = sys.argv[2] if len(sys.argv) > 2 else None

    model = brain.get_model()
    print 'Model initialized.'
    def fun(im):
        pred = model.predict(np.reshape(im, (1, 32, 32, 3))).flatten()
        auto = pred[1]
        amax = np.argmax(pred)
        return -auto - (1 if amax == 1 else 0)
    def cb(x, f, accept):
        # stop early if we find something that wins
        return f <= -1
    def ts(x):
        # pick a random coord and twiddle it
        idx = np.random.randint(3072)
        xx = x[idx]
        lo = xx - np.random.randint(min(16, xx) + 1)
        up = xx + np.random.randint(min(16, 255-xx) + 1)
        x[idx] = np.random.random_integers(lo, up)
        return x
    x0 = np.reshape(scipy.misc.imread(fname, mode='RGB'), (3072)) if fname else np.random.randint(256, size=3072, dtype='uint8')

    res = scipy.optimize.basinhopping(fun, x0, take_step=ts, callback=cb, disp=True)
    print res.fun

    scipy.misc.imsave(outname, np.reshape(res.x, (32, 32, 3)))

if __name__ == '__main__':
    main()
