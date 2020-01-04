# Find the right command to use for a program.

import os, sys, subprocess
from subprocess import DEVNULL
from typing import List

_COMPARE_CMD = None


def compare_cmd(print_cmds: bool) -> List[str]:
    """Find the command to use for ImageMagick compare."""
    global _COMPARE_CMD

    if _COMPARE_CMD != None:
        # Memoized
        return _COMPARE_CMD

    env_compare = os.environ.get("COMPARE", None)

    # Try to find where the command is.
    result_cmd = None
    for attempt in [
        env_compare,
        "compare",
        "magick compare",
    ]:
        # Does it work?
        if attempt == None:
            continue
        attempt_cmd = attempt.split(" ")
        try:
            processresult = verbose_run(
                print_cmds, attempt_cmd + ["-version"], stdout=DEVNULL, stderr=DEVNULL
            )
        except FileNotFoundError:
            continue
        else:
            if processresult.returncode == 0:
                result_cmd = attempt_cmd
                break

    if result_cmd == None:
        cur_val = repr(env_compare) if env_compare != None else "unset"
        raise Exception(
            " ".join(
                line.strip()
                for line in """ 
            Cannot find ImageMagick's compare program. Is ImageMagick installed?
            If so, you can try setting environment variable COMPARE
            to the complete path of the compare executable. Environment variable
            COMPARE is currently: {} .
            """.strip()
                .format(cur_val)
                .splitlines()
            )
        )

    else:
        _COMPARE_CMD = result_cmd
        return result_cmd


def verbose_run(print_cmd, args, *restargs, **kw):
    if print_cmd:
        print("  Running: {}".format(" ".join(args)), file=sys.stderr)
    return subprocess.run(args, *restargs, **kw)
