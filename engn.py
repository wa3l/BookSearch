#!/usr/bin/python

"""
BookSearch
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
      kgrams = self.process_wildcard(q)
      subset = self.wildcard_terms(kgrams)
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
      if term not in self.store.index: return
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
        found = True
        for i in range(1, len(terms)):
          if (pos + i) not in self.store.index[terms[i]][doc]:
            found = False
            break
        if found: answers.add(doc)
    return answers


  def phrase_search(self, query):
    """Perform a phrase search"""
    terms = query.split()
    docs = self.boolean_search(terms)
    if docs:
      return self.positional_search(docs, terms)


  def wildcard_terms(self, kgrams):
    """Given a list of kgrams, return union of their terms"""
    terms = set()
    for g in kgrams:
      inter = set()
      if g in self.store.kindex:
        inter = self.store.kindex[g]
      if not terms: terms = inter.copy()
      terms &= inter
    return terms


  def process_wildcard(self, cards):
    """Generate a wildcard's kgrams"""
    middle = (len(cards) == 3)
    kgrams = []
    if cards[0] == '*':
      kgrams.extend(self.kgrams(cards[1], 'end'))
    elif cards[1] == '*' and middle:
      kgrams.extend(self.kgrams(cards[0], 'start'))
      kgrams.extend(self.kgrams(cards[2], 'end'))
    else:
      kgrams.extend(self.kgrams(cards[0], 'start'))
    return kgrams


  def kgrams(self, term, pos):
    """Generate kgrams for wildcard subset"""
    k = self.store.kgrams_length
    kgrams = []
    if pos == 'start':
      kgrams.append("$" + term[0:k-1])

    for i in range(len(term) - (k-1)):
      kgrams.append(term[i:i+k])

    if pos == 'end':
      kgrams.append(term[-(k-1):] + "$")
    return [t for t in kgrams if len(t) == k]

