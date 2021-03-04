import argparse

from main import main

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true", help='tell mode')
group.add_argument("-q", "--quiet", action="store_true", help='quiet mode')
args = parser.parse_args()

tell = args.verbose or __debug__
main(v=tell)
