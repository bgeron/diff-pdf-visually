import argparse, sys
from . import pdfdiff

from .constants import DEFAULT_THRESHOLD, DEFAULT_VERBOSITY, DEFAULT_DPI
from .constants import MAX_VERBOSITY, VERB_WARN_SANITY

def main():

    description = """
    Compare two PDFs visually. The exit code is 0 if they are the same, and 2
    if there are significant differences.
    """.strip()

    parser = argparse.ArgumentParser(description=description)

    verbosity = DEFAULT_VERBOSITY

    def more_silent():
        assert verbosity <= DEFAULT_VERBOSITY, "cannot be both silent and verbose"
        verbosity -= 1
    def more_verbose():
        assert verbosity >= DEFAULT_VERBOSITY, "cannot be both silent and verbose"
        verbosity += 1

    parser.add_argument('a', metavar='a.pdf')
    parser.add_argument('b', metavar='b.pdf')
    parser.add_argument('--silent', '-q',
        action='count',
        default=0,
        help="silence output (can be used only once); the result can be found "
             "in the exit code")
    assert DEFAULT_VERBOSITY==1
    parser.add_argument('--verbose', '-v',
        action='count',
        default=0,
        help="show more information (can be used {} times)".format(
            MAX_VERBOSITY - DEFAULT_VERBOSITY))
    parser.add_argument('--threshold',
        default=DEFAULT_THRESHOLD,
        type=float,
        help="PSNR threshold to consider a change significant, "
             "higher is more sensitive (default: %(default)s)")
    parser.add_argument('--dpi',
        default=DEFAULT_DPI,
        type=int,
        help="resolution for the rasterised files (default: %(default)s)")
    parser.add_argument('--time',
        default=0,
        type=int,
        help="number of seconds to wait before discarding temporary files, "
             "or 0 to immediately discard")

    args = parser.parse_args()

    assert args.silent == 0 or args.verbose == 0, "cannot be silent and verbose"
    assert 1 <= args.dpi

    verbosity = DEFAULT_VERBOSITY + args.verbose - args.silent

    if verbosity >= VERB_WARN_SANITY:
        if not args.a[-4:].lower() == ".pdf":
            print("Warning: {!r} does not end in .pdf.".format(args.a))
        if not args.b[-4:].lower() == ".pdf":
            print("Warning: {!r} does not end in .pdf.".format(args.b))

    if pdfdiff(args.a, args.b,
            verbosity=verbosity,
            threshold=args.threshold,
            dpi=args.dpi,
            time_to_inspect=args.time):
        sys.exit(0)
    else:
        sys.exit(2)


if __name__ == '__main__':
    main()
