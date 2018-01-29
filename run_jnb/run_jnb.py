# -*- coding: utf-8 -*-

import argparse as argparse
import json as json
import csv
from io import StringIO

from nbconvert.preprocessors import ExecutePreprocessor as EP

from .core import run_jnb


def main():
    parser = argparse.ArgumentParser(description='Execute and parametrise (python3 only) jupyter notebooks.')
    parser.add_argument("input_path", help="path of input jupyter notebook")
    parser.add_argument("-o", "--output_path", help="path of the output jupyter notebook. The input path can be used as relative path by starting with '///' . * can be used once at the beggining or at the end as a wildcard of the input_path filename, excluding the '.ipynb' extension.",
                        default=r"///_run_jnb/*-output", type=str)
    parser.add_argument("-e", "--execution_path", help="path of the folder where to execute the notebook.  r'///input' or r'///output' can be used to denote the input / output folder.",
                        default=r'///input', type=str)
    parser.add_argument("-m", "--return_mode", help="flag to write the generated notebook to the output_path. 'parametrise_only' to just parametrise the notebook without executing it, 'except' to write just in case of an error and true /false to write it always /never.",
                        choices=['parametrise_only','except', 'true', 'false'], default='except')
    parser.add_argument("-O", "--overwrite", help="overwrite output_path if exists. If the parameter is False the used output_path will be incremented until a valid one is found.",
                        action='store_true', default=False)
    parser.add_argument("-t", "--timeout", help="ExecutePreprocessor.timeout",
                        type=int, default=EP.timeout.default_value)
    parser.add_argument("-k", "--kernel_name", help="ExecutePreprocessor.kernel_name",
                        type=str, default=EP.kernel_name.default_value)
    parser.add_argument('-E', "--ep_kwargs", help="other ExecutePreprocessor parameters as keyword arguments",
                        default=None, type=str)
    parser.add_argument('-M',"--end_cell_index", help="End cell index used to slice the notebook in finding the possible parameters.", default=None, type=int),
    parser.add_argument('-a', "--arg", help="jupyter notebook argument as json file or as json string (python3 only)",
                        default=None, type=str)
    parser.add_argument("-v", "--verbose", help="verbose mode to write the returned output as csv. -v for the path of the generated notebook and th error prompt number. -vv appends also the error type and value. -vvv or more appends the error traceback.", action='count')

    args = parser.parse_args()

    if args.return_mode not in ['except','parametrise_only']:
        args.return_mode = json.loads(args.return_mode)

    if args.ep_kwargs is not None:
        args.ep_kwargs = json.loads(args.ep_kwargs)
    res = run_jnb(input_path=args.input_path, output_path=args.output_path,
                  execution_path=args.execution_path,
                  return_mode=args.return_mode, overwrite=args.overwrite,
                  timeout=args.timeout, kernel_name=args.kernel_name,
                  ep_kwargs=args.ep_kwargs,end_cell_index=args.end_cell_index,
                  arg=args.arg)

    output = StringIO()
    writer = csv.writer(output)

    if args.verbose is None:
        pass
    elif args.verbose == 1:
        writer.writerow(res[:2])
    elif args.verbose == 2:
        writer.writerow(res[:-1])
    elif args.verbose > 2:
        writer.writerow(res)

    if args.verbose is not None:
        print(output.getvalue())
