# -*- coding: utf-8 -*-
import shutil
import os
from collections import OrderedDict, namedtuple
from ..core import possible_parameter, run_jnb

PP=namedtuple('PossibleParameter',['name','value','cell_index'])
PP_1=namedtuple('PossibleParameter',['name', 'cell_index'])

def test_possible_parameter():
    input_path = r'./example/Power_function.ipynb'
    res_1 = [PP_1(name='exponent', cell_index=7), PP_1(name='np_arange_args', cell_index=4),
           PP_1(name='x', cell_index=5), PP_1(name='y', cell_index=9)]
    assert possible_parameter(input_path, jsonable_parameter=False) == res_1

    res_2 = [PP(name='exponent', value=2, cell_index=7), PP(name='np_arange_args', value={'start': -10, 'stop': 10, 'step': 0.01}, cell_index=4)]
    assert possible_parameter(input_path) == res_2
    assert possible_parameter(input_path, end_cell_index=4) == []
    assert possible_parameter(input_path, end_cell_index=5) == [res_2[1]]
    assert possible_parameter(input_path, end_cell_index=6, jsonable_parameter=False) == [res_1[1],res_1[2]]
    assert possible_parameter(input_path, end_cell_index=6 ) == [res_2[1]]

def test_run_jnb():
    input_path = r'./example/Power_function.ipynb'
    dirname, basename = os.path.split(input_path)
    output_dir = os.path.abspath(os.path.join(dirname, '_run_jnb'))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    output_path = os.path.join(output_dir, basename[:-6]+'-output'+basename[-6:])
    assert run_jnb(input_path, return_mode='parametrised_only', exponent=1) == (output_path, None, None, None, None)

    output_path = output_path[:-6]+' (1)'+output_path[-6:]
    assert run_jnb(input_path, return_mode=True, exponent=1) == (output_path, None, None, None, None)

    output_path = output_path.replace('(1).ipynb', '(2).ipynb')
    assert run_jnb(input_path, return_mode=True, exponent=3,
                   np_arange_args={'start': -20,
                                   'stop': 20,
                                   'step': 0.1}) == (output_path, None, None, None, None)

    assert run_jnb(input_path, return_mode=False, arg='{"exponent":1}',
                   np_arange_args={'start': -20,
                                   'stop': 20,
                                   'step': 0.1}) == (None, None, None, None, None)


    output_path = output_path.replace('(2).ipynb', '(3).ipynb')
    res = run_jnb(input_path, return_mode=True, exponent=1, np_arange_args={'step': 0.1})
    assert res[:-1] == (output_path, 3, 'TypeError', "Required argument 'start' (pos 1) not found")

    assert run_jnb(input_path, return_mode=False, arg='./example/power_function_arg.json') == (None, None, None, None, None)
