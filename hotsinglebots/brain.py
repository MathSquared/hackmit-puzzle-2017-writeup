#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import itertools
import sys

import keras
import numpy as np
import scipy

classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
interps = ['bilinear', 'nearest', 'lanczos', 'bicubic', 'cubic']
model = None


def get_model():
    global model
    model = model or keras.models.load_model('model.hdf5')
    return model


def get_image(fname, interp='bilinear'):
    im = scipy.ndimage.imread(fname, mode='RGB')
    return scipy.misc.imresize(im, (32, 32, 3), interp)


def automobile(Im, model):
    pred = model.predict(Im)
    return list(pred[:][1]), list(np.argmax(pred, 1))


def classify_images(Im, model):
    pred = model.predict(Im)
    return [np.argmax(predx) for predx in pred]


def main():
    model = get_model()
    print 'Model initialized.'
    dats = list(itertools.product(sys.argv[1:], interps))
    Im = np.array([get_image(fname, intp) for fname, intp in dats])
    pred = model.predict(Im)
    print pred
    for (fname, intp), predx in zip(dats, pred):
        print '%10s  %8s:%s' % (classes[np.argmax(predx)], intp, fname)


if __name__ == '__main__':
    main()
