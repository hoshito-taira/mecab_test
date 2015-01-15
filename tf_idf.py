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
    #urls = ["http://ja.wikipedia.org/wiki/Tf-idf"]
    urls = [
      "http://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=沖縄県&rvprop=content",
      "http://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=茨城県&rvprop=content",
      "http://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=栃木県&rvprop=content",
      "http://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=群馬県&rvprop=content",
      "http://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=埼玉県&rvprop=content",
      "http://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=千葉県&rvprop=content",
      "http://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=東京都&rvprop=content",
      "http://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=神奈川県&rvprop=content"
    ]
    def url2words(url):
      try:
        html = urllib2.urlopen(url).read()
      except HTTPError:
        html = ""
      soup = BeautifulSoup(html)
      plain_text = soup.get_text().encode("utf-8")
      words = extract_words(plain_text)
      return words
    docs = [url2words(url) for url in urls]
    print len(docs)
    tfidfs = tfidf(docs[0],docs)
    tfidfs.sort(cmp=lambda x,y:cmp(x["tfidf"],y["tfidf"]),reverse=True)
    result = [e for i,e in enumerate(tfidfs) if len(e["word"]) > 2 and i < 30]
    for r in result:
      print "{ word : %s, tfidf : %s }" % (r["word"], r["tfidf"])

if __name__ == '__main__':
  unittest.main()
