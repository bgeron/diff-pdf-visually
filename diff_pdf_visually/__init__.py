"""
Quickly check whether there is a visible difference between two PDFs, using ImageMagick and pdftocairo.
"""

__version__ = '1.8.1'

from typing import List

__all__ = [] # type: List[str]

from .diff import pdf_similar, pdfdiff_pages, pdfdiff
from .diff import pdftopng, imgdiff
