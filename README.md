# run_jnb

**run_jnb** is a python package and command line tool for parametrising (python3 only) and executing Jupyter notebooks.

- **Source**: [https://github.com/hz-inova/run_jnb](https://github.com/hz-inova/run_jnb)

## Install

```sh
pip install run_jnb
```

## Usage

For a notebook written in python one can find the possible parameters. This is achived by parsing the abstract syntax tree of the code cells. A variable can be a possible parameter if:
- it is defined in a cell that contains only comments or assignments (clean cell requirement),
- its name is not used previously beside the assignment (function parameter requirement).

One can pass arguments as keyword arguments or in a json format (file or string). For safety reasons, in order to avoid any code injection, only json serialisable keywords arguments are available. The keyword arguments are firstly encoded in json format using the standard [json encoder](https://docs.python.org/3.6/library/json.html#json.JSONEncoder). The json format is decoded into python objects using the standard [json decoder](https://docs.python.org/3.6/library/json.html#json.JSONDecoder) and it is mapped to a keyword argument by unpacking its content.

The generated notebook (parametrised or not) can be easily executed (the implementation relies on [nbconvert Executing notebooks](http://nbconvert.readthedocs.io/en/latest/execute_api.html)).

The package contains two public functions ***possible_parameter*** and ***run_jnb*** (see the docstring).

***run_jnb*** is available also as a command line tool and its documentation is available via 
```sh
run_jnb -h
```

## Simple example

```python
>>> from run_jnb import possible_parameter, run_jnb
```
Consider the [notebook]example/Power_function.ipynb).

***possible_parameter*** returns an *OrderedDict* where the key is the parameter name and the value is the cell index where the parameter is assigned.

```python
>>> possible_parameter('./Power_function.ipynb')
OrderedDict([('np_arange_args', 4), ('x', 5), ('exponent', 7), ('y', 9)])
```
The notebook contains several possible parameters. 

Next we will parametrise the *exponent* using ***run_jnb***.

***run_jnb*** returns a tuple with three elements:
- the first element is the path of the generated notebook, 
- the second element is the prompt number of the cell where the error is catched,
- the third element is the output of **sys.exc_info()**.

```python
>>> run_jnb("./Power_function.ipynb", return_mode=True, exponent=1)
('./_run_jnb/Power_function-output.ipynb', None, (None, None, None))
```
Please see the [generated notebook](example/_run_jnb/Power_function-output.ipynb). Same output can be obtained by using *arg* parameter of ***run_jnb***:
```python
>>> run_jnb("./Power_function.ipynb", return_mode=True, arg='{"exponent":1}')
```
or using the command line tool. At command line the output is return only when the verbose flag is used (the tuple is serialised to json):
```sh
# macOS or Linux bash terminal (" can be escaped by \")
$ run_jnb ./Power_function.ipynb -m true -a "{\"exponent\":1}" -v
[["None", "None", "None"], "./_run_jnb/Power_function-output.ipynb", null]

# Windows cmd (" can be escaped by "") 
> run_jnb ./Power_function.ipynb -m true -a "{""exponent"":1}" -v
[["None", "None", "None"], "./_run_jnb/Power_function-output.ipynb", null]
```
 *np_arange_args* and *exponent* can be parametrised:
 ```python
>>> run_jnb("./Power_function.ipynb", return_mode=True, exponent=1, np_arange_args={'start':-20,'stop':20,'step':0.1})
('./_run_jnb/Power_function-output (1).ipynb', None, (None, None, None))
```
Please see the [generated notebook](example/_run_jnb/Power_function-output (1).ipynb).

If the generated notebook contains an error:
 ```python
>>> run_jnb("./Power_function.ipynb", return_mode=True, exponent=1, np_arange_args={'step':0.1})
('./_run_jnb/Power_function-output (2).ipynb', 3, (nbconvert.preprocessors.execute.CellExecutionError, ...)
```
the second element in the returned tuple is the prompt number (please see the [generated notebook](example/_run_jnb/Power_function-output (2).ipynb)).


## Dependencies
- [python](https://www.python.org): 3.5 or higher
- [nbconvert](http://nbconvert.readthedocs.io): 4.2 or higher

## License
[BSD 3](LICENSE)

## Acknowledgments
[***nbrun***](https://github.com/tritemio/nbrun) 
