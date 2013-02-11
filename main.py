#!/usr/bin/python

from __future__ import print_function
import sys, re, cmd
import gen, engn, timer

class Prompt(cmd.Cmd):
  """Search query interface"""

  engine = None
  store  = None
  prompt = "\nquery> "
  welcome = "\n### Welcome to Wael's search engine!\n### Enter your query to perform a search.\n### Enter '?' for help and 'exit' to terminate."


  def preloop(self):
    """Print intro message and write or load indices"""
    print(self.welcome)
    with timer.Timer() as t:
      self.store = gen.Store("books")
    print('> Request took %.03f sec.' % t.interval)


  def default(self, line):
    """Handle search query"""
    query = self.parse_query(line)
    if not self.engine: self.engine = engn.Engine(self.store)
    # search for query
    with timer.Timer() as t:
      answers = self.engine.search(query)

    if answers:
      print("\n> Found %d search results:" % len(answers), end=' ')
      for doc in answers: print(doc, end=' ')
      print()
    else:
      print("\n> Sorry, your search for: (%s) did not yield any results :(" % line)

    print('\n> Search took %.06f sec.' % t.interval)


  def parse_query(self, line):
    """Parse all three kinds of query terms into a dict"""
    query = {'bool': [], 'phrase': [], 'wild': []}
    line = re.sub(r'[_]|[^\w\s"*]', ' ', line.strip().lower())
    (query, line) = self.parse_wildcard(query, line)
    (query, line) = self.parse_phrase(query, line)
    (query, line) = self.parse_boolean(query, line)
    return query


  def parse_wildcard(self, query, line):
    """Extract wildcard queries into query{}"""
    wregex = r"([\w]+)?([\*])([\w]+)?"
    query['wild'] = re.findall(wregex, line)
    if query['wild']:
      line = re.sub(wregex, '', line)
      i = 0
      while i < len(query['wild']):
        query['wild'][i] = filter(len, query['wild'][i])
        i += 1
    return (query, line)


  def parse_phrase(self, query, line):
    """extract phrase query terms into query{}"""
    pregex = r'\w*"([^"]*)"'
    query['phrase'] = re.findall(pregex, line)
    if query['phrase']: line = re.sub(pregex, '', line)
    return (query, line)


  def parse_boolean(self, query, line):
    """ consider whatever is left as boolean query terms"""
    query['bool'] = line.split()
    return (query, line)


  def emptyline(self):
    """Called when user doesn't enter anything"""
    print("\n> Enter your search query or type '?' for help.")


  def do_exit(slef, line):
    """Type 'exit' to terminate the program"""
    return True


  def do_EOF(self, line):
    print() # print new line for prettier exits
    return True


def main():
  Prompt().cmdloop()

if __name__ == '__main__':
  main()
