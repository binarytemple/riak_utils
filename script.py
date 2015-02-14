#!/usr/bin/python

"""
Example input:

  File: `/var/lib/riak/leveldb/707914855582156101004909840846949587645842325504/sst_3'
  Size: 4096        Blocks: 8          IO Block: 4096   directory
Device: fd09h/64472e    Inode: 154643      Links: 2
Access: (0755/drwxr-xr-x)  Uid: (  99/    riak)   Gid: (  99/ UNKNOWN)
Access: 2014-02-12 10:41:54.946526681 +0200
Modify: 2014-12-10 18:25:01.000000000 +0200
Change: 2014-02-11 21:06:18.665803431 +0200
"""

results={}
f=open('<file containing recursive stat output for a given riak data director see above for example>','rb')
lines=f.readlines()

for l in lines:
    if len(l) > 0 and not l[0].isdigit():
        sp=l.split(":",1)
        h=sp[0].strip()
        t=sp[1].strip().replace("`","").replace("'","")
        if h == "File":
            current=t
            results[current] = {}
        else:
            results[current][h]=t

print "File,Access,Modify,Change"
for k in results.keys():
    print "%s,%s,%s,%s" % (k,results[k]["Access"],results[k]["Modify"],results[k]["Change"])
