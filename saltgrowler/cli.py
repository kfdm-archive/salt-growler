import logging
import argparse
import saltgrowler.core

parser = argparse.ArgumentParser()
parser.add_argument(
    '-v',
    '--verbose',
    action='store_const',
    default=logging.INFO,
    const=logging.DEBUG,
)


def main():
    args = parser.parse_args()
    # Reset the root handlers since salt does not play nicely like
    # typical libraries
    logging.root.handlers = []
    logging.basicConfig(level=args.verbose)
    # Even if we set additional debugging, we don't want to go lower than
    # INFO for the gntp library
    if args.verbose == logging.DEBUG:
        logging.getLogger('gntp').setLevel(logging.INFO)
    saltgrowler.core.EventReader().dispatcher()
