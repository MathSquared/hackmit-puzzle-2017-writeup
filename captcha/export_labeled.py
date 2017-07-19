#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name

import json
import os
import StringIO
import sys
import zipfile

import scipy

import decipher


def main():
    if len(sys.argv) != 4:
        print 'Usage: %s <images_dir> <labels.json> <output.zip>' % sys.argv[0]
        return
    imdir, fnlabels, fnout = sys.argv[1:]

    labels = None
    with open(fnlabels) as flabels:
        labels = json.load(flabels)

    imnames = os.listdir(imdir)
    impaths = [os.path.join(imdir, imname) for imname in imnames]
    imnames = [os.path.splitext(imname)[0] for imname in imnames]

    with zipfile.ZipFile(fnout, 'w') as fout:
        for imname, impath in zip(imnames, impaths):
            if imname not in labels['good']:
                continue
            im = scipy.misc.imread(impath)
            im = decipher.preprocess(im)
            im, feat = decipher.label(im)
            if decipher.check_labels(im, feat):
                lets = decipher.get_letters(im, feat)
                for i, (label, let) in enumerate(zip(labels['good'][imname], lets)):
                    sio = StringIO.StringIO()
                    scipy.misc.imsave(sio, let, 'png')
                    png = sio.getvalue()
                    sio.close()

                    fout.writestr('%s/%s_%d.png' % (label, imname, i), png)


if __name__ == '__main__':
    main()
