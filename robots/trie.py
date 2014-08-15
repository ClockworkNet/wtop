#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# author:         rex
# blog:           http://iregex.org
# filename        trie.py
# created:        2010-08-01 20:24
# source uri:     http://iregex.org/blog/trie-in-python.html

# Standard Library
import re


class Trie():
    """Regexp::Trie in python"""

    def __init__(self):
        self.data = dict()

    def add(self, word):
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or dict()
            ref = ref[char]
        ref[""] = 1

    def dump(self):
        return self.data

    def quote(self, char):
        return re.escape(char)

    def _regexp(self, pData):
        data = pData
        if "" in data and len(data.keys()) == 1:
            return None

        alt = list()
        cc = list()
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                try:
                    recurse = self._regexp(data[char])
                    alt.append(self.quote(char)+recurse)
                except:
                    cc.append(self.quote(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append("[%s]" % "".join(cc))

        if len(alt) == 1:
            result = alt[0]
        else:
            result = "(?:%s)" % "|".join(alt)

        if q:
            if cconly:
                result += "?"
            else:
                result = "(?:%s)?" % result
        return result

    def regexp(self):
        return self._regexp(self.dump())


if __name__ == '__main__':
    a = Trie()
    for w in ['foobar', 'foobah', 'fooxar', 'foozap', 'fooza']:
        a.add(w)
    print a.regexp()
