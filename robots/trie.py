#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#author:         rex
#blog:           http://iregex.org
#filename        tr.py
#created:        2010-08-01 20:24

class Trie():
    """Regexp::Trie in python"""
    def __init__(self):
        self.data={}

    def add(self, word):
        ref=self.data
        for char in word:
            ref[char]=ref.has_key(char) and ref[char] or {}
            ref=ref[char]
        ref['']=1

    def dump(self):
        return self.data

    def _regexp(self, pData):
        data=pData
        if data.has_key("") and len(data.keys())==1:
            return None

        alt=[]
        cc=[]
        q=0
        for char in sorted(data.keys()):
            if isinstance(data[char],dict):
                try:
                    recurse=self._regexp(data[char])
                    alt.append(char+recurse)
                except:
                    cc.append(char)
            else:
                q=1
        cconly=len(alt) and 0 or 1  #if len, 0; else:0

        if len(cc)>0:
            if len(cc)==1:
                alt.append(cc[0])
            else:
                alt.append('['+''.join(cc)+']')

        if len(alt)==1:
            result=alt[0]
        else:
            result="(?:"+"|".join(alt)+")"

        if q:
            if cconly:
                result+="?"
            else:
                result="(?:%s)?" % result
        return result
    def regexp(self):
        return "(?-xism:%s)" % self._regexp(self.dump())

a=Trie()

for w in ['foobar', 'foobah', 'fooxar', 'foozap', 'fooza']:
    a.add(w)
print a.regexp()
