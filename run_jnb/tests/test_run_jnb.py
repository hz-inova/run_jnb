# -*- coding: utf-8 -*-
import sys
import io
import os
from ..run_jnb import main

# https://stackoverflow.com/questions/22822267/python-capture-print-output-of-another-module

def test_run_jnb_command_line():
    input_path = r'./example/Power_function.ipynb'
    sys.stdout = io.StringIO()
    sys.argv=['run_jnb',input_path,'-m','false','-vvv']
    main()
    output = sys.stdout.getvalue()
    assert output[:-1]==',,,,'+os.linesep