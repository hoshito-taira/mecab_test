#!/usr/bin/env python
#-*- coding: utf-8 -*-
import nltk
import MeCab
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

def tfidf(doc,docs):
  tokens = list(chain.from_iterable(docs))
  A = nltk.TextCollection(docs)
  token_types = set(tokens)
  return [{"word":token_type,"tfidf":A.tf_idf(token_type, doc)} for token_type in token_types]


def extract_words(text):
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

# 標準出力でTF-IDFを返却
if __name__ == '__main__':
  def url_words(num):
    plain_text = open("47area/area_" + str(num) + "/AA/wiki_00", "r").read()
    words = extract_words(plain_text)
    return words

  docs = [url_words(i) for i in range(1, 48)]
  print "{["
  c_flag = True
  for i in range(0,len(docs)):
    if c_flag :
      print "{"
      c_flag = False
    else :
      print ",{"
    print '"word" : "%s", "children" : [' % areas[i];
    tfidfs = tfidf(docs[i],docs)
    tfidfs.sort(cmp=lambda x,y:cmp(x["tfidf"],y["tfidf"]),reverse=True)
    result = [e for i,e in enumerate(tfidfs)]
    cc_flag = True
    for r in result:
      if r["tfidf"] > 0 :
        if cc_flag :
          print '{ "word" : "%s", "tfidf" : %s }' % (r["word"], r["tfidf"])
          cc_flag = False
        else :
          print ',{ "word" : "%s", "tfidf" : %s }' % (r["word"], r["tfidf"])
    print "]}"
  print "]}"
