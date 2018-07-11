# -*- coding: utf-8 -*-

from ..util import find_duplicates, variable_status


def test_find_duplicates():
    assert find_duplicates([1, 2, 3, 2, 1, 0, 0]) == {0, 1, 2}


def test_variable_status():

    code = """
class C(A):
    def f(self,x,y=3):
        pass
"""
    assert variable_status(code) == (set(), {'C'}, {})

    code = """
a = 1
class C(A):
    def f(self,x,y=3):
        pass
"""
    assert variable_status(code) == (set(), {'C','a'}, {})

    code = """
def f(x):
    b=c
    return x+a
"""
    assert variable_status(code) == (set(), {'f'}, {})

    code = """
a += 1
b = a
"""
    assert variable_status(code) == (set(), {'a', 'b'}, {})
    assert variable_status(code, jsonable_parameter=False) == ({'b'}, {'a', 'b'}, {})

    code = """
a = 1
b = a
"""
    assert variable_status(code) == (set(), {'a', 'b'}, {})
    assert variable_status(code, jsonable_parameter=False) == ({'b'}, {'a', 'b'}, {})

    code = """
a = 1
a = 2
"""
    assert variable_status(code) == ({'a'}, {'a'}, {'a':2})

    assert variable_status("a = {b:2,c:{'d':e}}", jsonable_parameter=False) == ({'a'},
                                                      {'a', 'b', 'c', 'e'}, {})
    assert variable_status("a = f(b)", jsonable_parameter=False) == ({'a'}, {'a', 'b', 'f'}, {})
    assert variable_status("a,b = 1,2") == ({'a', 'b'}, {'a', 'b'}, {'a':1, 'b':2})
    assert variable_status("a,b = (1,2)") == ({'a', 'b'}, {'a', 'b'}, {'a':1, 'b':2})
    assert variable_status("a,b = [1,2,3]") == ({'a', 'b'}, {'a', 'b'}, {'a':1, 'b':2})
    assert variable_status("a,b = map(lambda x: x**2, [1,2])") == (set(), {'a', 'b', 'map', 'x'}, {})
    assert variable_status("a  = f(a)", jsonable_parameter=False) == (set(), {'a', 'f'}, {})
