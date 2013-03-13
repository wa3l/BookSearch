#!/usr/bin/python

"""
Book Search
Module: engn
Author: Wael Al-Sallami
Date: 2/10/2013
"""

class Engine:
  """The search engine"""

  store = None
  query = {}

  def __init__(self, store):
    """Save a pointer to our indices"""
    self.store = store


  def search(self, query):
    """Perform any search and return results"""
    self.query = query
    answers = wanswers = []
    answers    = self.get_boolean_answers(answers)
    answers    = self.get_phrase_answers(answers)
    wanswers   = self.get_wildcard_answers(wanswers)
    if wanswers: answers.append(set.intersection(*wanswers))
    if answers: return set.intersection(*answers)


  def get_boolean_answers(self, answers):
    """Get boolean answers and append them to the overall list of answers"""
    if self.query["bool"]:
      boolean = self.boolean_search(self.query["bool"])
      if boolean: answers.append(boolean)
    return answers


  def get_phrase_answers(self, answers):
    """Get phrase answers and append them to the overall list of answers"""
    for phrase in self.query["phrase"]:
      phrase = self.phrase_search(phrase)
      if phrase: answers.append(phrase)
    return answers


  def get_wildcard_answers(self, answers):
    """perform wildcard search given a list of wildcards"""
    terms = []
    for q in self.query['wild']:
      bigrams = self.process_wildcard(q)
      subset  = self.wildcard_terms(bigrams)
      if subset: terms.append(subset)

    for card in terms:
      subset = set()
      for t in card:
        results = set(self.store.index[t].keys())
        if not subset: subset = results.copy()
        subset |= results
      answers.append(subset)
    return answers


  def boolean_search(self, query):
    """Perform a boolean search given a list of terms"""
    terms_docs = []
    for term in query:
      if term not in self.store.index: return None
      docs = set()
      for doc in self.store.index[term].keys():
        docs.add(doc)
      terms_docs.append(docs)
    return set.intersection(*terms_docs)


  def positional_search(self, docs, terms):
    """Perform a positional search given a list of docs and terms"""
    answers = set()
    for doc in docs:
      base_pos = self.store.index[terms[0]][doc]
      for pos in base_pos:
        i = 1
        found = True
        while i < len(terms):
          if pos + i not in self.store.index[terms[i]][doc]:
            found = False
            break
          i += 1
        if found:
          answers.add(doc)
    return answers


  def phrase_search(self, query):
    """Perform a phrase search"""
    terms = query.split()
    docs = self.boolean_search(terms)
    if docs is None: return
    return self.positional_search(docs, terms)


  def wildcard_terms(self, bigrams):
    """Given a list of bigrams, return union of their terms"""
    terms = set()
    for tri in bigrams:
      inter = set()
      if tri in self.store.kindex:
        inter = self.store.kindex[tri]
      if not terms: terms = inter.copy()
      terms = terms & inter
    if terms: return terms


  def process_wildcard(self, cards):
    """Generate a wildcard's bigrams"""
    middle = (len(cards) == 3)
    bigrams = []
    if cards[0] == '*':
      bigrams.extend(self.bigrams(cards[1], 'end'))
    elif cards[1] == '*' and middle:
      bigrams.extend(self.bigrams(cards[0], 'start'))
      bigrams.extend(self.bigrams(cards[2], 'end'))
    else:
      bigrams.extend(self.bigrams(cards[0], 'start'))
    return bigrams


  def bigrams(self, term, pos):
    """Generate bigrams for wildcard subset"""
    k = 2
    bigrams = []
    if pos == 'start': bigrams.append("$" + term[0:k-1])
    i = 0
    while i < len(term) - (k - 1):
      bigrams.append(term[i:i+k])
      i += 1
    if pos == 'end': bigrams.append(term[-(k-1):] + "$")
    return [t for t in bigrams if len(t) == k]

