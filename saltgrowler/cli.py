import logging
import argparse
import saltgrowler.core

logging.getLogger('gntp')

parser = argparse.ArgumentParser()
parser.add_argument(
    '-v',
    '--verbose',
    action='store_const',
    default=logging.WARNING,
    const=logging.INFO,
)

def main():
    args = parser.parse_args()
    # Reset the root handlers since salt does not play nicely like
    # typical libraries
    logging.root.handlers = []
    logging.basicConfig(level=args.verbose)
    saltgrowler.core.EventReader().dispatcher()
