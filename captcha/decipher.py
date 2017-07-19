#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name,no-member

import sys

import numpy as np
import scipy
from scipy import misc, ndimage

import lines
import ocr_letter


def threshold(im):
    return (im[:, :, 1] > 192) * 255


def denoise(im):
    #scipy.misc.imshow(im)
    ret = np.copy(im)
    #np.set_printoptions(threshold='nan')
    #print ret
    ret -= lines.lines * 255
    ret = np.clip(ret, 0, 255)
    #scipy.misc.imshow(lines.lines)
    #print ret
    #scipy.misc.imshow(ret)
    ret = scipy.ndimage.grey_closing(ret, (5, 5))
    #scipy.misc.imshow(im)
    return scipy.ndimage.grey_opening(ret * im / 255, (2, 2))


#def denoise(im):
#    ret = im[:,:]
#    ret[22,14:25] = 0  # get rid of known noise spot
#    ret[20,32:41] = 0
#    ret[22,78:81] = 0
#    ret[24,71:75] = 0
#    ret[26,66:71] = 0
#    ret = scipy.ndimage.grey_opening(im, (2, 2))
#    return ret


def preprocess(im):
    return denoise(threshold(im))


def label(im):
    # Label in x-axis only to avoid breaking apart i's
    flat = im.max(axis=0)
    label_flat, num_features = scipy.ndimage.label(flat)
    label = (im * label_flat) / 255
    return label, num_features


def crop_to_fit(im):
    # https://stackoverflow.com/a/44734377
    rows = np.any(im, axis=1)
    cols = np.any(im, axis=0)
    ymn, ymx = np.where(rows)[0][[0, -1]]
    xmn, xmx = np.where(cols)[0][[0, -1]]
    return im[ymn:ymx+1, xmn:xmx+1]


def check_labels(im, feat):
    if feat != 4:
        return False
    for f in range(1, feat + 1):
        area = np.count_nonzero(im == f)
        if area < 53:  # detached stem
            return False
        if area > 205:  # two letters
            return False

        bbox = crop_to_fit(im == f)
        bbox_sh = bbox.shape
        if bbox_sh[0] > 24 or bbox_sh[1] > 24:  # two letters
            return False

    return True


def get_letters(im, feat, invert=True):
    identity = lambda x: x
    return [(np.invert if invert else identity)(crop_to_fit(im == f)) for f in range(1, feat + 1)]


def main():
    im = scipy.misc.imread('samples/7f5b038b5dfec2e785116e43c8d74fd3.jpg')
    im = preprocess(im)
    #im = threshold(im)
    im, feat = label(im)
    scipy.misc.imshow(im * (255 / feat))

    if check_labels(im, feat):
        lets = get_letters(im, feat)
        scipy.misc.imshow(lets[0])
        scipy.misc.imsave('letout.png', lets[0])
        ocr = [ocr_letter.ocr(let) for let in lets]
        print ''.join(ocr)
    else:
        print 'invalid'


if __name__ == '__main__':
    main()
