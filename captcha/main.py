#!/usr/bin/python
# pylint:disable=missing-docstring,invalid-name,no-member

import json
import requests
import StringIO
import sys
import zipfile

import scipy

import brain
import decipher
import download


def load_initial(fninitial):
    ret = []
    initial = None
    with open(fninitial) as finitial:
        initial = json.load(finitial)
    good = initial['good']
    for name, solution in good.iteritems():
        ret.append({'name': name, 'solution': solution})
    return ret


def load_save(fnsave):
    with open(fnsave) as fsave:
        save = json.load(fsave)
        return save['solutions']


def send(solutions_wrapped):
    r = requests.post('https://captcha.delorean.codes/u/MathSquared/solution', json=solutions_wrapped)
    return r.text


def next_captcha():
    q = []
    while True:
        print 'Downloading new batch...'
        batch = download.to_dict(download.download())
        q.extend(batch.iteritems())
        for name, data in q:
            sio = StringIO.StringIO(data)
            im = scipy.misc.imread(sio, mode='RGB')
            sio.close()
            yield name, data, im


def main():
    if len(sys.argv) != 5 and len(sys.argv) != 6:
        print 'Usage: %s <model> <initial.json> <out.json> <out.zip> [save.json]'
        return

    fnmodel, fninitial, fnout, fnzip, fnsave = sys.argv[1:] + [None]
    solutions = load_initial(fninitial)

    print 'Loaded initial data: %d' % len(solutions)

    if fnsave:
        solutions += load_save(fnsave)
        print 'Loaded saved data: now %d' % (len(solutions))

    sess, x, _, y = brain.import_model(fnmodel)

    print 'Model imported'

    already = set()
    try:
        with zipfile.ZipFile(fnzip, 'w') as fzip:
            dl = next_captcha()
            while len(solutions) < 15000:
                name, data, im = dl.next()
                if name in already:
                    print '      [dp] %s' % name
                else:
                    already.add(name)
                    fzip.writestr('%s.jpg' % name, data)
                    im = decipher.preprocess(im)
                    im, feat = decipher.label(im)
                    if decipher.check_labels(im, feat):
                        lets = decipher.get_letters(im, feat)
                        lets = [brain.prepare_img(let) for let in lets]
                        res = sess.run(y, feed_dict={x: lets})
                        guess = ''.join([brain.pretty[brain.from_onehot(oh)] for oh in res])
                        solutions.append({'name': name, 'solution': guess})
                        print '%5d %-4s %s' % (len(solutions), guess, name)
                    else:
                        print '      ---- %s' % name
    except:
        print 'Error, saving...'
        try:
            with open(fnout) as fout:
                json.dump({'solutions': solutions}, fout)
        except:
            json.dump({'solutions': solutions}, sys.stdout)
            raise
        raise

    print
    print 'Writing and sending...'

    try:
        with open(fnout, 'w') as fout:
            json.dump({'solutions': solutions}, fout)
        print send({'solutions': solutions})
    except:
        json.dump({'solutions': solutions}, sys.stdout)
        print send({'solutions': solutions})
        raise


if __name__ == '__main__':
    main()
