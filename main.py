#!/usr/bin/python

"""
BookSearch
Module: main
Author: Wael Al-Sallami
Date: 2/10/2013
"""

import sys, re, cmd, gen, engn, timer

class Prompt(cmd.Cmd):
  """Search query interface"""

  engine  = None
  store   = None
  line    = None
  prompt  = "\nquery> "
  welcome = "\n### Welcome to BookSearch!\n### Enter your query to perform a search.\n### Enter '?' for help and 'exit' to terminate."


  def preloop(self):
    """Print intro message and write or load indices"""
    print self.welcome
    with timer.Timer() as t:
      self.store = gen.Store("books")
    print '> Request took %.03f sec.' % t.interval


  def default(self, line):
    """Handle search query"""
    query = self.parse_query(line)
    with timer.Timer() as t:
      if not self.engine:
        self.engine = engn.Engine(self.store)
      answers = self.engine.search(query)
      self.print_answers(answers)
    print '\n> Search took %.06f sec.' % t.interval


  def parse_query(self, line):
    """Parse all three kinds of query terms into a dict"""
    query = {'bool': [], 'phrase': [], 'wild': []}
    self.line  = re.sub(r'[_]|[^\w\s"*]', ' ', line.strip().lower())
    query = self.parse_wildcard(query)
    query = self.parse_phrase(query)
    query = self.parse_boolean(query)
    return query


  def parse_wildcard(self, query):
    """Extract wildcard queries into query{}"""
    regex = r"([\w]+)?([\*])([\w]+)?"
    query['wild'] = re.findall(regex, self.line)
    if query['wild']:
      self.line = re.sub(regex, '', self.line)
      for i in range(len(query['wild'])):
        query['wild'][i] = filter(len, query['wild'][i])
    return query


  def parse_phrase(self, query):
    """extract phrase query terms into query{}"""
    regex = r'\w*"([^"]*)"'
    query['phrase'] = re.findall(regex, self.line)
    if query['phrase']:
      self.line = re.sub(regex, '', self.line)
    return query


  def parse_boolean(self, query):
    """Consider whatever is left as boolean query terms"""
    query['bool'] = self.line.split()
    return query


  def print_answers(self, answers):
    """Print search results"""
    if answers:
      print "\n> Found %d search results:" % len(answers),
      for doc in answers: print doc,
    else:
      print "\n> Sorry, your search for: (%s) did not yield any results :(" % line


  def emptyline(self):
    """Called when user doesn't enter anything"""
    print "\n> Enter your search query or type '?' for help."


  def do_exit(slef, line):
    """Type 'exit' to terminate the program"""
    return True


  def do_EOF(self, line):
    print '' # print new line for prettier exits
    return True


def main():
  Prompt().cmdloop()

if __name__ == '__main__':
  main()
