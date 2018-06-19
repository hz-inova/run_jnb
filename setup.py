# -*- coding: utf-8 -*-
import run_jnb

from setuptools import setup
setup(
    name = 'run_jnb',
    packages = ['run_jnb'],
    entry_points = { "console_scripts": ['run_jnb = run_jnb.run_jnb:main']},
    description = 'Parametrise (python3 only) and execute Jupyter notebooks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version = run_jnb.__version__,
    author = 'Andrei V. Plamada',
    author_email = 'andreiplamada@gmail.com',
    url = 'https://github.com/hz-inova/run_jnb',
    license = 'BSD 3-clause "New" or "Revised" License',
    keywords = ['jupyter-notebook', 'execute', 'parametrise'],
    python_requires = '>=3.5',
    install_requires = ['nbconvert>=4.2'],
    classifiers = ['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: BSD License',
                   ],
)
