import typing as t

from superduper import Component


class MyComponentUtil(Component):
    a: int
    b: str
    c: t.Dict


def test_hash_item():

    c1 = MyComponentUtil('test', a=1, b='test-1', c={'this': 'is a test'})

    c2 = MyComponentUtil('test', a=1, b='test-1', c={'this': 'is a test'})

    assert c1.uuid == c2.uuid

    c3 = MyComponentUtil('test', a=1, b='test-2', c={'this': 'is a test'})

    assert c1.hash != c3.hash

    assert c1.merkle_tree['b'] != c3.merkle_tree['b']

    for k in c1.merkle_tree:
        if k == 'b':
            continue
        assert (
            c1.merkle_tree[k] == c3.merkle_tree[k]
        ), 'Trees differed at key: {}'.format(k)
