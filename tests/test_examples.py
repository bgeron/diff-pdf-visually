from diff_pdf_visually import pdfdiff, pdfdiff_pages


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
