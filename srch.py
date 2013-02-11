#!/usr/bin/python

# 19, 23, 203

import os
import marshal
import re

def load_index():
  index_file = open("index.dat")
  index = marshal.load(index_file)
  index_file.close()
  return index

def load_wildcard_index():
  index_file = open("kgram-index.dat")
  index = marshal.load(index_file)
  index_file.close()
  return index

def boolean_find(query, index):
  terms_docs = []
  for term in query:
    if term not in index: return None
    docs = set()
    for doc in index[term].keys():
      docs.add(doc)
    terms_docs.append(docs)

  return set.intersection(*terms_docs)


def positional_find(index, docs, terms):
  answers = set()
  for doc in docs:
    base_pos = index[terms[0]][doc]
    for pos in base_pos:
      i = 1
      found = True
      while i < len(terms):
        if pos + i not in index[terms[i]][doc]:
          found = False
          break
        i += 1
      if found:
        answers.add(doc)

  return answers


def phrase_find(query, index):
  terms = query.split()
  docs = boolean_find(terms, index)
  if docs is None: return
  answers = positional_find(index, docs, terms)
  return answers

def get_trigrams(term, pos):
  k = 2
  trigrams = []
  if pos == 'start': trigrams.append("$" + term[0:k-1])
  i = 0
  while i < len(term) - (k - 1):
    trigrams.append(term[i:i+k])
    i += 1
  if pos == 'end': trigrams.append(term[-(k-1):] + "$")
  return [t for t in trigrams if len(t) == k]

def process_wildcard(wildcard):
  cards = []
  i = 1
  while i <= 3:
    if wildcard.group(i) is not None: cards.append(wildcard.group(i))
    i += 1
  middle = (len(cards) == 3)
  trigrams = []
  if cards[0] == '*':
    trigrams.extend(get_trigrams(cards[1], 'end'))
  elif cards[1] == '*' and middle:
    trigrams.extend(get_trigrams(cards[0], 'start'))
    trigrams.extend(get_trigrams(cards[2], 'end'))
  else:
    trigrams.extend(get_trigrams(cards[0], 'start'))
  # print trigrams
  return trigrams

def get_wildcard_terms(index, trigrams):
  terms = set()
  for tri in trigrams:
    inter = set()
    if tri in index: inter = index[tri]
    if not terms: terms = inter.copy()
    terms = terms & inter
  if terms:
    print terms
    return terms


def find(query):
  """
  iterate over query terms, decide what type of term is it and add it to a
  list of that type's terms, process each type and return an interesected
  set. All intersected sets from the 3 types of queries are then intersected
  to return the result to main()
  """

  answers = []
  wildcard_answers = []
  queries = {'wild': [], 'phrase': [], 'bool': []}
  index = load_index()

  i = 0
  for q in query:
    wild  = re.search(r"([\w]+)?([\*])([\w]+)?", q)
    terms = re.findall(r"\w+", q)

    if wild:
      trigrams       = process_wildcard(wild)
      kgram_index    = load_wildcard_index()
      wildcard_terms = get_wildcard_terms(kgram_index, trigrams)
      if wildcard_terms:
        queries["wild"].append(wildcard_terms)
    else:
      if len(terms) > 1:
        queries["phrase"].append(q)
      else:
        queries["bool"].append(q)

  if queries["bool"]:
    boolean = boolean_find(queries["bool"], index)
    if boolean: answers.append(boolean)

  for t in queries["phrase"]:
    phrase = phrase_find(t, index)
    if phrase: answers.append(phrase)

  for termset in queries["wild"]:
    inter = set()
    for t in termset:
      results = set(index[t].keys())
      if not inter: inter = results.copy()
      inter |= results
    wildcard_answers.append(inter)

  if wildcard_answers: answers.append(set.intersection(*wildcard_answers))

  # if no bool and no phrase, return all wild answers intersected with other wild answers
  if answers: return set.intersection(*answers)

