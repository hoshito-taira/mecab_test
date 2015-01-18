#!/usr/bin/python
# -*- coding: utf-8 -*-
#http://mecab.googlecode.com/svn/trunk/mecab/doc/posid.html
import MeCab
filteredPOS = [10, 11, 12, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]

def wordsvector(sentence):
  sentence = sentence.encode("utf-8") if isinstance(sentence,unicode) else sentence
  words = []
  tagger = MeCab.Tagger('')
  node = tagger.parseToNode(sentence)
  while node:
    fs = node.feature.split(",")
    if (node.surface is not None) and node.surface != "" :
    #if (node.surface is not None) and node.surface != "" and fs[0] in ['名詞']:
      words.append(node.surface)
    node = node.next
  return words

def featurevector(sentence):
  words = wordsvector(sentence)
  return dict([(w, 1) for w in words])
