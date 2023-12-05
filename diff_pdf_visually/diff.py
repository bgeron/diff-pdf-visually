#!/usr/bin/env python3

"""
Test if there is a significant difference between two PDFs using ImageMagick
and pdftocairo.
"""

INFINITY = float("inf")

import os.path, pathlib, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from .polyfill import nullcontext
from .constants import DEFAULT_THRESHOLD, DEFAULT_VERBOSITY, DEFAULT_DPI
from .constants import VERB_PRINT_REASON, VERB_PRINT_TMPDIR
from .constants import VERB_PERPAGE, VERB_PRINT_CMD, VERB_ROUGH_PROGRESS
from .constants import DEFAULT_NUM_THREADS, MAX_REPORT_PAGENOS

from . import external_programs
from .external_programs import verbose_run


def pdftopng(sourcepath, destdir, basename, verbosity, dpi):
    """
    Invoke pdftocairo to convert the given PDF path to a PNG per page.
    Return a list of page numbers (as strings).
    """
    if [] != list(destdir.glob(basename + "*")):
        raise ValueError("destdir not clean: " + repr(destdir))

    verbose_run(
        (verbosity > VERB_PRINT_CMD),
        [
            "pdftocairo",
            "-png",
            "-r",
            str(dpi),
            str(sourcepath),
            str(destdir / basename),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    # list of strings with decimals
    numbers = sorted(path.name for path in destdir.glob(basename + "*" + ".png"))

    return [s[len(basename) + 1 : -4] for s in numbers]


# returns a float, which can be inf
def imgdiff(a, b, diff, log, print_cmds):
    assert a.is_file()
    assert b.is_file()
    assert not diff.exists()
    assert not log.exists()

    with log.open("w+b") as f:
        cmdresult = verbose_run(
            print_cmds,
            external_programs.compare_cmd(print_cmds)
            + ["-verbose", "-metric", "PSNR", str(a), str(b), str(diff),],
            stdout=f,
            stderr=subprocess.STDOUT,
        )

    if cmdresult.returncode > 1:
        raise ValueError("compare crashed, status=" + str(cmdresult.returncode))

    with log.open("r") as f:
        lines = f.readlines()

    if any("image widths or heights differ" in l for l in lines):
        raise ValueError("image widths or heights differ")

    PREF = "    all: "
    all_line = [l for l in lines if l.startswith(PREF)]
    assert len(all_line) == 1
    all_str = all_line[0][len(PREF) :].strip()
    all_num = INFINITY if (all_str == "0" or all_str == "1.#INF") else float(all_str)
    return all_num



def pdf_similar(a, b, **kw):
    """
    Return True if the PDFs are sufficiently similar.

    The optional arguments to this function can be found on pdfdiff_pages.
    """

    return len(pdfdiff_pages(a, b, **kw)) == 0
def pdfdiff(*args, **kw):
    """
    DEPRECATED: THIS FUNCTION HAS A VERY CONFUSING NAME.
    Alias for pdf_similar.
    """
    import warnings
    warnings.warn('pdfdiff was renamed to pdf_similar', DeprecationWarning)
    return pdf_similar(*args, **kw)

def pdfdiff_pages(
    a,
    b,
    threshold=DEFAULT_THRESHOLD,
    verbosity=DEFAULT_VERBOSITY,
    dpi=DEFAULT_DPI,
    tempdir=None,
    time_to_inspect=0,
    num_threads=DEFAULT_NUM_THREADS,
    max_report_pagenos=MAX_REPORT_PAGENOS,
):
    """
    Find visual differences between two PDFs; return the page numbers with
    significant differences.

    When the number of pages is different between the PDFs, then return [-1].

    Keyword arguments:

    tempdir: if not None, then this should be a pathlib.Path for an empty writable
        directory where we will put temporary files, which help the user understand
        where differences are and what led to the conclusion on whether the two
        PDF files are significantly different.

        The layout of this directory is not guaranteed to remain stable across
        releases of diff_pdf_visually, but it may contain an image for each page of
        either PDF, and an image for the difference, and a text log.

    time_to_inspect: after computing the diff, wait for this many seconds before
        removing the temporary directory (if tempdir was not specified) and
        returning from the function. If tempdir was specified, then we will not
        remove the directory.
    """

    assert os.path.isfile(a), "file {} must exist".format(a)
    assert os.path.isfile(b), "file {} must exist".format(b)

    if tempdir == None:
        path_context = tempfile.TemporaryDirectory(prefix="diffpdf-")
    else:
        assert isinstance(tempdir, pathlib.Path)
        assert tempdir.is_dir(), \
            f"Temporary directory {tempdir} should be an existing directory"
        assert list(tempdir.glob('*')) == [], \
            f"temporary directory {tempdir} should be empty at the start"
        path_context = nullcontext(tempdir)

    with path_context as p:
        if not isinstance(p, pathlib.Path):
            # The TemporaryDirectory context manager returns a string
            p = pathlib.Path(p)

        if verbosity >= VERB_PRINT_TMPDIR:
            print("  Temporary directory: {}".format(p))
        if verbosity >= VERB_ROUGH_PROGRESS:
            print("  Converting each page of the PDFs to an image...")

        # expand pdfs to pngs
        with ThreadPoolExecutor(max_workers=num_threads) as pool:
            a_i_ = pool.submit(pdftopng, a, p, "a", verbosity=verbosity, dpi=dpi)
            b_i_ = pool.submit(pdftopng, b, p, "b", verbosity=verbosity, dpi=dpi)

            # Wait for results
            a_i = a_i_.result()
            b_i = b_i_.result()

        if a_i != b_i:
            assert len(a_i) != len(
                b_i
            ), "mishap with weird page numbers: {} vs {}".format(a_i, b_i)
            if verbosity >= VERB_PRINT_REASON:
                print("Different number of pages: {} vs {}".format(len(a_i), len(b_i)))
            return [-1]
        assert len(a_i) > 0

        if verbosity >= VERB_ROUGH_PROGRESS:
            print(
                "  PDFs have same number of pages. Checking each pair of converted images..."
            )

        significances = []

        for pageno in a_i:
            # remember pageno is a string
            pageapath = p / "a-{}.png".format(pageno)
            pagebpath = p / "b-{}.png".format(pageno)
            diffpath = p / "diff-{}.png".format(pageno)
            logpath = p / "log-{}.txt".format(pageno)
            s = imgdiff(
                pageapath, pagebpath, diffpath, logpath, (verbosity > VERB_PRINT_CMD)
            )
            if verbosity >= VERB_PERPAGE:
                print("- Page {}: significance={}".format(pageno, s))

            significances.append(s)

        min_significance = min(significances, default=INFINITY)
        significant = min_significance <= threshold

        largest_significances = sorted(
            (sgf, pageno_minus_one + 1)
            for (pageno_minus_one, sgf) in enumerate(significances)
            if sgf < threshold
        )

        if verbosity >= VERB_PRINT_REASON:
            freetext = "different" if significant else "the same"
            print(
                "Min sig = {}, significant?={}. The PDFs are {}.{}".format(
                    min_significance,
                    significant,
                    freetext,
                    ""
                    if largest_significances == []
                    else " The most different pages are: {}.".format(
                        ", ".join(
                            "page {} (sgf. {})".format(pageno, sgf)
                            for (sgf, pageno) in largest_significances[
                                :max_report_pagenos
                            ]
                        )
                    ),
                )
            )

        if time_to_inspect > 0:
            print(
                "Waiting for {} seconds before removing temporary directory...".format(
                    time_to_inspect
                ),
                end="",
                flush=True,
            )
            time.sleep(time_to_inspect)
            print(" done.")

        return list(map(lambda pair: pair[1], largest_significances))
