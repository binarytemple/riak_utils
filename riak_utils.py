# coding=utf-8
# We should be generally correct that given 100 items of input
# there is a reasonable expectation that at least one
# item should end up on the first partition.
# Todo, graph the partition distribution for this input set of numbers.
# 
# filter(lambda x: x[0][0] == 1, permute(16,0,100))

from sha import sha

from py_interface import erl_term


def permute(ring_size, start, end):
    """
    Usage example:

       In [359]: %%timeit
       permutations=permute(16,1,32)
       .....:
       1000 loops, best of 3: 743 µs per loop
       In [361]: permutations=permute(16,1,32)

       In [363]: len(permutations)
       Out[363]: 31

       In [364]: permutations[0]
       Out[364]:
       ((4, 274031556999544297163190906134303066185487351808L),
        (5, 365375409332725729550921208179070754913983135744L),
        (6, 456719261665907161938651510223838443642478919680L))
    """
    return [(whatp(x, ring_size)) for x in range(start, end)]


def whatp(bucket_type=None,bucket=None,key=None,ring_size=None,n_val=None):
    """
    Returns a tuple containing three tuples
       * primary partition number (indexed from 1) and partition start on 2 ** 160 numberline
       * as above but for the secondary partition n+1
       * as above but for the secondary partition n+2

    :rtype : object
    """
    part = ( 2 ** 160 ) / int(ring_size)
    id_hash = chash(bucket_type,bucket,key)

    # Partitioning rule... id is assigned to the partition after the hash and then two more
    pt = [(x + 1, x * part  ) for x in range(0, int(ring_size))]
    pt.reverse()
    primary = None

    for idx, val in enumerate(pt):
        if id_hash > val[1]:
            primary = idx -1
            break

    ret = []
    count=0
    while count < n_val:
        ret.append(pt[(primary - count % 64)])
        count += 1

    return id_hash,ret

def chash(bucket_type,bucket,key):
    if bucket_type != None:
        bt= erl_term.ErlBinary(bucket_type)
        b = erl_term.ErlBinary(bucket)
        k = erl_term.ErlBinary(key)
        etb=erl_term.TermToBinary(erl_term.ErlTuple((erl_term.ErlTuple((bt,b)),k)))
        return long(sha(etb).hexdigest(),16)
    else:
        b = erl_term.ErlBinary(bucket)
        k = erl_term.ErlBinary(key)
        etb=erl_term.TermToBinary(erl_term.ErlTuple((b,k)))
        return long(sha(etb).hexdigest(),16)

# #
# The following code take from:
#
# https://www.udacity.com/wiki/plotting-graphs-with-python
#
# This code is not necessary to run the util, I'm just dumping it here temporarily
#

from matplotlib import pyplot
from numpy import arange
import bisect


def scatterplot(x, y):
    pyplot.plot(x, y, 'b.')
    pyplot.xlim(min(x) - 1, max(x) + 1)
    pyplot.ylim(min(y) - 1, max(y) + 1)
    pyplot.show()


def barplot(labels, data):
    pos = arange(len(data))
    pyplot.xticks(pos + 0.4, labels)
    pyplot.bar(pos, data)
    pyplot.show()


def histplot(data, bins=None, nbins=5):
    if not bins:
        minx, maxx = min(data), max(data)
        space = (maxx - minx) / float(nbins)
        bins = arange(minx, maxx, space)
    binned = [bisect.bisect(bins, x) for x in data]
    l = ['%.1f' % x for x in list(bins) + [maxx]] if space < 1 else [str(int(x)) for x in list(bins) + [maxx]]
    displab = [x + '-' + y for x, y in zip(l[:-1], l[1:])]
    barplot(displab, [binned.count(x + 1) for x in range(len(bins))])


def barchart(x, y, numbins=5):
    datarange = max(x) - min(x)
    bin_width = float(datarange) / numbins
    pos = min(x)
    bins = [0 for i in range(numbins + 1)]

    for i in range(numbins):
        bins[i] = pos
        pos += bin_width
    bins[numbins] = max(x) + 1
    binsum = [0 for i in range(numbins)]
    bincount = [0 for i in range(numbins)]
    binaverage = [0 for i in range(numbins)]

    for i in range(numbins):
        for j in range(len(x)):
            if x[j] >= bins[i] and x[j] < bins[i + 1]:
                bincount[i] += 1
                binsum[i] += y[j]

    for i in range(numbins):
        binaverage[i] = float(binsum[i]) / bincount[i]
    barplot(range(numbins), binaverage)


def piechart(labels, data):
    fig = pyplot.figure(figsize=(7, 7))
    pyplot.pie(data, labels=labels, autopct='%1.2f%%')
    pyplot.show()
