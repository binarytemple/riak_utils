# riak_utils

verifying correctness

# todo 

serialize the type/bucket/key combo using erlang serialization mechanism as in:

```
key_of(ObjectName) ->         
  crypto:sha(term_to_binary(ObjectName)).
```

Might be tricky to call into an erlang dll just to access the term constructor and `term_to_binary` nif.

found the libary `py_interface` which provides a module [`erl_term`](https://github.com/skysbird/py_interface/blob/master/py_interface/erl_term.py) which enables serializing python tuples using the same binary format as `erlang:term_to_binary/1`.

```
import sys
import types
import string
import socket
import getopt
from py_interface import erl_term
```

Examples of `py_interface` use

```python


import sys
import types
import string
import socket
import getopt
from py_interface import erl_term
from py_interface import erl_node
from py_interface import erl_opts
from py_interface import erl_common
from py_interface import erl_eventhandler

In [129]: erl_term.TermToBinary( erl_term.ErlTuple(("default","TYPE","32324")) )
Out[129]: '\x83h\x03k\x00\x07defaultk\x00\x04TYPEk\x00\x0532324'
In [130]: b=erl_term.TermToBinary( erl_term.ErlTuple(("default","TYPE","32324")) )
In [131]: erl_term.Bin
erl_term.BinariesToTerms erl_term.BinaryToTerm
In [131]: erl_term.BinaryToTerm(b)
Out[131]: ('default', 'TYPE', '32324')
In [132]: erl_term.BinaryToTerm(b)
KeyboardInterrupt
In [132]: b=erl_term.TermToBinary( erl_term.ErlTuple(("a","a","a")) )
In [133]: b
Out[133]: '\x83h\x03k\x00\x01ak\x00\x01ak\x00\x01a'

```

A further complication is the Riak implementation of consistent hashing http://basho.github.io/riak_core/chash.html#key_of-1. 

I can't tell from looking at the [implemention](https://github.com/basho/riak_core/blob/ddab30a9f86c0e6566d788731ab2596a40e2729a/src/chash.erl) exactly how I can replicate the logic in pure python.

# First look at the implementation

https://github.com/basho/riak_core/blob/7898729fa72af47194df410b480f5df78d488d7b/src/riak_core_util.erl#L260

Looking at a bucket properties I see that the default consistent hashing functions is

"chash_keyfun":{"mod":"riak_core_util","fun":"chash_std_keyfun"},

So this is where the magic happens

```
riak_core_util:chash_std_keyfun/
```






