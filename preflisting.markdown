```
{ok, Ring} = riak_core_ring_manager:get_my_ring().
CKey=chash:key_of({{<<"foo">>,<<"bar">>},<<"baz">>}).
riak_core_ring:preflist(CKey, Ring).
```

Returns:
```
(dev1@127.0.0.1)65> lists:last(riak_core_ring:preflist(chash:key_of({{<<"foo">>,<<"bar">>},<<"baz">>}), Ring)).
{981946412581700398168100746981252653831329677312,
 'dev1@127.0.0.1'}

(dev1@127.0.0.1)72> lists:sublist(riak_core_ring:preflist(chash:key_of({{<<"foo">>,<<"bar">>},<<"dbadzdd">>}), Ring),0).
[]

(dev1@127.0.0.1)73> lists:sublist(riak_core_ring:preflist(chash:key_of({{<<"foo">>,<<"bar">>},<<"dbadzdd">>}), Ring),3).
[{1255977969581244695331291653115555720016817029120,
  'dev1@127.0.0.1'},
 {1278813932664540053428224228626747642198940975104,
  'dev1@127.0.0.1'},
 {1301649895747835411525156804137939564381064921088,
  'dev1@127.0.0.1'}]
```

