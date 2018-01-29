# -*- coding: utf-8 -*-
import shutil
import os
from collections import OrderedDict
from ..core import possible_parameter, run_jnb


def test_possible_parameter():
    input_path = r"../example/Power_function.ipynb"
    assert possible_parameter(input_path) == OrderedDict([('np_arange_args', 4), ('x', 5), ('exponent', 7), ('y', 9)])
    assert possible_parameter(input_path,4) == OrderedDict()
    assert possible_parameter(input_path,5) == OrderedDict([('np_arange_args', 4)])
    assert possible_parameter(input_path,6) == OrderedDict([('np_arange_args', 4), ('x', 5)])


def test_run_jnb():
    input_path = r"../example/Power_function.ipynb"
    dirname,basename=os.path.split(input_path)
    output_dir = os.path.abspath(os.path.join(dirname,'_run_jnb'))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    output_path=os.path.join(output_dir,basename[:-6]+'-output'+basename[-6:])
    assert run_jnb(input_path, return_mode='parametrise_only', exponent=1)==(output_path,None,None,None,None)

    output_path=output_path[:-6]+' (1)'+output_path[-6:]
    assert run_jnb(input_path, return_mode=True, exponent=1)==(output_path,None,None,None,None)

    output_path=output_path.replace('(1).ipynb','(2).ipynb')
    assert run_jnb(input_path, return_mode=True, exponent=3, np_arange_args={'start':-20,'stop':20,'step':0.1})==(output_path,None,None,None,None)

    output_path=output_path.replace('(2).ipynb','(3).ipynb')
    res=run_jnb(input_path, return_mode=True, exponent=1, np_arange_args={'step':0.1})
    assert res[:-1]==(output_path,3,'TypeError', "Required argument 'start' (pos 1) not found")


