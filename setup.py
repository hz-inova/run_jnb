# -*- coding: utf-8 -*-
import run_jnb

from setuptools import setup
setup(
    name = 'run_jnb',
    packages = ['run_jnb'],
    description = 'Parametrise (python3 only) and execute Jupyter notebooks',
    version = run_jnb.__version__,
    author = 'Andrei V. Plamada',
    author_email = 'andreiplamada@gmail.com',
    url = 'https://github.com/hz-inova/run_jnb',
    #download_url = 'https://github.com/hz-inova/run_jnb/archive/v0.1.tar.gz',
    #keywords = ['jupyter-notebook','execute','parametrized'],
    python_requires = '>=3.5',
    install_requires = ['nbconvert>=4.2'],
    classifiers = ['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: BSD License',
                   ],
)
