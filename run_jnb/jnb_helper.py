# -*- coding: utf-8 -*-

import copy
import nbformat
import os

from .util import _read_nb, sort_dict, variable_status
from nbconvert import PythonExporter

class _JupyterNotebookHelper:
    """


    Parameters
    ----------
    nb : str, nbformat.notebooknode.NotebookNode
        Jupyter notebook path or its content as a NotebookNode object.
    end_cell_index : int, optional
        End cell index used to slice the notebook in finding the possible parameters.

    Attributes
    ----------
    language : str
        Language used in the jupyter notebook from ['metadata']['kernelspec']['language'].
    language_version : str
        Version of the language from ['metadata']['language_info']['version']
    kernel : str
        Kernel name from ['metadata']['kernelspec']['name']
    cells : list
        Cells from ['cells']
    possible_param : collections.OrderedDict
        Ordered dictionary with possible parameters for the jupyter notebook.
        The key is the name of the variable and the value is the index of
        the cell where the variable is defined.
        The dictionary is ordered by the cell index.
    """
    def __init__(self, nb, end_cell_index=None):
        if isinstance(nb, nbformat.notebooknode.NotebookNode):
            pass
        elif isinstance(nb, str):
            if os.path.splitext(nb)[1]!='.ipynb':
                raise ValueError("The extension of the jupyter notebook = '{}' is not '.ipynb'".format(nb))
            nb = _read_nb(nb)
        else:
            raise TypeError()
        self.language = nb['metadata']['kernelspec']['language']
        self.language_version = nb['metadata']['language_info']['version']
        self.kernel = nb['metadata']['kernelspec']['name']
        self.nb = nb
        self.exporter = PythonExporter()

        if self.language == 'python' and self.language_version[0] == '3':
            self.possible_param = self._cell_index_of_possible_param(end_cell_index)
        else:
            self.possible_param = sort_dict({})

    def _cell_index_of_possible_param(self,end_cell_index):
        index_of_params = {}
        exclude_variable = set()
        new_nb = copy.deepcopy(self.nb)

        for i, cell in enumerate(self.nb['cells'][:end_cell_index]):
            if cell['cell_type'] == 'code':
                new_nb['cells'] = [cell]
                source, _ = self.exporter.from_notebook_node(new_nb)
                params, exclude_variable = variable_status(source,
                                                           exclude_variable)
                for param in params:
                    if param not in index_of_params.keys():
                        index_of_params[param] = i

        return sort_dict(index_of_params, by='value')
