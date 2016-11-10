import re
from collections import Counter

class NotebookLibrariesPlugin(object):
    '''
    are all the cells in the correct order?
    '''
    def __init__(self):
        self.libraries_in_notebook = {}

    def parse_notebook(self, filename, notebook):
        if 'cells' not in notebook:
            # we don't handle v3 for now
            return
        # this pattern has gotten weaker from original
        pattern = r'^(?:from|import)\s+([\w.]*)\s+'
        cells = notebook['cells']
        execution_cells = [cell for cell in cells if cell['cell_type'] == 'code']
        modules = []
        for cell in execution_cells:
            # determine if any libraries have been used w/ regular expressions
            source = cell['source']
            source = ''.join(source)
            modules += re.findall(pattern, source)

        self.libraries_in_notebook[filename] = modules

    def summary(self):
        libraries_across_notebooks = []
        for (filename, libraries) in self.libraries_in_notebook.items():
            print('\t%s : %s' %(libraries, filename))
            libraries_across_notebooks += libraries

        hist = Counter(libraries_across_notebooks)
        print('Overall Library Usage: %s' %(hist))
