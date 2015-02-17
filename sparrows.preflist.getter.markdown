

```
%% for riak 2.x (type/bucket/key)

Preflist = fun(BucketType,Bucket,Key) ->
  BKey = {{BucketType,Bucket},Key},
  {ok, Ring} = riak_core_ring_manager:get_my_ring(),
  DocIdx = riak_core_util:chash_key(BKey),
  BucketProps = riak_core_bucket:get_bucket(Bucket, Ring),
  [NValue] = [Y || {X1, Y} <- BucketProps, n_val == X1],
  UpNodes = riak_core_node_watcher:nodes(riak_kv),
  Preflist2 = riak_core_apl:get_apl_ann(DocIdx, NValue, Ring, UpNodes),
  [IndexNode || {IndexNode, _Type} <- Preflist2]
end.
Preflist(<<"foo">>,<<"bar">>,<<"baz">>).


%% for riak 1.x (bucket/key)

PreflistOld = fun(Bucket,Key) ->
  BKey = {Bucket,Key},
  {ok, Ring} = riak_core_ring_manager:get_my_ring(),
  DocIdx = riak_core_util:chash_key(BKey),
  BucketProps = riak_core_bucket:get_bucket(Bucket, Ring),
  [NValue] = [Y || {X1, Y} <- BucketProps, n_val == X1],
  UpNodes = riak_core_node_watcher:nodes(riak_kv),
  Preflist2 = riak_core_apl:get_apl_ann(DocIdx, NValue, Ring, UpNodes),
  [IndexNode || {IndexNode, _Type} <- Preflist2]
end.
Preflist(<<"bar">>,<<"baz">>).










```