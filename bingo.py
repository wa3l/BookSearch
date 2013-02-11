#!/usr/bin/python

import sys
import os
import igen
import srch


def main():
  if len(sys.argv) == 1:
    print 'usage: ./bingo.py query'
    sys.exit(1)

  args = sys.argv[1:]

  if args[0] == "--generate-index":
    igen.generate();
    sys.exit(1)
  elif not os.path.exists("index.dat"):
    print "\nError: Please generate the index before querying the system."
    print 'Usage: ./bingo.py --generate-index'
    sys.exit(1)

  results = srch.find(args)
  if results is None:
    print "\nSorry, no search results were found!"
  else:
    print results

if __name__ == '__main__':
  main()
