#!/usr/bin/env python
#-*- coding: utf-8 -*-
import nltk
import MeCab
import mecabsplitter as splitter
import math, sys
import urllib2
from urllib2 import HTTPError
from itertools import chain
from bs4 import BeautifulSoup

areas = [
  "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
  "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
  "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県",
  "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山",
  "鳥取県", "島根県", "岡山県", "広島県", "山口県",
  "徳島県", "香川県", "愛媛県", "高知県",
  "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

#def tfidf(doc,docs):
#  """対象の文書と全文の形態素解析した単語リストを指定すると対象の文書のTF-IDFを返す"""
#  tokens = list(chain.from_iterable(docs)) #flatten
#  A = nltk.TextCollection(docs)
#  token_types = set(tokens)
#  return [{"word":token_type,"tfidf":A.tf_idf(token_type, doc)} for token_type in token_types]
def cos(d1, d2):
  v1 = splitter.wordsvector(d1)
  v2 = splitter.wordsvector(d2)
  intersec = set(v1).intersection(set(v2))
  return len(intersec) / (math.sqrt(len(set(v1))) * math.sqrt(len(set(v2))))

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
      return plain_text
      #words = extract_words(plain_text)
      #return words
    docs = [url2words(i) for i in range(1, 48)]
    for i in range(0, len(docs)):
      print areas[i]
      cos_sim = []
      for j in range(0, len(docs)):
        cos_sim.append({ "area" : areas[j], "cos" : cos(docs[i], docs[j])})
      cos_sim.sort(cmp=lambda x,y:cmp(x["cos"],y["cos"]),reverse=True)
      for r in cos_sim:
        print "{ area : %s, cos : %s }" % (r["area"], r["cos"])
      print '------------------'
    #docs = [url2words(url) for url in urls]
    #for i in range(0,len(docs)):
    #  tfidfs = tfidf(docs[i],docs)
    #  tfidfs.sort(cmp=lambda x,y:cmp(x["tfidf"],y["tfidf"]),reverse=True)
    #  result = [e for i,e in enumerate(tfidfs)]
    #  for r in result:
    #    print "{ word : %s, tfidf : %s }" % (r["word"], r["tfidf"])
    #  print "------------------------"

if __name__ == '__main__':
  unittest.main()
