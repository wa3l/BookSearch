#!/usr/bin/python

import os
import re
import marshal

class Store:

  index  = {}
  kindex = {}
  index_name   = "index.dat"
  kindex_name  = "kindex.dat"


  def __init__(self, dir):
    """Generate index, store index and kgram index"""
    if self.indices_present():
      self.load_indices()
    else:
      self.generate_indices(dir)


  def generate_indices(self, dir):
    """Generate positional and kgram indices"""
    documents = self.get_documents(dir)
    # generate indices
    for d in documents:
      terms = self.tokenize(documents[d])
      i = 0
      while i < len(terms):
        w = terms[i]
        self.index[w]    = self.index.get(w) or {}
        self.index[w][d] = self.index[w].get(d) or set()
        self.index[w][d].add(i)
        i += 1
        for tri in self.trigrams(w):
          self.kindex[tri] = self.kindex.get(tri) or set()
          self.kindex[tri].add(w)
    # save indices
    self.save_indices()


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


  def load_indices(self):
    """Loads indices into memory"""
    if not self.index:  self.load_index()
    if not self.kindex: self.load_kindex()


  def load_index(self):
    """Loads positional index into memory"""
    index_file = open(self.index_name)
    self.index = marshal.load(index_file)
    index_file.close()


  def load_kindex(self):
    """Loads kgram index into memory"""
    index_file = open(self.kindex_name)
    index = marshal.load(index_file)
    index_file.close()


  def get_documents(self, dir):
    """Search for txt files only, return dict of {doc-name: doc-path}"""
    names = [name for name in os.listdir(dir) if name.endswith(".txt")]
    documents = {}
    for name in names:
      documents[name.split(".")[0]] = os.path.join(dir, name)
    return documents


  def trigrams(self, term):
    """Generate all possible trigrams for term"""
    k = 2
    i = 0
    trigrams = ["$" + term[0:k-1]]
    while i < len(term) - (k - 1):
      trigrams.append(term[i:i+k])
      i += 1
    trigrams.append(term[-(k-1):] + "$")
    return trigrams


  def tokenize(self, filename):
    """Read document and return its tokens/terms"""
    f = open(filename, 'rU')
    # terms = re.sub(r"[^\w\s]*[_]*", " ", f.read().lower())
    terms = re.sub(r"[^\w\s]", " ", f.read().lower())
    return terms.split()

