
***************************************************************
``diff-pdf-visually``: Find visual differences between two PDFs
***************************************************************

.. image:: https://img.shields.io/pypi/v/diff-pdf-visually.svg
    :target: https://pypi.python.org/pypi/diff-pdf-visually/

.. image:: https://img.shields.io/pypi/l/diff-pdf-visually.svg
    :target: https://pypi.python.org/pypi/diff-pdf-visually/

This script checks whether two PDFs are visually the same. So:

- White text on a white background will be **ignored**.
- Subtle changes in position, size, or color of text will be **detected**.
- This program will ignore changes caused by a different version of the PDF generator, or by invisible changes in the source document.

This is in contrast to most other tools, which tend to extract the text stream out of a PDF, and then diff those texts. Such tools include:

- `pdf-diff <https://github.com/JoshData/pdf-diff>`_ by Joshua Tauberer

There seem to be some tools similar to the one you're looking at now, although I have experience with none of these:

- Václav Slavík seems to have `an open source one <https://github.com/vslavik/diff-pdf>`_
- There might be more useful ones mentioned on `this SuperUser thread <https://superuser.com/questions/46123/how-to-compare-the-differences-between-two-pdf-files-on-windows>`_

The strength of this script is that it's simple to use on the command line, and it's easy to reuse in scripts:

.. code-block:: python

    from diff_pdf_visually import pdfdiff

    # Returns True or False
    pdfdiff("a.pdf", "b.pdf")

Or use it from the command line:

.. code-block:: shell

    $ pip3 install --user diff-pdf-visually
    $ diff-pdf-visually a.pdf b.pdf

How it works
============

We use ``pdftocairo`` to convert both PDFs to a series of PNG images in a temporary directory. The number of pages and the dimensions of the page must be exactly the same. Then we call ``compare`` from ImageMagick to check how similar they are; if one of the pages compares different above a certain threshold, then the PDFs are reported as different, otherwise they are reported the same.

**You must have ImageMagick and pdftocairo already installed**.

Call ``diff-pdf-visually`` without parameters (or run ``python3 -m diff_pdf_visually``) to see its command line arguments. Import it as ``diff_pdf_visually`` to use its functions from Python.

There are some options that you can use either from the command line or from Python::

    $ diff-pdf-visually  -h
    usage: diff-pdf-visually [-h] [--silent] [--verbose] [--threshold THRESHOLD]
                             [--dpi DPI] [--time TIME]
                             a.pdf b.pdf

    Compare two PDFs visually. The exit code is 0 if they are the same, and 2 if
    there are significant differences.

    positional arguments:
      a.pdf
      b.pdf

    optional arguments:
      -h, --help            show this help message and exit
      --silent, -q          silence output (can be used only once)
      --verbose, -v         show more information (can be used 2 times)
      --threshold THRESHOLD
                            PSNR threshold to consider a change significant,
                            higher is more sensitive (default: 100)
      --dpi DPI             resolution for the rasterised files (default: 50)
      --time TIME           number of seconds to wait before discarding temporary
                            files, or 0 to immediately discard

These "temporary files" include a PNG image of where any differences are, per page, as well as the log output of ImageMagick. If you want to get a feeling for thresholds, there are some example PDFs in the ``tests/`` directory.

So what do you use this for?
============================

Personally, I've used this a couple of times to refactor my LaTeX documents: I just simplify or remove some macro definitions, and if nothing changes, apparently it's safe to make that change.

How to install this
===================

``pip3 install diff-pdf-visually``

Status
======

At the moment, this program/module works best for finding *whether* two PDFs are visually different.

This project is licenced under the MIT licence. It does not work on Python 2, but patches are welcome if they are not too invasive.

