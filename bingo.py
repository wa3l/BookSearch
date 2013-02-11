#!/usr/bin/python

import sys
import os
# import igen
# import srch
import cmd
import gen

class Prompt(cmd.Cmd):
  engine = None

  """Search query processor"""
  intro = "\nWelcome to Wael's search engine!\nPlease type your query to perform a search.\nType '?' for help and 'exit' to terminate"
  prompt = "\nquery> "

  def default(self, line):
    if not self.engine:
      store = gen.Store("books")
      self.engine = 1
      # self.engine = engn.Engine(store)
    # search for query
    # self.engine.search(line)
    print "You searched for: %s" % line

  def emptyline(self):
    print "\nEnter your search query or type '?' for help"

  def do_exit(slef, line):
    """Type 'exit' to terminate the program"""
    return True

  def do_EOF(self, line):
    print # print new line for prettier exits
    return True

def main():
  Prompt().cmdloop()

  # elif not os.path.exists("index.dat"):
  #   print "\nError: Please generate the index before querying the system."

  # results = srch.find(args)
  # if results is None:
  #   print "\nSorry, no search results were found!"
  # else:
  #   print results

if __name__ == '__main__':
  main()
