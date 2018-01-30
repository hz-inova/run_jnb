# -*- coding: utf-8 -*-

import json
import os

from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError

from .util import _read_nb, _write_nb, sort_dict, group_dict_by_value, \
 decode_json, kwargs_to_variable_assignment, _mark_auto_generated_code, \
 increment_name
from .jnb_helper import _JupyterNotebookHelper


def possible_parameter(nb, end_cell_index=None):
    """
    Find the possible parameters from a jupyter notebook (python3 only).

    The possible parameters are obtained by parsing the abstract syntax tree of
    the python code generated from the jupyter notebook.

    For a jupuyter notebook, a variable can be a possible parameter if:
        - it is defined in a cell that contains only comments or assignments,
        - its name is not used in the current cell beside the assignment nor previously.


    Parameters
    ----------
    nb : str, nbformat.notebooknode.NotebookNode
        Jupyter notebook path or its content as a NotebookNode object.
    end_cell_index : int, optional
        End cell index used to slice the notebook in finding the possible parameters.

    Returns
    -------
    collections.OrderedDict
        Ordered dictionary with the possible parameters for the jupyter notebook.
        The key is the name of the variable and the value is the index of the cell where the variable is defined using a zero-based numbering.
        The dictionary is ordered by the cell index.
    """
    jh = _JupyterNotebookHelper(nb, end_cell_index)
    return jh.possible_param


def run_jnb(input_path, output_path=r"///_run_jnb/*-output",
            execution_path=r'///input',
            return_mode='except',
            overwrite=False,
            timeout=ExecutePreprocessor.timeout.default_value,
            kernel_name=ExecutePreprocessor.kernel_name.default_value,
            ep_kwargs=None, end_cell_index=None, arg=None, **kwargs):
    """
    Run an input jupyter notebook file and optionally (python3 only)
    parametrise it.

    One can pass arguments as keyword arguments or in a json format (file or string).
    For safety reasons, in order to avoid any code injection,
    only json serialisable keywords arguments are available. The keyword
    arguments are firstly encoded in json format using the standard json encoder.
    The json content is decoded into python objects using the standard json decoder
    and it is mapped to a variable assignment by unpacking it.
    The assignments are appended at the end of the cell where they are initially defined.


    Parameters
    ----------
    input_path : str
        Path of the input jupyter notebook.
    output_path : str, optional
        Path of the output jupyter notebook.
        One can use the input_path location as relative path by starting with "///" .
        * can be used once in the beggining or end (excluding the ".ipynb" extension) as a wildcard of the input_path filename.
        "///_run_jnb/*-output" is the default value and states that the output
        is in the run_jnb folder with respect to the input_path directory and "-output" is appended to the input name.
    execution_path : str, optional
        The path of the folder where to execute the notebook.
        r'///input' or r'///output' can be used to denote the input / output folder.

    return_mode : ['parametrised_only','except',True, False], optional
        Flag to write the generated notebook to the output_path: "parametrised_only" writes the generated notebook without executing it, "except" writes in case of an exception, True writes always, False writes never.
    overwrite : bool, optional
        Flag to overwrite or not the output_path. If the parameter is False
        the used output_path will be incremented until a valid one is found.
    timeout : int, optional
        ExecutePreprocessor.timeout
    kernel_name : str, optional
        ExecutePreprocessor.kernel_name
    ep_kwargs : dict, optional
        Other kwargs accepted by nbconvert.preprocessors.ExecutePreprocessor
    end_cell_index : int, optional
        End cell index used to slice the notebook in finding the possible parameters.
    arg : str
        Path of a json file (it should end in ".json") or json formatted string used to parametrise the jupyter notebook.
        It should containt json objects. It is decoded into python objects following https://docs.python.org/3.6/library/json.html#json-to-py-table .
    kwargs:
        json serialsable keyword arguments used to parametrise the jupyter notebook.

    Returns
    -------
    tuple
        (output absolute path or None, error prompt number, error type, error value, error traceback)
        If the generated file is written the output path is returned otherwise None.
        If an error is catched the details are return otherwise None.
        """

    if os.path.splitext(input_path)[1] != '.ipynb':
        raise ValueError("The extension of input_path = '{}' is not '.ipynb'".format(input_path))
    if os.path.basename(input_path) == '*':
        raise ValueError("The filename ={} can not start with *".format(input_path))


    input_path_dir, input_path_base = os.path.split(input_path)
    if output_path.startswith(r'///'):
        input_rel = True
        output_path = output_path[3:]
    else:
        input_rel = False
    output_path_dir, output_path_base = os.path.split(output_path)

    if input_rel:
        output_path_dir = os.path.join(input_path_dir, output_path_dir)
        output_path_dir = os.path.normpath(output_path_dir)

    if os.path.exists(output_path_dir) is False:
        os.makedirs(output_path_dir)

    if output_path_base.endswith('.ipynb'):
        pass
    elif output_path_base.startswith("*"):
        output_path_base = input_path_base[:-6]+output_path_base[1:]+'.ipynb'
    elif output_path_base.endswith("*"):
        output_path_base = output_path_base[:-1]+input_path_base[:-6]+'.ipynb'
    else:
        raise ValueError("Invalid output_path")

    output_path = os.path.abspath(os.path.join(output_path_dir,
                                               output_path_base))

    if output_path is not None and os.path.splitext(output_path)[1] != '.ipynb':
        raise ValueError("The extension of output_path = '{}' is not '.ipynb'".format(output_path))

    if execution_path.startswith(r'///input'):
        execution_path = os.path.join(input_path_dir, execution_path[8:])
    elif execution_path.startswith(r'///output'):
        execution_path = os.path.join(input_path_dir, execution_path[8:])
    execution_path = os.path.normpath(execution_path)

    if os.path.exists(execution_path) is False:
        os.makedirs(execution_path)

    if ep_kwargs is None:
        ep_kwargs = {}

    if return_mode not in ['parametrised_only','except', True, False]:
        raise TypeError("return mode is not valid!")

    kwarg_to_json = json.dumps(kwargs)
    kwarg_as_kwarg = decode_json(kwarg_to_json)
    arg_as_kwarg = decode_json(arg)

    multiple_kwarg = set(arg_as_kwarg.keys()) & set(kwarg_as_kwarg.keys())
    if multiple_kwarg != set():
        raise ValueError('Multiple values for keyword argument {}'.format(multiple_kwarg))
    jupyter_kwargs = {**arg_as_kwarg, **kwarg_as_kwarg}
    nb = _read_nb(input_path)

    # clean notebook
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            nb['cells'][i]['outputs'] = []
            nb['cells'][i]['execution_count'] = None

    if jupyter_kwargs != {}:
        params_of_interest = {}
        jnh = _JupyterNotebookHelper(nb, end_cell_index)
        for el in jupyter_kwargs.keys():
            if el not in jnh.possible_param.keys():
                raise ValueError(repr(el)+' is not a possible parameter {}.'.format(list(jnh.possible_param.keys())))
            else:
                params_of_interest[el] = jnh.possible_param[el]
        params_of_interest = sort_dict(params_of_interest, by='value')
        cell_index_param = group_dict_by_value(params_of_interest)
        for key, value in cell_index_param.items():
            cell_param = {k: jupyter_kwargs[k] for k in value}
            cell_code = kwargs_to_variable_assignment(cell_param)
            marked_code = _mark_auto_generated_code(cell_code)
            nb['cells'][key]['source'] += marked_code

    if return_mode != 'parametrised_only':
        ep = ExecutePreprocessor(timeout=timeout, kernel_name=kernel_name,
                                 **ep_kwargs)

    catch_except = False

    error = (None, None, None, None)
    try:
        if return_mode != 'parametrised_only':
            ep.preprocess(nb, {'metadata': {'path': execution_path}})
    except CellExecutionError:
        catch_except = True

        for cell in nb['cells'][::-1]:
            if cell['cell_type'] == 'code' and cell.get('outputs')!=[]:
                for output in cell['outputs']:
                    if output.get('output_type') == 'error':
                        error = (cell['execution_count'],
                                 output.get('ename'), output.get('evalue'),
                                 output.get('traceback'))
                        break
                if error[0] is not None:
                    break
                else:
                    raise ValueError('Cell expected to have an error.')
    except:
        raise

    if return_mode == 'except':
        if catch_except is True:
            nb_return = True
        else:
            nb_return = None
    elif return_mode is True or return_mode == 'parametrised_only':
        nb_return = True
    elif return_mode is False:
        nb_return = None

    if nb_return is not None:
        if overwrite is False:
            while os.path.exists(output_path):
                dirname, basename = os.path.split(output_path)
                root, ext = os.path.splitext(basename)
                new_root = increment_name(root)
                output_path = os.path.join(dirname, new_root+ext)
        nb_return = output_path  # update the output_path
        _write_nb(nb, output_path)
    return (nb_return, *error)
