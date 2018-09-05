import argparse, sys
from . import pdfdiff

from .constants import DEFAULT_VERBOSITY, MAX_VERBOSITY

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
        help="silence output (can be used only once)")
    assert DEFAULT_VERBOSITY==1
    parser.add_argument('--verbose', '-v',
        action='count',
        default=0,
        help="show more information (can be used {} times)".format(
            MAX_VERBOSITY - DEFAULT_VERBOSITY))

    args = parser.parse_args()

    assert args.silent == 0 or args.verbose == 0, "cannot be silent and verbose"

    verbosity = DEFAULT_VERBOSITY + args.verbose - args.silent

    if pdfdiff(args.a, args.b, verbosity=verbosity):
        sys.exit(0)
    else:
        sys.exit(2)


if __name__ == '__main__':
    main()
