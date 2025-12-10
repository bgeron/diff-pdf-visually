"""
Quickly check whether there is a visible difference between two PDFs, using ImageMagick and pdftocairo.
"""

__version__ = '2.0.0.alpha1'

from typing import List

__all__ = [] # type: List[str]

from .diff import pdf_similar, pdfdiff_pages
from .diff import pdftopng, imgdiff_ratio
