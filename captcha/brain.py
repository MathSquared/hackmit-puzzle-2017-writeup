#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name,no-member

import glob
import os
import sys

import numpy as np
import scipy
import scipy.misc
import tensorflow as tf

pretty = list('1234567890qwertyuiopasdfghjklzxcvbnm')
slot = {let: i for i, let in enumerate(pretty)}


def to_onehot(sz, slot):
    ret = np.zeros([sz])
    ret[slot] = 1
    return ret


def from_onehot(onehot):
    return np.argmax(onehot)


def read_labeled(base, imglob):
    """
    Reads and returns a labeled set of character images.

    Reads from base/*/imglob, using the first * as the labels.
    Returns parallel arrays of the images read and the labels.
    """
    impaths = glob.glob(os.path.join(base, '*', imglob))

    splitpaths = [os.path.normpath(path).split(os.path.sep) for path in impaths]
    splitbase = os.path.normpath(base).split(os.path.sep)
    label_idx = len(splitbase)
    labels = [splitpath[label_idx] for splitpath in splitpaths]
    onehots = [to_onehot(len(pretty), slot[label]) for label in labels]

    ims = [(scipy.misc.imread(path, mode='L') != 0) for path in impaths]

    return onehots, ims


def prepare_img(im, invert=True):
    sh = im.shape
    pad_v = (24 - sh[0])
    pad_h = (24 - sh[1])
    pad_t = pad_v // 2
    pad_b = pad_v - pad_t
    pad_l = pad_h // 2
    pad_r = pad_h - pad_l

    if invert:
        im = np.invert(im)

    return np.pad(im, ((pad_t, pad_b), (pad_l, pad_r)), 'constant')


def model():
    # https://github.com/tensorflow/tensorflow/blob/r1.2/tensorflow/examples/tutorials/mnist/mnist_softmax.py
    x = tf.placeholder(tf.float32, [None, 24, 24], name='x')
    xf = tf.contrib.layers.flatten(x)
    W = tf.Variable(tf.zeros([24 * 24, 36]))
    b = tf.Variable(tf.zeros([36]))
    y = tf.add(tf.matmul(xf, W), b, name='y')
    y_ = tf.placeholder(tf.float32, [None, 36], name='y_')

    cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    return train_step, accuracy, x, y_, y


def import_model(fname):
    sess = tf.Session()
    saver = tf.train.import_meta_graph(os.path.splitext(fname)[0] + '.meta')
    saver.restore(sess, fname)

    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name('x:0')
    y = graph.get_tensor_by_name('y:0')
    y_ = graph.get_tensor_by_name('y_:0')

    return sess, x, y_, y


def main():
    if len(sys.argv) != 5:
        print 'Usage: %s <base> <train_glob> <test_glob> <model_out>'
        return

    base, train_glob, test_glob, model_out = sys.argv[1:]

    train_y_, train_raw = read_labeled(base, train_glob)
    test_y_, test_raw = read_labeled(base, test_glob)
    train_x = [prepare_img(im) for im in train_raw]
    test_x = [prepare_img(im) for im in test_raw]

    print train_x[0]

    print 'Data read: %d train, %d test' % (len(train_x), len(test_x))

    train_step, accuracy, x, y_, y = model()

    print 'Model initialized'

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    for step in range(1000):
        sess.run(train_step, feed_dict={x: train_x, y_: train_y_})
        if step % 10 == 0:
            print step

    print 'Model trained'

    print 'Accuracy:', sess.run(accuracy, feed_dict={x: test_x, y_: test_y_})

    saver = tf.train.Saver()
    print 'Filepath:', saver.save(sess, model_out)


if __name__ == '__main__':
    main()
