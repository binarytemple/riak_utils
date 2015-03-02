#!/usr/bin/env python
"""
This code reads a Riak ringfile then outputs the list of custom buckets and their properties.

"""

import sys
from py_interface import erl_term

sys.setrecursionlimit(1500)


TODO: rewrite the code which selects the input filename

f=open(fn,'rb')
content=f.read()
conv=erl_term.BufToTerm(content)

def recur(o,ret):
    #print "TYPE %s" % type(o)
    for i in o:
        if type(i) == tuple:
            recur(list(i),ret)
            #print "List item %s" % i
        elif type(i) == list and len(i) == 1 and type(i[0][0]) is tuple:
            #print "potential>>>>>>>>"
            ret.append(i)
        else:
            #print "other>>>"
            #print i
            pass

ret = []
recur(conv[0],ret)

bd={}
print "finished"
for i in ret:
    name=i[0][0][1].contents  #.atomText# == "bucket":
    bd[name] = {}
    props=filter(lambda x: type(x) is tuple and type(x[1]) is not tuple ,i[0][1][1])
    for i in props:
        pname=i[0].atomText
        if erl_term.IsErlBinary(i[1]):
            bd[name][pname] = i[1].contents
        if erl_term.IsErlAtom(i[1]):
            bd[name][pname] = i[1].atomText
        #print "all >>>> %s" % i[0]
        #print "yes >>>> %s" % i[1]

print bd

