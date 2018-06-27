[![Build Status](https://travis-ci.org/hz-inova/run_jnb.svg?branch=master)](https://travis-ci.org/hz-inova/run_jnb)
[![Build status](https://ci.appveyor.com/api/projects/status/g15r1prwb2smvx6d/branch/master?svg=true)](https://ci.appveyor.com/project/aplamada/run-jnb/branch/master)
[![codecov](https://codecov.io/gh/hz-inova/run_jnb/branch/master/graph/badge.svg)](https://codecov.io/gh/hz-inova/run_jnb)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# run_jnb

**run_jnb** is a python package and command line tool for parametrising (python3 only) and executing Jupyter notebooks.

- **Source**: [https://github.com/hz-inova/run_jnb](https://github.com/hz-inova/run_jnb)
- **Platform**: Independent
- **Development Status**: Alpha
- **Getting Started**: [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/hz-inova/run_jnb/master?filepath=example%2FGetting%20Started.ipynb)

## Installation

```sh
pip install run_jnb
```

## Short Description

The package contains two public functions ***possible_parameter*** and ***run_jnb*** (see the docstring).

```python
>>> from run_jnb import possible_parameter, run_jnb
```

***run_jnb*** can be used also as a command line tool and its documentation is available via

```sh
run_jnb -h
```

## Simple Example

Consider the [notebook](example/Power_function.ipynb).

***possible_parameter*** returns a *list* of possible parameters with their name, value and cell index.
The list is alphabetically sorted by the name of the possible parameters.

```python
>>> possible_parameter('./Power_function.ipynb')
[PossibleParameter(name='exponent', value=2, cell_index=7),
 PossibleParameter(name='np_arange_args', value={'start': -10, 'stop': 10, 'step': 0.01}, cell_index=4)]
```

***run_jnb*** allows one to easily parametrise and execute a notebook.
```python
# Parametrise the noteboook and not execute the notebook
>>> run_jnb('./Power_function.ipynb', return_mode='parametrised_only', exponent=1)
# Parametrise and execute the notebook
>>> run_jnb('./Power_function.ipynb', return_mode=True, exponent=1)

Output(output_nb_path='.../_run_jnb/Power_function-output.ipynb',  error_prompt_number=None, 
error_type=None, error_value=None, error_traceback=None)
```
Please see the exported notebook by [only parametrising](example/_run_jnb/Power_function-output.ipynb) and by [parametrising and executing ](example/_run_jnb/Power_function-output%20(1).ipynb) the initial notebook.
Same output can be obtained by using *arg* parameter
```python
>>> run_jnb('.../Power_function.ipynb', return_mode=True, arg='{"exponent":1}')
```
or using the command line tool (the output is returned only in verbose mode and the tuple is serialised as a csv)
```sh
# " can be escaped by \"
$ run_jnb ./Power_function.ipynb -m true -a "{\"exponent\":1}" -vvv
".../_run_jnb/Power_function-output.ipynb",,,,
```

*np_arange_args* and *exponent* can be parametrised
```python
# parametrise using keyword arguments
>>> run_jnb('./Power_function.ipynb', return_mode=True, exponent=3, np_arange_args={'start':-20,'stop':20,'step':0.1})
# parametrise mixing keyword arguments and arg parameter
>>> run_jnb('./Power_function.ipynb', return_mode=True, arg='{"exponent":3}', np_arange_args={'start':-20,'stop':20,'step':0.1})
# parametrise using arg parameter with a json file
>>> run_jnb('./Power_function.ipynb', return_mode=True, arg='./power_function_arg.json')

Output(output_nb_path='.../_run_jnb/Power_function-output (1).ipynb',  error_prompt_number=None, 
error_type=None, error_value=None, error_traceback=None)
```
where in the last example [*power_function_arg.json*](example/power_function_arg.json) contains
```javascript
{
    "exponent": 3,
    "np_arange_args": {
        "start": -20,
	"stop": 20,
	"step": 0.1
    }
}
```

Please see the [generated notebook](example/_run_jnb/Power_function-output%20(2).ipynb).

If an error is detected during the execution of the generated notebook
```python
>>> run_jnb('./Power_function.ipynb', return_mode=True, exponent=1, np_arange_args={'step':0.1})
Output(output_nb_path='.../_run_jnb/Power_function-output (2).ipynb',  error_prompt_number=3, 
error_type='TypeError', error_value="Required argument 'start' (pos 1) not found", error_traceback=...)
```
the output provides also the prompt number of the cell where the error was caught and details about the error (please see the [generated notebook](example/_run_jnb/Power_function-output%20(3).ipynb)).

## How it works

For a notebook written in python one can find the possible parameters. This is achieved by parsing the abstract syntax tree of the code cells. A variable can be a possible parameter if:
- it is defined in a cell that contains only comments or assignments,
- its name is not used as a global variable in the current cell (beside the assignment) nor previously.


One can pass arguments as keyword arguments or in a json format (file or string). For safety reasons, in order to avoid any code injection, only json serializable keywords arguments are available. The keyword arguments are firstly encoded in json format using the standard [json encoder](https://docs.python.org/3.6/library/json.html#json.JSONEncoder). The json content is decoded into python objects using the standard [json decoder](https://docs.python.org/3.6/library/json.html#json.JSONDecoder) and it is mapped to a variable assignment by unpacking it. The assignments are appended at the end of the cell where they are initially defined.

For a *jsonable parameter*, i.e. a parameter for which its value can be recovered from its json representation using the standard decoder, the value of the parameter is returned as well. The value is determined in two steps: firstly the assignment is safely evaluated using [ast.literal_eval](https://docs.python.org/3/library/ast.html) and next it is checked if it is a jsonable parameter.

The generated notebook (parametrised or not) can be easily executed. The implementation relies on [nbconvert Executing notebooks](http://nbconvert.readthedocs.io/en/latest/execute_api.html).


## Dependencies
- [python](https://www.python.org): 3.5 or higher
- [nbconvert](http://nbconvert.readthedocs.io): 4.2 or higher

## License
[BSD 3](LICENSE)

## Acknowledgments
[nbrun](https://github.com/tritemio/nbrun) and [nbparameterise](https://github.com/takluyver/nbparameterise) were a source of inspiration.
