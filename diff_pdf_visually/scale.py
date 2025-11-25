import math, re, sys

from . import external_programs
from .external_programs import verbose_run

# poor person's enum
SCALE_INFTY_TO_0 = 'infty means 0% similar, 0 means 100% similar, typical values below 10'
SCALE_1_TO_0 = '1 means 0% similar, 0 means 100% similar, typical values about one billionth'
MODERN = '0 means 0% similar, 1 means 100% similar, typical values around 0.5'

DETECTED_SCALE = None

MINIMUM_V7_1_1_47_VALUE=1e-15

VERSION_WARNING = "diff-pdf-visually: WARNING: detected ImageMagick version {}, which " \
    + "diff-pdf-visually has not been tuned on. Diff-pdf-visually may give wrong results. " \
    + "Consider installing ImageMagick 7.1.1-47 or v7.1.2-*."

def imagemagick_psnr_scale_from_version(magick_version_str):
    """
    Given ImageMagick's version string, determine what scale it
    uses for its PSNR metrics.

    If in this version of ImageMagick, its metrics are unusable to us,
    raise an exception.
    """

    triple = magick_version_str.split(".")[:3]

    major, minor = int(triple[0]), int(triple[1])
    if (major, minor) < (7, 1):
        print(VERSION_WARNING.format(magick_version_str), file=sys.stderr)

        return SCALE_INFTY_TO_0

    patch, subpatch = triple[2].split('-', 2)
    patch = int(patch)
    if patch >= 2:
        return MODERN

    subpatch = int(subpatch)
    if subpatch < 46:
        if subpatch < 44:
            print(VERSION_WARNING.format(magick_version_str), file=sys.stderr)
        return SCALE_INFTY_TO_0
    elif subpatch == 46:
        raise EnvironmentError(
            "ImageMagick version 7.1.1-46 does not report usable PSNR metrics for us. "
            "Please switch to any other version."
        )
    else:
        return SCALE_1_TO_0

def convert_to_modern_scale(from_scale, value):
    """
    Approximate conversion from old scales.

    This conversion makes the values broadly comparable, but generally old
    versions of ImageMagick have different algorithms, and the metric returned
    by old ImageMagick versions, after scale-conversion will be sometimes
    higher and sometimes lower than the metric returned by modern ImageMagick
    (i.e. stuff like 7.1.2-8).
    """

    if from_scale == SCALE_INFTY_TO_0:
        return 1 / (1 + 0.8 * value)

    elif from_scale == SCALE_1_TO_0:
        value_not_exponential = (
            math.log((value + MINIMUM_V7_1_1_47_VALUE) / MINIMUM_V7_1_1_47_VALUE, 10)
            / -math.log(MINIMUM_V7_1_1_47_VALUE, 10)
        )
        return 1 - value_not_exponential ** 1.4

    elif from_scale == MODERN:
        return value

    else:
        raise ValueError(f"Unknown scale: {from_scale}")

def detect_scale_for_current_imagemagick(verbose=True, print_cmds=True):
    """
    Try to detect the scale used by currently installed ImageMagick.

    The result is memoized.
    """

    global DETECTED_SCALE

    if DETECTED_SCALE: return DETECTED_SCALE

    if verbose:
        print("Detecting version of ImageMagick in use.", file=sys.stderr)

    cmdline = external_programs.compare_cmd(print_cmds) + ["-version"]
    cmdresult = verbose_run(
        print_cmds,
        cmdline,
        capture_output=True,
    )

    match = re.match(r'Version: ImageMagick (\S+)', cmdresult.stdout.decode('utf-8'))
    if not match:
        raise EnvironmentError(f"Could not detect ImageMagick version from output of {cmdline}")

    version = match.group(1)
    if verbose:
        print(f"Found version: {version}", file=sys.stderr)

    scale = imagemagick_psnr_scale_from_version(version)
    DETECTED_SCALE = scale
    return scale