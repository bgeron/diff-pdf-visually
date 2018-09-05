#!/usr/bin/env python3

"""
Test if there is a significant difference between two PDFs using ImageMagick
and pdftocairo.
"""

DPI=50

INFINITY = float('inf')
SIGNIFICANCE=INFINITY

VERB_PRINT_CMD=False
VERB_PDFDIFF=1
TIME_TO_INSPECT=0

import os.path, pathlib, subprocess, sys, tempfile, time

def pdftopng(sourcepath, destdir, basename):
    """
    Invoke pdftocairo to convert the given PDF path to a PNG per page.
    Return a list of page numbers (as strings).
    """
    if [] != list(destdir.glob(basename + '*')):
        raise ValueError("destdir not clean: " + repr(destdir))

    verbose_run(
        [
            'pdftocairo', '-png', '-r', str(DPI), str(sourcepath),
            str(destdir / basename)
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    # list of strings with decimals
    numbers = sorted(path.name for path in destdir.glob(basename + '*' + '.png'))

    return [s[len(basename)+1:-4] for s in numbers]

# returns a float, which can be inf
def imgdiff(a, b, diff, log):
    assert a.is_file()
    assert b.is_file()
    assert not diff.exists()
    assert not log.exists()

    with log.open('wb') as f:
        cmdresult = verbose_run(
            [
                'compare', '-verbose', '-metric', 'PSNR',
                str(a), str(b), str(diff),
            ],
            stdout=f,
            stderr=subprocess.STDOUT,
        )

    if cmdresult.returncode > 1:
        raise ValueError("compare crashed, status="+str(cmdresult.returncode))

    with log.open('r') as f:
        lines = f.readlines()

    if any('image widths or heights differ' in l for l in lines):
        raise ValueError("image widths or heights differ")

    PREF='    all: '
    all_line = [l for l in lines if l.startswith(PREF)]
    assert len(all_line) == 1
    all_str = all_line[0][len(PREF):].strip()
    all_num = INFINITY if all_str == '0' else float(all_str)
    return all_num

def is_significant(f):
    return f < SIGNIFICANCE

def pdfdiff(a, b):
    """Given two filenames, return whether the PDFs are sufficiently similar."""
    assert os.path.isfile(a), "file {} must exist".format(a)
    assert os.path.isfile(b), "file {} must exist".format(b)

    with tempfile.TemporaryDirectory(prefix="diffpdf") as d:
        p = pathlib.Path(d)
        if VERB_PDFDIFF >= 2:
            print("      Temporary directory: {}".format(p))
        # expand a
        a_i = pdftopng(a, p, "a")
        b_i = pdftopng(b, p, "b")
        if a_i != b_i:
            if VERB_PDFDIFF >= 1:
                print("Different number of pages: {} vs {}", a_i, b_i)
            return False
        assert len(a_i) > 0

        significances = []

        for pageno in a_i:
            # remember pageno is a string
            pageapath = p / "a-{}.png".format(pageno)
            pagebpath = p / "b-{}.png".format(pageno)
            diffpath = p / "diff-{}.png".format(pageno)
            logpath = p / "log-{}.txt".format(pageno)
            s = imgdiff(pageapath, pagebpath, diffpath, logpath)
            if VERB_PDFDIFF >= 2:
                print("Page {}: significance={}".format(pageno, s))

            significances.append(s)

        min_significance = min(significances, default=INFINITY)
        significant = is_significant(min_significance)
        if VERB_PDFDIFF >= 1:
            freetext = "different" if significant else "the same"
            print("Min sig = {}, significant?={}. The PDFs are {}.".format(
                    min_significance, significant, freetext
                ))

        if TIME_TO_INSPECT > 0:
            print(
                "Waiting for {} seconds before removing temporary directory..."
                .format(TIME_TO_INSPECT),
                end='',
                flush=True
            )
            time.sleep(TIME_TO_INSPECT)
            print(" done.")

        return not significant

def verbose_run(args, *restargs, **kw):
    if VERB_PRINT_CMD:
        print("Running: {}".format(' '.join(args)), file=sys.stderr)
    return subprocess.run(args, *restargs, **kw)

def verbose_check_output(args, *restargs, **kw):
    if VERB_PRINT_CMD:
        print("Running: {}".format(' '.join(args)), file=sys.stderr)
    return subprocess.check_output(args, *restargs, **kw)
