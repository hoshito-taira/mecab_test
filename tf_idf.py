#!/usr/bin/env python
#-*- coding: utf-8 -*-
import nltk
import MeCab
import urllib2
from urllib2 import HTTPError
from itertools import chain
from bs4 import BeautifulSoup

def tfidf(doc,docs):
  """対象の文書と全文の形態素解析した単語リストを指定すると対象の文書のTF-IDFを返す"""
  tokens = list(chain.from_iterable(docs)) #flatten
  A = nltk.TextCollection(docs)
  token_types = set(tokens)
  return [{"word":token_type,"tfidf":A.tf_idf(token_type, doc)} for token_type in token_types]


def extract_words(text):
  """テキストを与えると名詞のリストにして返す"""
  text =  text.encode("utf-8") if isinstance(text,unicode) else text
  mecab = MeCab.Tagger("")
  node = mecab.parseToNode(text)
  words = []
  while node:
    fs = node.feature.split(",")
    if (node.surface is not None) and node.surface != "" and fs[0] in ['名詞']:
      words.append(node.surface)
    node = node.next
  return words

import unittest

class MachineLearningTest(unittest.TestCase):
  def test_tfidf(self):
    """tfidfのテスト"""
    def url2words(num):
      plain_text = open("47area/area_" + str(num) + "/AA/wiki_00", "r").read()
      #try:
      #  html = urllib2.urlopen(url).read()
      #except HTTPError:
      #  html = ""
      #soup = BeautifulSoup(html)
      #plain_text = soup.get_text().encode("utf-8")
      words = extract_words(plain_text)
      return words
    docs = [url2words(i) for i in range(1, 48)]
    #docs = [url2words(url) for url in urls]
    for i in range(0,len(docs)):
      tfidfs = tfidf(docs[i],docs)
      tfidfs.sort(cmp=lambda x,y:cmp(x["tfidf"],y["tfidf"]),reverse=True)
      result = [e for i,e in enumerate(tfidfs)]
      for r in result:
        print "{ word : %s, tfidf : %s }" % (r["word"], r["tfidf"])
      print "------------------------"

if __name__ == '__main__':
  unittest.main()
