#!/usr/bin/python

"""
Book Search
Module: gen
Author: Wael Al-Sallami
Date: 2/10/2013
"""

import os, re, gzip, marshal, timer

class Store:
  """The data store"""

  index  = {}
  kindex = {}
  kgrams_length = 2
  index_name    = "index.dat"
  kindex_name   = "kindex.dat"


  def __init__(self, dir):
    """Build index, store index and kgram index"""
    if self.indices_present():
      self.load_indices()
    else:
      print "\n> Writing indices! This only happens once, please wait ..."
      self.build_indices(dir)


  def build_indices(self, dir):
    """Build positional and kgram indices"""
    doc_terms = self.get_doc_terms(dir)
    self.build_index(doc_terms)
    self.build_kindex()
    self.save_indices()


  def build_index(self, doc_terms):
    """Build the positional index based on documents"""
    for d in doc_terms:
      i = 0
      for t in doc_terms[d]:
        if t not in self.index: self.index[t] = {}
        if d not in self.index[t]: self.index[t][d] = set()
        self.index[t][d].add(i)
        i += 1


  def build_kindex(self):
    """Build the k-gram index based on terms"""
    for w in self.index.keys():
      for g in self.kgrams(w):
        if g not in self.kindex: self.kindex[g] = set()
        self.kindex[g].add(w)


  def load_indices(self):
    """Loads indices into memory"""
    if not self.index or not self.kindex:
      print "\n> Reading indices! This happens once per session, please wait ..."
    if not self.index:  self.load_index()
    if not self.kindex: self.load_kindex()


  def load_index(self):
    """Loads positional index into memory"""
    index_file = open(self.index_name)
    self.index = marshal.load(index_file)
    index_file.close()


  def load_kindex(self):
    """Loads kgram index into memory"""
    index_file  = open(self.kindex_name)
    self.kindex = marshal.load(index_file)
    index_file.close()


  def save_indices(self):
    """Save positional and kgram indices to disk"""
    index_file = open(self.index_name, "w")
    marshal.dump(self.index, index_file)
    index_file.close()

    kgram_file = open(self.kindex_name, "w")
    marshal.dump(self.kindex, kgram_file)
    kgram_file.close()


  def indices_present(self):
    """Return True if indices are present on disk"""
    if os.path.exists(self.index_name) and os.path.exists(self.kindex_name):
      return True


  def get_doc_terms(self, dir):
    """Search for txt files only, return dict of {doc-name: doc-path}"""
    names = [name for name in os.listdir(dir) if name.endswith(".txt")]
    doc_terms = {}
    for name in names:
      doc_terms[name.split(".")[0]] = self.tokenize(os.path.join(dir, name))
    return doc_terms


  def kgrams(self, term):
    """Build all possible kgrams for term"""
    k = self.kgrams_length
    kgrams = ["$" + term[0:k-1]]
    for i in range(len(term) - (k-1)):
      kgrams.append(term[i:i+k])
    kgrams.append(term[-(k-1):] + "$")
    return kgrams


  def tokenize(self, filename):
    """Read document and return its tokens/terms"""
    f = open(filename, 'rU')
    terms = re.sub(r'[_]|[^\w\s]', ' ', f.read().lower())
    f.close()
    return terms.split()

