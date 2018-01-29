# -*- coding: utf-8 -*-

from ..util import find_duplicates, variable_status


def test_find_duplicates():
    assert find_duplicates([1,2,3,2,1,0,0]) == {0,1,2}


def test_variable_status():
    code = """
class C(A):
    pass
"""
    assert variable_status(code) == (set(), {'C','A'})

    code = """
class C(A):
    def f(self,x,y=3):
        pass
"""
    assert variable_status(code) == (set(), {'C','A'})

    code = """
def f(x):
    b=c
    return x+a
"""
    assert variable_status(code) == (set(),{'f','x','c','a'})

    code = """
a += 1
b = a
"""
    assert variable_status(code) == ({'b'},{'a','b'})

    assert variable_status("a = {b:2,c:{'d':e}}") == ({'a'},{'a','b','c','e'})
    assert variable_status("a = f(b)") == ({'a'},{'a','b','f'})
    assert variable_status("a,b = 1,2") == ({'a','b'},{'a','b'})
