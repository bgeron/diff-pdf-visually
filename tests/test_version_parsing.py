from diff_pdf_visually.scale import imagemagick_psnr_scale_from_version, SCALE_INFTY_TO_0, SCALE_1_TO_0, MODERN

def test_version_parsing():
    # Hypothetical, assume behaves like 7.1.1-0.
    # Check that weird versions don't break at least.
    assert imagemagick_psnr_scale_from_version("6.3.5-gamma") == SCALE_INFTY_TO_0
    assert imagemagick_psnr_scale_from_version("7.0") == SCALE_INFTY_TO_0
    assert imagemagick_psnr_scale_from_version("7.1.1-0") == SCALE_INFTY_TO_0
    assert imagemagick_psnr_scale_from_version("7.1.1-45") == SCALE_INFTY_TO_0
    try:
        imagemagick_psnr_scale_from_version("7.1.1-46")
        assert False
    except EnvironmentError:
        pass
    assert imagemagick_psnr_scale_from_version("7.1.1-47") == SCALE_1_TO_0
    assert imagemagick_psnr_scale_from_version("7.1.2-0") == MODERN
    # Latest version as of writing
    assert imagemagick_psnr_scale_from_version("7.1.2-8") == MODERN

    # Hypothetical, assume behaves like 7.1.2-0.
    # Check that weird versions don't break at least.
    assert imagemagick_psnr_scale_from_version("7.1.3-alpha") == MODERN
