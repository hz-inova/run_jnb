# -*- coding: utf-8 -*-

import collections
import ast
import json
import copy

from typing import Union
import nbformat


def kwargs_to_variable_assignment(kwargs: dict, value_representation=repr,
                                  assignment_operator: str = ' = ',
                                  statement_separator: str = '\n',
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
    join_str = '\n' if statement_per_line else ''
    for key, value in kwargs.items():
        code.append(key + assignment_operator +
                    value_representation(value)+statement_separator)
    return join_str.join(code)


def _mark_auto_generated_code(code: str):
    comment_after = '# '
    new_code = "\n".join(['', '', '',
                          comment_after+'!!! start assign jupyter notebook parameter(s) !!!',
                          '',
                          code,
                          comment_after+'!!! end assign jupyter notebook parameter(s) !!!'])
    return new_code


def decode_json(json_input: Union[str, None] = None):
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


def is_jsonable(obj) -> bool:
    """
    Check if an object is jsonable.

    An object is jsonable if it is json serialisable and by loading its json representation the same object is recovered.
    Parameters
    ----------
    obj : 
        Python object

    Returns
    -------
    bool

    >>> is_jsonable([1,2,3])
    True
    >>> is_jsonable((1,2,3))
    False
    >>> is_jsonable({'a':True,'b':1,'c':None})
    True
    """
    try:
        return obj==json.loads(json.dumps(obj))
    except TypeError:
        return False
    except:
        raise


def is_literal_eval(node_or_string) -> tuple:
    """
    Check if an expresion can be literal_eval.

    ----------
    node_or_string : 
        Input

    Returns
    -------
    tuple
        (bool,python object)

        
        If it can be literal_eval the python object is returned. Otherwise None it is returned.
        
    >>> is_literal_eval('[1,2,3]')
    (True, [1, 2, 3])
    >>> is_literal_eval('a')
    (False, None)
    """
    try:
        obj=ast.literal_eval(node_or_string)
        return (True, obj)
    except:
        return (False, None)


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


def sort_dict(d: dict, by: str = 'key',
              allow_duplicates: bool = True) -> collections.OrderedDict:
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
                    exclude_variable: Union[set, None] = None,
                    jsonable_parameter: bool = True) -> tuple:
    """
    Find the possible parameters and "global" variables from a python code.

    This is achieved by parsing the abstract syntax tree.

    Parameters
    ----------
    code : str
        Input code as string.
    exclude_variable : set, None, optional
        Variable to exclude.
    jsonable_parameter: bool, True, optional
        Consider only jsonable parameter

    Returns
    -------
    tuple
        (a set of possible parameter, a set of parameter to exclude, a dictionary of possible parameter )

        A variable is a possible parameter if 1) it is not in the input exclude_variable,
        2) the code contains only assignments, and 3) it is used only to bound objects.

        The set of parameter to exclude is the union of the input exclude_variable and all names that looks like a global variable.
        The dictionary of possible parameter {parameter name, parameter value} is available only if jsonable_parameter is True. 




    >>> variable_status("a=3")
    ({'a'}, {'a'}, {'a': 3})
    >>> variable_status("a=3",jsonable_parameter=False)
    ({'a'}, {'a'}, {})
    >>> variable_status("a += 1")
    (set(), {'a'}, {})
    >>> variable_status("def f(x,y=3):\\n\\t pass")
    (set(), {'f'}, {})
    >>> variable_status("class C(A):\\n\\t pass")
    (set(), {'C'}, {})
    >>> variable_status("import f")
    (set(), {'f'}, {})
    >>> variable_status("import f as g")
    (set(), {'g'}, {})
    >>> variable_status("from X import f")
    (set(), {'f'}, {})
    >>> variable_status("from X import f as g")
    (set(), {'g'}, {})
    """
    if exclude_variable is None:
        exclude_variable = set()
    else:
        exclude_variable = copy.deepcopy(exclude_variable)
    root = ast.parse(code)
    store_variable_name = set()
    assign_only = True
    dict_parameter={}

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Assign):
            for assign_node in ast.walk(node):
                if isinstance(assign_node, ast.Name):

                    if isinstance(assign_node.ctx, ast.Store):
                        if jsonable_parameter is False:
                            store_variable_name |= {assign_node.id}
                    else:
                        exclude_variable |= {assign_node.id}

            _is_literal_eval,_value=is_literal_eval(node.value)

            if jsonable_parameter is True:
                for assign_node in ast.iter_child_nodes(node):
                    if isinstance(assign_node, ast.Tuple):
                        i=0
                        for assign_tuple_node in ast.iter_child_nodes(assign_node):
                            if isinstance(assign_tuple_node, ast.Name):

                                if isinstance(_value,(collections.Iterable)) and is_jsonable(_value[i]) and _is_literal_eval:
                                    dict_parameter[assign_tuple_node.id]=_value[i]                                
                                    store_variable_name |= {assign_tuple_node.id} 
                                else:
                                    exclude_variable |= {assign_tuple_node.id}
                                i += 1
                    else:
                        if isinstance(assign_node, ast.Name):
                            if is_jsonable(_value) and _is_literal_eval:
                                dict_parameter[assign_node.id]=_value
                                store_variable_name |= {assign_node.id} 
                            else:
                                exclude_variable |= {assign_node.id}

        elif isinstance(node, ast.AugAssign):
            for assign_node in ast.walk(node):
                if isinstance(assign_node, ast.Name):
                    exclude_variable |= {assign_node.id}
        # class and function
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            assign_only = False
            exclude_variable |= {node.name}
        # import
        elif isinstance(node, ast.Import):
            assign_only = False
            for node1 in ast.iter_child_nodes(node):
                if node1.asname is not None:
                    exclude_variable |= {node1.asname}
                else:
                    exclude_variable |= {node1.name}
        # import from
        elif isinstance(node, ast.ImportFrom):
            assign_only = False
            for node1 in ast.iter_child_nodes(node):
                if node1.asname is not None:
                    exclude_variable |= {node1.asname}
                else:
                    exclude_variable |= {node1.name}
        else:
            assign_only = False
    if assign_only is True:
        possible_parameter = store_variable_name-exclude_variable
        if jsonable_parameter is True:
            dict_parameter = {k:dict_parameter[k] for k in possible_parameter}
        return (possible_parameter, store_variable_name | exclude_variable, dict_parameter)
    return set(), store_variable_name | exclude_variable, {}


def increment_name(name: str, start_marker: str = " (",
                   end_marker: str = ")") -> str:
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
