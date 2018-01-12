# -*- coding: utf-8 -*-

import collections
import ast
import json
import copy

import nbformat
from typing import Union


def kwargs_to_variable_assignment(kwargs: dict, value_representation=repr,
                                  assignment_operator: str=' = ',
                                  statement_separator: str ='\n',
                                  statement_per_line: bool = False) -> str:
    """
    Convert a dictionary into a string with assignments

    Each assignment is constructed based on:
    key assignment_operator value_representation(value) statement_separator,
    where key and value are the key and value of the dictionary.
    Moreover one can seprate the assignment statements by new lines.

    Parameters
    ----------
    kwargs : dict

    assignment_operator: str, optional:
        Assignment operator (" = " in python)
    value_representation: str, optinal
        How to represent the value in the assignments (repr function in python)
    statement_separator : str, optional:
        Statement separator (new line in python)
    statement_per_line: bool, optional
        Insert each statement on a different line

    Returns
    -------
    str
        All the assignemnts.

    >>> kwargs_to_variable_assignment({'a': 2, 'b': "abc"})
    "a = 2\\nb = 'abc'\\n"
    >>> kwargs_to_variable_assignment({'a':2 ,'b': "abc"}, statement_per_line=True)
    "a = 2\\n\\nb = 'abc'\\n"
    >>> kwargs_to_variable_assignment({'a': 2})
    'a = 2\\n'
    >>> kwargs_to_variable_assignment({'a': 2}, statement_per_line=True)
    'a = 2\\n'
    """
    code = []
    join_str='\n' if statement_per_line else ''
    for key, value in kwargs.items():
        code.append(key + assignment_operator +
                    value_representation(value)+statement_separator)
    return join_str.join(code)


def _mark_auto_generated_code(code:str):
    comment_after = '# '
    new_code = "\n".join(['','',
                          comment_after+'!!! start assign jupyter notebook parameter(s) !!!',
                          '',
                          code,
                          comment_after+'!!! end assign jupyter notebook parameter(s) !!!'])
    return new_code


def decode_json(json_input: Union[str, None]=None):
    """
    Simple wrapper of json.load and json.loads.

    If json_input is None the output is an empty dictionary.
    If the input is a string that ends in .json it is decoded using json.load.
    Otherwise it is decoded using json.loads.

    Parameters
    ----------
    json_input : str, None, optional
        input json object


    Returns
    -------
    Decoded json object

    >>> decode_json()
    {}
    >>> decode_json('{"flag":true}')
    {'flag': True}
    >>> decode_json('{"value":null}')
    {'value': None}
    """
    if json_input is None:
        return {}
    else:
        if isinstance(json_input, str) is False:
            raise TypeError()
        elif json_input[-5:] == ".json":
            with open(json_input) as f:
                decoded_json = json.load(f)
        else:
            decoded_json = json.loads(json_input)
    return decoded_json



def find_duplicates(l: list) -> set:
    """
    Return the duplicates in a list.

    The function relies on
    https://stackoverflow.com/questions/9835762/find-and-list-duplicates-in-a-list .
    Parameters
    ----------
    l : list
        Name

    Returns
    -------
    set
        Duplicated values

    >>> find_duplicates([1,2,3])
    set()
    >>> find_duplicates([1,2,1])
    {1}
    """
    return set([x for x in l if l.count(x) > 1])


def sort_dict(d: dict, by: str='key',
              allow_duplicates: bool=True) -> collections.OrderedDict:
    """
    Sort a dictionary by key or value.

    The function relies on
    https://docs.python.org/3/library/collections.html#collections.OrderedDict .
    The dulicated are determined based on
    https://stackoverflow.com/questions/9835762/find-and-list-duplicates-in-a-list .
    Parameters
    ----------
    d : dict
        Input dictionary
    by : ['key','value'], optional
        By what to sort the input dictionary
    allow_duplicates : bool, optional
        Flag to indicate if the duplicates are allowed.
    Returns
    -------
    collections.OrderedDict
        Sorted dictionary.

    >>> sort_dict({2: 3, 1: 2, 3: 1})
    OrderedDict([(1, 2), (2, 3), (3, 1)])
    >>> sort_dict({2: 3, 1: 2, 3: 1}, by='value')
    OrderedDict([(3, 1), (1, 2), (2, 3)])
    >>> sort_dict({'2': 3, '1': 2}, by='value')
    OrderedDict([('1', 2), ('2', 3)])
    >>> sort_dict({2: 1, 1: 2, 3: 1}, by='value', allow_duplicates=False)
    Traceback (most recent call last):
        ...
    ValueError: There are duplicates in the values: {1}
    >>> sort_dict({1:1,2:3},by=True)
    Traceback (most recent call last):
        ...
    ValueError: by can be 'key' or 'value'.
    """
    if by == 'key':
        i = 0
    elif by == 'value':
        values = list(d.values())
        if len(values) != len(set(values)) and not allow_duplicates:
            duplicates = find_duplicates(values)
            raise ValueError("There are duplicates in the values: {}".format(duplicates))
        i = 1
    else:
        raise ValueError("by can be 'key' or 'value'.")

    return collections.OrderedDict(sorted(d.items(), key=lambda t: t[i]))


def group_dict_by_value(d: dict) -> dict:
    """
    Group a dictionary by values.


    Parameters
    ----------
    d : dict
        Input dictionary

    Returns
    -------
    dict
        Output dictionary. The keys are the values of the initial dictionary
        and the values ae given by a list of keys corresponding to the value.

    >>> group_dict_by_value({2: 3, 1: 2, 3: 1})
    {3: [2], 2: [1], 1: [3]}
    >>> group_dict_by_value({2: 3, 1: 2, 3: 1, 10:1, 12: 3})
    {3: [2, 12], 2: [1], 1: [3, 10]}
    """
    d_out = {}
    for k, v in d.items():
        if v in d_out:
            d_out[v].append(k)
        else:
            d_out[v] = [k]
    return d_out


def _read_nb(nb_path: str):
    with open(nb_path, 'r') as f:
        return nbformat.read(f, as_version=nbformat.NO_CONVERT)


def _write_nb(nb: nbformat.notebooknode.NotebookNode, nb_path: str):
    with open(nb_path, mode='wt', newline='\n', encoding='UTF-8') as f:
        nbformat.write(nb, f)


def variable_status(code: str,
                    exclude_variable: Union[set, None]=None) -> tuple:
    """
    Find the possible and the used variables from a python code.


    Parameters
    ----------
    code : str
        Input code as string.
    exclude_variable : set, None, optional
        Variable to exclude.
    Returns
    -------
    tuple
        (a set of possible parameter,a set of parameter to exclude)

        Assuming that the code can be the content of a function, this function
        tries to identify the variable that can be used as parameter and the one
        that have be discarded. This is achieved by parsing the abstract syntax trees.
        If the variable is used for the first time in an assignment it is a
        candidate for a possible parameter as long it is not present in
        exclude_variable. The names used in the code are carefully discarded.

    >>> variable_status("a=3")
    ({'a'}, {'a'})
    >>> variable_status("a += 1")
    (set(), {'a'})
    >>> variable_status("def f(x,y=3):\\n\\t pass")
    (set(), {'f'})
    >>> variable_status("import f")
    (set(), {'f'})
    >>> variable_status("import f as g")
    (set(), {'g'})
    >>> variable_status("from X import f")
    (set(), {'f'})
    >>> variable_status("from X import f as g")
    (set(), {'g'})
    """
    if exclude_variable is None:
        exclude_variable = set()
    else:
        exclude_variable = copy.deepcopy(exclude_variable)
    root = ast.parse(code)
    store_variable_name = set()
    assign_only = True
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Assign):
            for assign_node in ast.walk(node):
                if isinstance(assign_node, ast.Name):
                    if isinstance(assign_node.ctx, ast.Store):
                        store_variable_name |= {assign_node.id}
                    else:
                        exclude_variable |= {assign_node.id}
        elif isinstance(node, ast.AugAssign):
            for assign_node in ast.walk(node):
                if isinstance(assign_node, ast.Name):
                    exclude_variable |= {assign_node.id}
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            assign_only = False
            exclude_variable |= {node.name}
            if node.decorator_list is not None:
                for node1 in ast.iter_child_nodes(node):
                    for assign_node in ast.walk(node):
                        if isinstance(assign_node, ast.Name):
                            if isinstance(assign_node.ctx, ast.Load):
                                exclude_variable |= {assign_node.id}
        elif isinstance(node, ast.Import):
            assign_only = False
            for node1 in ast.iter_child_nodes(node):
                if node1.asname is not None:
                    exclude_variable |= {node1.asname}
                else:
                    exclude_variable |= {node1.name}
        elif isinstance(node, ast.ImportFrom):
            assign_only = False
            #exclude_variable |= {node.module}
            for node1 in ast.iter_child_nodes(node):
                if node1.asname is not None:
                    exclude_variable |= {node1.asname}
                else:
                    exclude_variable |= {node1.name}
        else:
            assign_only = False
    if assign_only is True:
        return (store_variable_name-exclude_variable,
                store_variable_name | exclude_variable)
    return set(), store_variable_name | exclude_variable


def increment_name(name: str, start_marker: str =" (",
                   end_marker: str =")") -> str:
    """
    Increment the name where the incremental part is given by parameters.

    Parameters
    ----------
    name : str, nbformat.notebooknode.NotebookNode
        Name
    start_marker : str
        The marker used before the incremental
    end_marker : str
        The marker after the incrementa

    Returns
    -------
    str
        Incremented name.

    >>> increment_name('abc')
    'abc (1)'
    >>> increment_name('abc(1)')
    'abc(1) (1)'
    >>> increment_name('abc (123)')
    'abc (124)'
    >>> increment_name('abc-1',start_marker='-',end_marker='')
    'abc-2'
    >>> increment_name('abc[2]',start_marker='[',end_marker=']')
    'abc[3]'
    >>> increment_name('abc1',start_marker='',end_marker='')
    Traceback (most recent call last):
        ...
    ValueError: start_marker can not be the empty string.
    """
    if start_marker == '':
        raise ValueError("start_marker can not be the empty string.")
    a = name
    start = len(a)-a[::-1].find(start_marker[::-1])

    if (a[len(a)-len(end_marker):len(a)] == end_marker
            and start < (len(a)-len(end_marker))
            and a[start-len(start_marker):start] == start_marker
            and a[start:len(a)-len(end_marker)].isdigit()):

        old_int = int(a[start:len(a)-len(end_marker)])
        new_int = old_int+1
        new_name = a[:start]+str(new_int)+end_marker
    else:
        new_name = a+start_marker+'1'+end_marker
    return new_name
