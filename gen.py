#!/usr/bin/python

import os, re, gzip, marshal, timer

class Store:
  """The data store"""

  index  = {}
  kindex = {}
  index_name   = "index.dat"
  kindex_name  = "kindex.dat"


  def __init__(self, dir):
    """Build index, store index and kgram index"""
    if self.indices_present():
      self.load_indices()
    else:
      print "\n> Writing indices! This only happens once, please wait ..."
      self.build_indices(dir)


  def build_indices(self, dir):
    """Build positional and kgram indices"""
    documents = self.get_documents(dir)
    for d in documents:
      terms = self.tokenize(documents[d])
      i = 0
      for w in terms:
        if w not in self.index: self.index[w] = {}
        if d not in self.index[w]: self.index[w][d] = set()
        self.index[w][d].add(i)
        i += 1

    for w in self.index.keys():
      for tri in self.bigrams(w):
        if tri not in self.kindex: self.kindex[tri] = set()
        self.kindex[tri].add(w)

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
    if not self.index or not self.kindex:
      print "\n> Reading indices! This happens once per session, please wait ..."
    if not self.index:
      self.load_index()
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


  def get_documents(self, dir):
    """Search for txt files only, return dict of {doc-name: doc-path}"""
    names = [name for name in os.listdir(dir) if name.endswith(".txt")]
    documents = {}
    for name in names:
      documents[name.split(".")[0]] = os.path.join(dir, name)
    return documents


  def bigrams(self, term):
    """Build all possible bigrams for term"""
    k = 2
    i = 0
    bigrams = ["$" + term[0:k-1]]
    while i < len(term) - (k - 1):
      bigrams.append(term[i:i+k])
      i += 1
    bigrams.append(term[-(k-1):] + "$")
    return bigrams


  def tokenize(self, filename):
    """Read document and return its tokens/terms"""
    f = open(filename, 'rU')
    terms = re.sub(r'[_]|[^\w\s]', ' ', f.read().lower())
    f.close()
    return terms.split()

