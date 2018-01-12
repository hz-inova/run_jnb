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

## Simple example
### Python Package

The package contains two public functions ***possible_parameter*** and ***run_jnb*** (see the docstring).

```python
>>> from run_jnb import possible_parameter, run_jnb
```
Consider the [notebook]example/Power_function.ipynb).

***possible_parameter*** returns an *OrderedDict* where the key is the parameter name and the value is the cell index where the parameter is assigned.

```python
>>> possible_parameter('./Power_function.ipynb')
OrderedDict([('v', 1), ('power', 3)])
```
The notebook contains two possible parameters ***v*** and ***power***. The first variable is not json serialisable so next ***power*** is used as argument using ***run_jnb***.

***run_jnb*** returns a tuple with three elements:
- the first element is the output of **sys.exc_info()**, 
- the second element is the path of the generated notebook,
- the third element is execution_count of the cell where the error is catched.

```python
>>> run_jnb("./Power_function.ipynb", return_mode=True, power=1)
((None, None, None), './_run_jnb/Power_function-output.ipynb', None)
```
Please see the [generated notebook](example/_run_jnb/Power_function-output.ipynb). Same output can be obtained by using ***arg*** parameter of ***run_jnb***:
```python
>>> run_jnb("./Power_function.ipynb", return_mode=True, arg='{"power":1}')
```

### Command Line Tool
***run_jnb*** can be used at command line. The output is return only when the verbose flag is used. The returned tuple is serialised to json (the first element of the tuple is represented as a string before the serialisation):
```sh
# macOS or Linux bash terminal (" can be escaped by \")
$ run_jnb ./Power_function.ipynb -m true -a "{\"power\":1}" -v
[["None", "None", "None"], "./_run_jnb/Power_function-output.ipynb", null]

# Windows cmd (" can be escaped by "") 
> run_jnb ./Power_function.ipynb -m true -a "{""power"":1}" -v
[["None", "None", "None"], "./_run_jnb/Power_function-output.ipynb", null]
```

The documentation is available via 
```sh
run_jnb -h
```

## Dependencies
- [python](https://www.python.org): 3.5 or higher
- [nbconvert](http://nbconvert.readthedocs.io): 4.2 or higher

## License
[BSD 3](LICENSE)

## Acknowledgments
[***nbrun***](https://github.com/tritemio/nbrun) 
