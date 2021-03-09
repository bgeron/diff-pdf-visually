"""
'Quickly check whether there is a visible difference between two PDFs, using ImageMagick and pdftocairo.
"""

__version__ = '1.6.1'

from typing import List

__all__ = [] # type: List[str]

from .diff import pdfdiff, pdfdiff_pages
from .diff import pdftopng, imgdiff
