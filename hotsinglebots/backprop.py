#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import sys

import keras
from keras import backend as K
import numpy as np
import scipy

import brain

# Much credit to
# https://github.com/fchollet/keras/blob/master/examples/conv_filter_visualization.py
# and
# https://blog.keras.io/how-convolutional-neural-networks-see-the-world.html


def layer_dict(model):
    return {layer.name: layer for layer in model.layers}


def get_iterate(model, layer_name, output_index):
    layers = layer_dict(model)
    layer_out = layers[layer_name].output

    loss = K.mean(layer_out[:, output_index])

    grad = K.gradients(loss, model.input)[0]
    grad /= K.sqrt(K.mean(K.square(grad)) + 1e-5)

    return K.function([model.input], [loss, grad])


def gradient_ascent(iterate, begin=None, steps=20000):
    l, g = None, None
    if not begin:
        begin = np.random.random((1, 32, 32, 3)) * 128 + 20
    for _ in range(steps):
        l, g = iterate([begin])
        begin += g * 2
        print l
        if l <= 0: break

    return begin, l


def beautify_im(res):
    res = (res - res.mean()) / (res.std() + 1e-5)
    res *= 0.1

    res += 0.5
    res = np.clip(res, 0, 1)

    res *= 255
    res = np.clip(res, 0, 255).astype('uint8')
    return res


def main():
    outname = sys.argv[1] if len(sys.argv) > 1 else 'picture.png'
    model = brain.get_model()
    iterate = get_iterate(model, 'predictions', 1)
    res, loss = gradient_ascent(iterate)

    if loss > 0:
        #im = beautify_im(res[0])
        im = np.clip(res[0], 0, 255).astype('uint8')
        scipy.misc.imsave(outname, im)
        print 'Done. Loss: %e' % loss
    else:
        print 'Unable to process.'


if __name__ == '__main__':
    main()
