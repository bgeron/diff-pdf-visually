
***************************************************************
``diff-pdf-visually``: Find visual differences between two PDFs
***************************************************************

.. image:: https://img.shields.io/pypi/v/diff-pdf-visually.svg
    :target: https://pypi.python.org/pypi/diff-pdf-visually/

.. image:: https://img.shields.io/pypi/l/diff-pdf-visually.svg
    :target: https://pypi.python.org/pypi/diff-pdf-visually/

.. image:: https://img.shields.io/badge/commitizen-friendly-brightgreen.svg
    :alt: Commitizen friendly
    :target: https://commitizen.github.io/cz-cli/


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


How to install this
===================

You can install this tool with ``pip3``, but we need the ImageMagick and Poppler programs.

On Ubuntu Linux
---------------

1.  ``sudo apt update``
2.  ``sudo apt install python3-pip imagemagick poppler-utils``
3.  ``pip3 install --user diff-pdf-visually``
4.  If this is the first time that you ``pip3 install --user`` something, then log out totally from Linux and log in again. (This is to refresh the ``PATH``.)
5.  Run with ``diff-pdf-visually``.

On Mac with Homebrew (untested)
-------------------------------

1.  Run ``brew install poppler imagemagick``.
2.  ``pip3 install --user diff-pdf-visually``
3.  If this is the first time that you ``pip3 install --user`` something, then close your terminal and open a new one. (This is to refresh the ``PATH``.)
4.  Run with ``diff-pdf-visually``.

On Windows Subsystem for Linux
------------------------------

I've never tried but I think this will work. Give it a go and let me know (at bram at bram dot xyz) if it worked! Unfortunately it takes quite a while to get everything installed.

1. Install Windows Subsystem for Linux (WSL) and Ubuntu 18.04, for instance `with this tutorial <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_

2. Initialize Ubuntu 18.04 (`tutorial <https://docs.microsoft.com/en-us/windows/wsl/initialize-distro>`_)

3. Now proceed with the Ubuntu Linux instructions.

Let me know (at bram at bram dot xyz) if this worked!

On Windows native
-----------------

Lars Olafsson suggested that the following might work:

- Install ``diff-pdf-visually`` via Pip.
- Install ImageMagick, e.g. via https://imagemagick.org/script/download.php
- Download pdftocairo/Poppler, e.g. the old Windows build produced by Todd Hubers and Ilya Kitaev: https://blog.alivate.com.au/poppler-windows/ . Extract the .7z file somewhere and update the Windows ``Path`` variable to add the ``bin`` folder that was extracted.
- Run ``diff-pdf-visually``.

How it works
============

We use ``pdftocairo`` to convert both PDFs to a series of PNG images in a temporary directory. The number of pages and the dimensions of the page must be exactly the same. Then we call ``compare`` from ImageMagick to check how similar they are; if one of the pages compares different above a certain threshold, then the PDFs are reported as different, otherwise they are reported the same.

**You must have ImageMagick and poppler already installed**.

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

There is also an environment variable:

- ``COMPARE``: override the path of ImageMagick compare. By default, we try first ``compare`` and then ``magick compare`` (for Windows).

So what do you use this for?
============================

Personally, I've used this a couple of times to refactor my LaTeX documents: I just simplify or remove some macro definitions, and if nothing changes, apparently it's safe to make that change.

Status
======

At the moment, this program/module works best for finding *whether* two PDFs are visually different.

This project is licenced under the MIT licence. It will not work on Python 2.

