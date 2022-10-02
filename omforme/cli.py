"""CLI interface for single view visualization mapping parameter values to an area scale resembling a (quality) pie."""
import argparse
import sys

import omforme.omforme as api
from omforme import APP_ALIAS, APP_NAME


def parse_request(argv: list[str]) -> int | argparse.Namespace:
    """DRY."""
    parser = argparse.ArgumentParser(
        prog=APP_ALIAS, description=APP_NAME, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--quiet',
        '-q',
        dest='quiet',
        default=False,
        action='store_true',
        help='work as quiet as possible (default: False)',
    )
    parser.add_argument(
        '--verbose',
        '-v',
        dest='verbose',
        default=False,
        action='store_true',
        help='work logging more information along the way (default: False)',
    )
    if not argv:
        parser.print_help()
        return 0

    options = parser.parse_args(argv)

    if options.verbose and options.quiet:
        parser.error('you cannot be quiet and verbose at the same time')

    return options


def main(argv: list[str] | None = None) -> int:
    """Delegate processing to functional module."""
    argv = sys.argv[1:] if argv is None else argv
    options = parse_request(argv)
    if isinstance(options, int):
        return 0
    return api.main(options)
