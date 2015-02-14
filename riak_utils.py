# coding=utf-8
# We should be generally correct that given 100 items of input
# there is a reasonable expectation that at least one
# item should end up on the first partition.
# Todo, graph the partition distribution for this input set of numbers.
# 
# filter(lambda x: x[0][0] == 1, permute(16,0,100))

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


def whatp(oid, ring_size):
    """
    Returns a tuple containing three tuples
       * primary partition number (indexed from 1) and partition start on 2 ** 160 numberline
       * as above but for the secondary partition n+1
       * as above but for the secondary partition n+2

    :rtype : object
       Limitations:
       The n_val is fixed at 3, would be more useful if the n_val could be set to 2, or numbers greater than 3
       Usage example:
       In [355]: whatp("a",16)
       Out[355]:
       ((9, 730750818665451459101842416358141509827966271488L),
           (10, 822094670998632891489572718402909198556462055424L),
           (11, 913438523331814323877303020447676887284957839360L))
    """
    part = ( 2 ** 160 ) / ring_size
    from sha import sha

    id_hash = long(sha(str(oid)).hexdigest(), 16)
    pt = [((x + 1, x * part), ((  ((x + 1) % ring_size) + 1    ), ((x + 1) % ring_size) * part  ),
           ((  ((x + 2) % ring_size) + 1    ), ((x + 2) % ring_size) * part  )     ) for x in range(0, ring_size)]
    # print pt

    res = None
    for p in zip(pt, pt[1:-1]):
        start = p[0][0][1]
        end = p[1][0][1]
        if id_hash >= start and id_hash < end:
            res = p[0]
            break

    if res == None:
        return pt[-1]
    else:
        return res


# #
# The following code take from:
#
# https://www.udacity.com/wiki/plotting-graphs-with-python
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
