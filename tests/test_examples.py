from diff_pdf_visually import pdfdiff, pdfdiff_pages
from tempfile import TemporaryDirectory
from pathlib import Path

def test_examples():
    assert pdfdiff("tests/base.pdf", "tests/base_plus_white_text.pdf",
        verbosity=0)
    assert not pdfdiff("tests/base.pdf", "tests/base_shifted_layout.pdf",
        verbosity=0)
    assert not pdfdiff("tests/base.pdf", "tests/base_twice.pdf",
        verbosity=0)
    assert [1] == pdfdiff_pages("tests/base.pdf", "tests/base_shifted_layout.pdf",
        verbosity=0)
    assert [-1] == pdfdiff_pages("tests/base.pdf", "tests/base_twice.pdf",
        verbosity=0)
    assert [2, 1] == pdfdiff_pages("tests/complex_1.pdf", "tests/complex_2.pdf",
        verbosity=0, threshold=100)
    assert [] == pdfdiff_pages("tests/complex_1.pdf", "tests/complex_2.pdf",
        verbosity=0, threshold=10)

    with TemporaryDirectory(dir=".", prefix="test_temp_") as d:
        p = Path(d)

        assert [2, 1] == pdfdiff_pages(
            "tests/complex_1.pdf",
            "tests/complex_2.pdf",
            verbosity=0,
            threshold=100,
            tempdir=p,
        )

        for template in [
            'a-{}.png', 'b-{}.png', 'diff-{}.png', 'log-{}.txt'
        ]:
            assert (p / template.format(1)).is_file()
            assert (p / template.format(2)).is_file()
            assert not (p / template.format(3)).exists()
