from diff_pdf_visually import pdfdiff


def test_examples():
    assert pdfdiff("tests/base.pdf", "tests/base_plus_white_text.pdf")
    assert not pdfdiff("tests/base.pdf", "tests/base_shifted_layout.pdf")
