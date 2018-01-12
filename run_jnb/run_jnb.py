# -*- coding: utf-8 -*-

import argparse as argparse
import json as json
from nbconvert.preprocessors import ExecutePreprocessor as EP
from .core import run_jnb

def main():
    parser = argparse.ArgumentParser(description='Run an input jupyter notebook file and optionally (python3 only) parametrise it.')
    parser.add_argument("input_path", help="path of input jupyter notebook")
    parser.add_argument("-o","--output_path", help="path of the output jupyter notebook. The input path can be used as relative path by starting with '///' . * can be used once in the beggining or end as a wildcard of the input_path filename, excluding the '.ipynb' extension.",
                        default=r"///_run_jnb/*-output", type=str)
    parser.add_argument("-e","--execution_path", help="path of the folder where to execute the notebook.  r'///input' or r'///output' can be used to denote the input / output folder.",
                        default=r'///input', type=str)
    parser.add_argument("-m","--return_mode", help="flag to write the generated notebook to the output_path",
                        choices=['except', 'true', 'false'], default='except')
    parser.add_argument("-O","--overwrite", help="overwrite output_path if exits",
                        action='store_true', default=False)
    parser.add_argument("-t","--timeout", help="ExecutePreprocessor.timeout",
                        type=int, default=EP.timeout.default_value)
    parser.add_argument("-k","--kernel_name", help="ExecutePreprocessor.kernel_name",
                        type=str, default=EP.kernel_name.default_value)
    parser.add_argument('-E',"--ep_kwargs", help="other ExecutePreprocessor parameters as keywords arguments",
                        default=None, type=str)
    parser.add_argument('-a',"--arg", help="jupyter notebook argument as json file or as json string (python3 only)",
                        default=None, type=str)
    parser.add_argument("-v", "--verbose", help="write the output",
                    action="store_true")


    args = parser.parse_args()

    if args.return_mode != 'except':
        args.return_mode = json.loads(args.return_mode)


    if args.ep_kwargs is not None:
        args.ep_kwargs = json.loads(args.ep_kwargs)
    res = run_jnb(input_path=args.input_path, output_path=args.output_path,
                  execution_path=args.execution_path,
                  return_mode=args.return_mode, overwrite=args.overwrite,
                  timeout=args.timeout,kernel_name=args.kernel_name,
                  ep_kwargs= args.ep_kwargs, arg=args.arg)

    if args.verbose:
        res = list(res)
        res[2]=[repr(el) for el in res[2] if el is not None]
        print(json.dumps(res))
