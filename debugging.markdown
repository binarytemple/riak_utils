
```

code:add_pathz("/usr/local/Cellar/erlang/17.3/lib/erlang/lib/runtime_tools-1.8.14/ebin").
dbg:start().
dbg:tracer(process, {fun(Msg, _) -> io:format("~p\n", [Msg]) end, []}).
dbg:tpl(riak_core_util,chash_std_keyfun, '_', []).
dbg:tpl(chash,key_of, '_', [ {'_', [], [{return_trace}] }] ).
dbg:p(all, c).
dbg:stop_clear().

```
