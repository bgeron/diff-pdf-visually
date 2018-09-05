import argparse, sys
from . import pdfdiff

def main():

    description = """
    Compare two PDFs visually. The exit code is 0 if they are the same, and 2
    if there are significant differences.
    """.strip()

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('a', metavar='a.pdf')
    parser.add_argument('b', metavar='b.pdf')

    args = parser.parse_args()
    if pdfdiff(args.a, args.b):
        sys.exit(0)
    else:
        sys.exit(2)


if __name__ == '__main__':
    main()
