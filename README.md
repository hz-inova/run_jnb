[![Build Status](https://travis-ci.org/hz-inova/run_jnb.svg?branch=master)](https://travis-ci.org/hz-inova/run_jnb)
[![Build status](https://ci.appveyor.com/api/projects/status/g15r1prwb2smvx6d/branch/master?svg=true)](https://ci.appveyor.com/project/aplamada/run-jnb/branch/master)
[![codecov](https://codecov.io/gh/hz-inova/run_jnb/branch/master/graph/badge.svg)](https://codecov.io/gh/hz-inova/run_jnb)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# run_jnb

**run_jnb** is a python package and command line tool for parametrising (python3 only) and executing Jupyter notebooks.

- **Source**: [https://github.com/hz-inova/run_jnb](https://github.com/hz-inova/run_jnb)
- **Platform**: Independent
- **Development Status**: Alpha

## Installion

```sh
pip install run_jnb
```

## Short Description

For a notebook written in python one can find the possible parameters. This is achieved by parsing the abstract syntax tree of the code cells. A variable can be a possible parameter if:
- it is defined in a cell that contains only comments or assignments,
- its name is not used as a global variable in the current cell (beside the assignment) nor previously.

One can pass arguments as keyword arguments or in a json format (file or string). For safety reasons, in order to avoid any code injection, only json serializable keywords arguments are available. The keyword arguments are firstly encoded in json format using the standard [json encoder](https://docs.python.org/3.6/library/json.html#json.JSONEncoder). The json content is decoded into python objects using the standard [json decoder](https://docs.python.org/3.6/library/json.html#json.JSONDecoder) and it is mapped to a variable assignment by unpacking it. The assignments are appended at the end of the cell where they are initially defined.

The generated notebook (parametrised or not) can be easily executed (the implementation relies on [nbconvert Executing notebooks](http://nbconvert.readthedocs.io/en/latest/execute_api.html)).

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

***possible_parameter*** returns an *OrderedDict* where the key is the parameter name and the value is the corresponding cell index.

```python
>>> possible_parameter('./Power_function.ipynb')
OrderedDict([('np_arange_args', 4), ('x', 5), ('exponent', 7), ('y', 9)])
```
The notebook contains several possible parameters.

Next we will parametrise the *exponent* using ***run_jnb***.

***run_jnb*** returns a tuple (output absolute path, error prompt number, error type, error value, error traceback).
One can easily parametrise and execute a notebook
```python
# Parametrise the noteboook and not execute the notebook
>>> run_jnb('./Power_function.ipynb', return_mode='parametrised_only', exponent=1)
# Parametrise and execute the notebook
>>> run_jnb('./Power_function.ipynb', return_mode=True, exponent=1)

('.../_run_jnb/Power_function-output.ipynb', None, None, None, None)
```
Please see the exported notebook by [only parametrising](example/_run_jnb/Power_function-output.ipynb) and by [parametrising and executing ](example/_run_jnb/Power_function-output%20(1).ipynb) the initial notebook.
Same output can be obtained by using *arg* parameter:
```python
>>> run_jnb('.../Power_function.ipynb', return_mode=True, arg='{"exponent":1}')
```
or using the command line tool:
```sh
# " can be escaped by \"
$ run_jnb ./Power_function.ipynb -m true -a "{\"exponent\":1}" -vvv
".../_run_jnb/Power_function-output.ipynb",,,,
```
At command line the output is returned only in verbose mode (the tuple is serialised as a csv).

*np_arange_args* and *exponent* can be parametrised:
```python
# parametrise using keyword arguments
>>> run_jnb('./Power_function.ipynb', return_mode=True, exponent=3, np_arange_args={'start':-20,'stop':20,'step':0.1})
# parametrise mixing keyword arguments and arg parameter
>>> run_jnb('./Power_function.ipynb', return_mode=True, arg='{"exponent":3}', np_arange_args={'start':-20,'stop':20,'step':0.1})
# parametrise using arg parameter with a json file
>>> run_jnb('./Power_function.ipynb', return_mode=True, arg='./power_function_arg.json')

('.../_run_jnb/Power_function-output (1).ipynb', None, None, None, None)
```
where in the last example [*power_function_arg.json*](example/power_function_arg.json) contains:
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

If the generated notebook contains an error:
```python
>>> run_jnb('./Power_function.ipynb', return_mode=True, exponent=1, np_arange_args={'step':0.1})
('.../_run_jnb/Power_function-output (2).ipynb', 3, 'TypeError', "Required argument 'start' (pos 1) not found", ...)
```
the second element in the returned tuple (3 in thise case) is the prompt number of the cell where the error was caught (please see the [generated notebook](example/_run_jnb/Power_function-output%20(3).ipynb)).


## Dependencies
- [python](https://www.python.org): 3.5 or higher
- [nbconvert](http://nbconvert.readthedocs.io): 4.2 or higher

## License
[BSD 3](LICENSE)

## Acknowledgments
[nbrun](https://github.com/tritemio/nbrun) and [nbparameterise](https://github.com/takluyver/nbparameterise) were a source of inspiration.
