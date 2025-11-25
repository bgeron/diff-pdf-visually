from diff_pdf_visually import pdf_similar, pdfdiff_pages
from tempfile import TemporaryDirectory
from pathlib import Path

def test_examples():
    ## Per page, simple examples
    assert [1] == pdfdiff_pages("tests/base.pdf", "tests/base_shifted_layout.pdf",
        verbosity=0)
    assert [-1] == pdfdiff_pages("tests/base.pdf", "tests/base_twice.pdf",
        verbosity=0)

    ## For the whole PDF
    assert pdf_similar("tests/base.pdf", "tests/base_plus_white_text.pdf",
        verbosity=0)
    assert not pdf_similar("tests/base.pdf", "tests/base_shifted_layout.pdf",
        verbosity=0)
    assert not pdf_similar("tests/base.pdf", "tests/base_twice.pdf",
        verbosity=0)
    
    ## Per page; determine which page is 'most different'
    assert [] == pdfdiff_pages("tests/complex_1.pdf", "tests/complex_2.pdf",
        verbosity=0, threshold_ratio=0.02)
    assert [] == pdfdiff_pages("tests/complex_1.pdf", "tests/complex_2.pdf",
        verbosity=0, threshold_ratio=0.1)
    assert [2, 1] == pdfdiff_pages("tests/complex_1.pdf", "tests/complex_2.pdf",
        verbosity=0, threshold_ratio=0.9)

    with TemporaryDirectory(dir=".", prefix="test_temp_") as d:
        p = Path(d)

        assert [2, 1] == pdfdiff_pages(
            "tests/complex_1.pdf",
            "tests/complex_2.pdf",
            verbosity=0,
            threshold_ratio=100,
            tempdir=p,
        )

        for template in [
            'a-{}.png', 'b-{}.png', 'diff-{}.png', 'log-{}.txt'
        ]:
            assert (p / template.format(1)).is_file()
            assert (p / template.format(2)).is_file()
            assert not (p / template.format(3)).exists()
