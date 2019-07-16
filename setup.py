# -*- coding: utf-8 -*-
from setuptools import setup
import os,codecs,re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'run_jnb',
    packages = ['run_jnb'],
    entry_points = { "console_scripts": ['run_jnb = run_jnb.run_jnb:main']},
    description = 'Parametrise (python3 only) and execute Jupyter notebooks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version = find_version("run_jnb", "__init__.py"),
    author = 'Andrei V. Plamada',
    author_email = 'andreiplamada@gmail.com',
    url = 'https://github.com/hz-inova/run_jnb',
    license = 'BSD 3-clause "New" or "Revised" License',
    keywords = ['jupyter-notebook', 'execute', 'parametrise'],
    python_requires = '>=3.5',
    install_requires = ['nbconvert>=4.2,!=5.4'],
    classifiers = ['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: BSD License',
                   ],
)
