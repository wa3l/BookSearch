#!/usr/bin/python

from __future__ import print_function
import sys, re, cmd
import gen, engn

class Prompt(cmd.Cmd):
  """Search query interface"""

  engine = None
  prompt = "\nquery> "
  intro = "\nWelcome to Wael's search engine!\nPlease type your query to perform a search.\nType '?' for help and 'exit' to terminate"


  def default(self, line):
    """Handle search query"""
    query = self.parse_query(line)

    if not self.engine:
      store = gen.Store("books")
      self.engine = engn.Engine(store)
    # search for query
    answers = self.engine.search(query)
    if answers:
      print("\nFound %d search results:" % len(answers), end=' ')
      for doc in answers: print(doc, end=' ')
      print()
    else:
      print("Sorry, your search for: %s did not yield any answers" % line)


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
    pregex = r'"(\w+\s?\w*)"'
    query['phrase'] = re.findall(pregex, line)
    if query['phrase']: line = re.sub(pregex, '', line)
    return (query, line)


  def parse_boolean(self, query, line):
    """ consider whatever left as boolean query terms"""
    query['bool'] = line.split()
    return (query, line)


  def emptyline(self):
    """Called when user doesn't enter anything"""
    print("\nEnter your search query or type '?' for help")


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
