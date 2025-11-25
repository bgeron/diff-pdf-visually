from diff_pdf_visually.scale import SCALE_INFTY_TO_0, SCALE_1_TO_0, convert_to_modern_scale

def absdiff(x, y):
    return abs(x - y)

def test_scale_conversion():
    # These are each PSNR results from ImageMagick v7.1.1-45 vs v7.1.1-47
    # vs v7.1.2-8 .

    # Completely different, e.g. black image vs white image
    assert absdiff(convert_to_modern_scale(SCALE_INFTY_TO_0, float("inf")), 0) < 1e-9
    assert absdiff(convert_to_modern_scale(SCALE_1_TO_0, 1), 0) < 1e-9
    # Modern: 0

    # Completely the same, e.g. white image vs. white image, or black vs. black
    assert absdiff(convert_to_modern_scale(SCALE_INFTY_TO_0, 0), 1) < 1e-9
    assert absdiff(convert_to_modern_scale(SCALE_1_TO_0, 0), 1) < 1e-9
    # Modern: 1

    # Base vs. base + period
    assert absdiff(convert_to_modern_scale(SCALE_INFTY_TO_0, 1.40473), .47085767) < 1e-6
    assert absdiff(convert_to_modern_scale(SCALE_1_TO_0, 0.000000171452), 0.5681449806) < 1e-6
    # Modern: 0.563821

    # Base vs. shifted layout
    assert absdiff(convert_to_modern_scale(SCALE_INFTY_TO_0, 0.769508), 0.6189626384) < 1e-6
    assert absdiff(convert_to_modern_scale(SCALE_1_TO_0, 0.000196647), 0.3278869916) < 1e-6
    # Modern: 0.308859

    # Complex layout page 1
    assert absdiff(convert_to_modern_scale(SCALE_INFTY_TO_0, 1.1842), 0.5135157341) < 1e-6
    assert absdiff(convert_to_modern_scale(SCALE_1_TO_0, 0.00000000185539), 0.7052220067) < 1e-6
    # Modern: 0.72763

    # Complex layout page 2
    assert absdiff(convert_to_modern_scale(SCALE_INFTY_TO_0, 1.59225), 0.439792418) < 1e-6
    assert absdiff(convert_to_modern_scale(SCALE_1_TO_0, 0.000000045457), 0.6098765583) < 1e-6
    # Modern: 0.611867

    # Complex layout version A, compare page 1 to page 2
    assert absdiff(convert_to_modern_scale(SCALE_INFTY_TO_0, 0.515075), 0.7081852046) < 1e-6
    assert absdiff(convert_to_modern_scale(SCALE_1_TO_0, 0.00342953), 0.2222183541) < 1e-6
    # Modern: 0.72763



# black/white	0.7310585786	999999	1	0		0.000001249999688	0
# identical	0.5	0	0	1		1	0.7297297297
# plus period	0.5000000429	1.40473	1.71E-07	0.563821		0.4708576767	0.5491137618
# shifted	0.5000491617	0.769508	0.000196647	0.308859		0.6189626384	0.4001690137
# complex 1	0.5000000005	1.1842	1.86E-09	0.72763		0.5135157341	0.611149377
# complex 2	0.5000000114	1.59225	4.55E-08	0.611867		0.439792418	0.5692684885
# complex a 1-2	0.5008573817	0.515075	0.00342953	0.205397		0.7081852046	0.3073150575
