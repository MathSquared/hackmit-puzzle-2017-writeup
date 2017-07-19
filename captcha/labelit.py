#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import json
import os
import sys

import scipy
from scipy import misc

import decipher


bad_words = set(('bad', '--', 'no', 'reject', 'x'))


def show_labeled(impath):
    im = scipy.misc.imread(impath)
    scipy.misc.imshow(im)
    im = decipher.preprocess(im)
    im, feat = decipher.label(im)
    im *= (255 / feat)
    scipy.misc.imshow(im)


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print 'Usage: %s <image_dir> <labels> [new_labels]'
    else:
        imdir, fnlabels = sys.argv[1:]
        fnnewlabels = sys.argv[3] if len(sys.argv) > 3 else fnlabels

        labels = {'good': {}, 'bad': {}}
        if os.path.isfile(fnlabels):
            with open(fnlabels) as flabels:
                labels = json.load(flabels)

        imnames = os.listdir(imdir)
        imnames.sort()
        impaths = [os.path.abspath(os.path.join(imdir, imname)) for imname in imnames]
        imnames = [os.path.splitext(imname)[0] for imname in imnames]

        try:
            for imname, impath in zip(imnames, impaths):
                if imname not in labels['good'] and imname not in labels['bad']:
                    print 'Label %s:' % imname
                    show_labeled(impath)
                    label = raw_input('-> ').strip()

                    if label in bad_words:
                        labels['bad'][imname] = True
                        print 'Marked as bad.'
                    elif len(label) == 4:
                        labels['good'][imname] = label
                        print 'Marked as good with label %s.' % label
                        print '%d labeled images.' % len(labels['good'])
                    else:
                        print 'Skipping this image.'
                    print
        except EOFError:
            # always, always, always output JSON
            pass

        try:
            with open(fnnewlabels, 'w') as fnewlabels:
                json.dump(labels, fnewlabels)
        except IOError:
            json.dump(labels, sys.stdout)
            raise


if __name__ == '__main__':
    main()
