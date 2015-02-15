# riak_utils

verifying correctness

# todo 

serialize the type/bucket/key combo using erlang serialization mechanism as in:

```
key_of(ObjectName) ->         
  crypto:sha(term_to_binary(ObjectName)).
```

Might be tricky to call into an erlang dll just to access the term constructor and `term_to_binary` nif.
