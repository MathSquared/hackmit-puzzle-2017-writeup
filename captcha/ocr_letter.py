#!/usr/bin/env python
# pylint:disable=missing-docstring,invalid-name,no-member

import StringIO
import subprocess

import scipy


def np_to_png(im):
    fout = StringIO.StringIO()
    scipy.misc.imsave(fout, im, 'png')
    ret = fout.getvalue()
    fout.close()
    return ret

def png_to_text(png):
    cmd = ['tesseract']
    cmd += ['-psm', '10']  # single character
    cmd += ['stdin', 'stdout']
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    res, _ = p.communicate(png)

    if p.returncode:
        return None
    return res


def ocr(im):
    return png_to_text(np_to_png(im))
