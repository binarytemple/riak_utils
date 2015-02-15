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

I get Erlang debugging up and running to trace into this function call I read [this as reference](http://blog.differentpla.net/blog/2014/05/08/debugging-erlang-with-a-remote-shell/)

```
** exception error: undefined function debugger:start/0
(dev1@127.0.0.1)10>
(dev1@127.0.0.1)10> code:add_pathz("/usr/local/Cellar/erlang/17.3/lib/erlang/lib/runtime_tools-1.8.
14/ebin").
true
(dev1@127.0.0.1)11> debugger:start().                                                              ** exception error: undefined function debugger:start/0
(dev1@127.0.0.1)12> dbg:start().
{ok,<0.2306.0>}
(dev1@127.0.0.1)13>  dbg:tracer(process, {fun(Msg, _) -> io:format("~p\n", [Msg]) end, []}).
{ok,<0.2306.0>}
(dev1@127.0.0.1)14>
(dev1@127.0.0.1)14> dbg:tpl(riak_core_util,chash_std_keyfun, '_', []).
{ok,[{matched,'dev1@127.0.0.1',1}]}
(dev1@127.0.0.1)15>


(dev1@127.0.0.1)14> dbg:tpl(riak_core_util,chash_std_keyfun, '_', []).
{ok,[{matched,'dev1@127.0.0.1',1}]}
(dev1@127.0.0.1)15>
(dev1@127.0.0.1)15>
(dev1@127.0.0.1)15>  dbg:p(all, c).
{ok,[{matched,'dev1@127.0.0.1',1040}]}
{trace,<6166.2950.0>,call,
       {riak_core_util,chash_std_keyfun,[{<<"foo">>,<<"bar">>}]}}
{trace,<6166.2973.0>,call,
       {riak_core_util,chash_std_keyfun,[{<<"foo">>,<<"bar">>}]}}
{trace,<6166.2974.0>,call,
       {riak_core_util,chash_std_keyfun,[{<<"foo">>,<<"bar">>}]}}
{trace,<6166.784.0>,call,
       {riak_core_util,chash_std_keyfun,[{<<"foo">>,<<"bar">>}]}}
{trace,<6166.763.0>,call,
       {riak_core_util,chash_std_keyfun,[{<<"foo">>,<<"bar">>}]}}
(dev1@127.0.0.1)16>
───────────────────────────────────────────────────────────────────────────────────────────────────
 {webmachine_decision_core,decision,1,
                           [{file,"src/webmachine_decision_core.erl"},
                            {line,558}]},
 {webmachine_decision_core,handle_request,2,
                           [{file,"src/webmachine_decision_core.erl"},
                            {line,33}]},
 {webmachine_mochiweb,loop,2,[{file,"src/webmachine_mochiweb.erl"},{line,74}]},
 {mochiweb_http,parse_headers,5,[{file,"src/mochiweb_http.erl"},{line,180}]},
 {proc_lib,init_p_do_apply,3,[{file,"proc_lib.erl"},{line,239}]}]</pre><P><HR><ADDRESS>mochiweb+webmachine web server</ADDRESS></body></html>%                                                        [~%]curl "localhost:10018/buckets/foo/keys/bar"
not found
[~%]curl -XPUT "localhost:10018/buckets/foo/keys/bar" -d test
[~%]curl "localhost:10018/buckets/foo/keys/bar"
test%                                                                                              [~%]
[~%]curl "localhost:10018/buckets/foo/keys/bar"
test%
[~%]curl -XPUT "localhost:10018/buckets/foo/keys/bar" -d test
```

Do your thing; enjoy the tracing.

Then turn it off:
```
11> dbg:stop_clear().
```

Back on, and continue onwards

```
(dev1@127.0.0.1)18> dbg:p(all, c).
{ok,[{matched,'dev1@127.0.0.1',1040}]}
(dev1@127.0.0.1)19> dbg:tpl(chash,key_of, '_', [ {'_', [], [{return_trace}] }] ).
{ok,[{matched,'dev1@127.0.0.1',1},{saved,1}]}
```

And the results

```
{trace,<6166.763.0>,call,{chash,key_of,[{<<"foo">>,<<"bar">>}]}}
{trace,<6166.784.0>,return_from,
       {chash,key_of,1},
       <<73,212,27,234,104,13,150,207,0,82,86,183,125,225,172,154,135,46,6,112>>}
{trace,<6166.763.0>,return_from,
       {chash,key_of,1},
       <<73,212,27,234,104,13,150,207,0,82,86,183,125,225,172,154,135,46,6,112>>}
```


Having created and activated a bucket type, we can also inspect the behavior when hashing a tuple of 
* bucket-type
* bucket
* key
```

{trace,<6166.5499.0>,call,
       {chash,key_of,[{{<<"fodddo">>,<<"foo">>},<<"bar">>}]}}
{trace,<6166.5499.0>,return_from,
       {chash,key_of,1},
       <<217,141,87,102,4,57,11,252,233,16,190,235,105,146,157,105,113,152,3,
         152>>}
(dev1@127.0.0.1)20>
───────────────────────────────────────────────────────────────────────────────────────────────────
Usage: riak-admin bucket-type activate <type>
[/basho/riak/dev%]./dev1/bin/riak-admin bucket-type activate fodddo
fodddo has been activated

WARNING: Nodes in this cluster can no longer be
downgraded to a version of Riak prior to 2.0
[/basho/riak/dev%]
[/basho/riak/dev%]curl -XGET "localhost:10018/types/default/buckets/foo/keys/bar"                  test%                                                                                              [/basho/riak/dev%]curl -XGET "localhost:10018/types/foodor/buckets/foo/keys/bar"
Unknown bucket type: foodor%                                                                       [/basho/riak/dev%]curl -XGET "localhost:10018/types/foodoo/buckets/foo/keys/bar"
Unknown bucket type: foodoo%                                                                       [/basho/riak/dev%]curl -XGET "localhost:10018/types/fodoo/buckets/foo/keys/bar"
Unknown bucket type: fodoo%                                                                        [/basho/riak/dev%]curl -XGET "localhost:10018/types/fodddo/buckets/foo/keys/bar"
not found
[/basho/riak/dev%]curl -XGET "localhost:10018/types/fodddo/buckets/foo/keys/bar"
```

So it doesn't look like anything fancy is happening there. Lets investigate further why the values are wrong.

```
       {chash,key_of,[{{<<"fodddo">>,<<"foo">>},<<"bar">>}]}}
{trace,<6166.2281.0>,return_from,
       {chash,key_of,1},
       <<217,141,87,102,4,57,11,252,233,16,190,235,105,146,157,105,113,152,3,
         152>>}
<<217,141,87,102,4,57,11,252,233,16,190,235,105,146,157,
  105,113,152,3,152>>
(dev1@127.0.0.1)23>
───────────────────────────────────────────────────────────────────────────────────────────────────

WARNING: Nodes in this cluster can no longer be
downgraded to a version of Riak prior to 2.0
[/basho/riak/dev%]
[/basho/riak/dev%]curl -XGET "localhost:10018/types/default/buckets/foo/keys/bar"                  test%                                                                                              [/basho/riak/dev%]curl -XGET "localhost:10018/types/foodor/buckets/foo/keys/bar"
Unknown bucket type: foodor%                                                                       [/basho/riak/dev%]curl -XGET "localhost:10018/types/foodoo/buckets/foo/keys/bar"
Unknown bucket type: foodoo%                                                                       [/basho/riak/dev%]curl -XGET "localhost:10018/types/fodoo/buckets/foo/keys/bar"
Unknown bucket type: fodoo%                                                                        [/basho/riak/dev%]curl -XGET "localhost:10018/types/fodddo/buckets/foo/keys/bar"
not found
[/basho/riak/dev%]curl -XGET "localhost:10018/types/fodddo/buckets/foo/keys/bar"
not found
[/basho/riak/dev%]
[/basho/riak/dev%]curl -XGET "localhost:10018/types/fodddo/buckets/foo/keys/bar"
not found
```

Invoking from riak attach produces the same result:
```
(dev1@127.0.0.1)23> chash:key_of({{<<"fodddo">>,<<"foo">>},<<"bar">>}).
{trace,<6166.2281.0>,call,
       {chash,key_of,[{{<<"fodddo">>,<<"foo">>},<<"bar">>}]}}
{trace,<6166.2281.0>,return_from,
       {chash,key_of,1},
       <<217,141,87,102,4,57,11,252,233,16,190,235,105,146,157,105,113,152,3,
         152>>}
<<217,141,87,102,4,57,11,252,233,16,190,235,105,146,157,
  105,113,152,3,152>>
  
```


