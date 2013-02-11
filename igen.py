#!/usr/bin/python

import os
import re
import marshal

# from collections import defaultdict

def doc_id(filename):
  name = filename.split(".")
  return int(name[0])

def get_doc_ids(dir):
  docs = [name for name in os.listdir(dir) if name.endswith(".txt")]
  doc_ids = {}
  for doc in docs:
    doc_ids[doc_id(doc)] = os.path.join(dir, doc)
  return doc_ids


def read_file(filename):
  f = open(filename, 'rU')
  # terms = re.sub(r"[^\w\s]*[_]*", " ", f.read().lower())
  terms = re.sub(r"[^\w\s]", " ", f.read().lower())
  return terms.split()


def generate_trigrams(term):
  k = 2
  trigrams = ["$" + term[0:k-1]]
  i = 0
  while i < len(term) - (k - 1):
    trigrams.append(term[i:i+k])
    i += 1
  trigrams.append(term[-(k-1):] + "$")
  return trigrams


def generate():
  dir = "books"
  doc_ids = get_doc_ids("books")
  index = {}
  kgram_index = {}

  for doc_id in doc_ids:
    terms = read_file(doc_ids[doc_id])
    i = 0
    while i < len(terms):
      w = terms[i]
      index[w] = (index.get(w) or {})
      index[w][doc_id] = (index[w].get(doc_id) or set())
      index[w][doc_id].add(i)
      i += 1
      for tri in generate_trigrams(w):
        kgram_index[tri] = kgram_index.get(tri) or set()
        kgram_index[tri].add(w)

  index_file = open("index.dat", "w")
  marshal.dump(index, index_file)
  index_file.close()

  kgram_file = open("kgram-index.dat", "w")
  marshal.dump(kgram_index, kgram_file)
  kgram_file.close()

  print "\n\nDone generating indices!"


# index structure:
# {term : {doc1:set(locations), doc2:set(locations), ....}}
