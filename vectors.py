"""
NotebookRepositoryAnalyzer() takes an arbitrary collection of IPython
notebooks and generates one vector of floats per notebook,
suitable for wrapping in a Pandas Dataframe.

Values in the vector are currently the average value per-cell of mostly
boolean analysis functions, cast to 1.0 or 0.0. There's also a
lines-per-cell function.

Primary TODO:
  figure out which features meaningfully identify notebook characteristics

We should add some notebook-wise features: are cells in order?

Alternate approaches to explore:
  - within a notebook, create a vector from each cell
    + analyze at notebook level or have notebooks be multi-dimensional vectors
    + pivot the analysis, building the vectors cellwise rather than featurewise

Use:
>>> findings = analyze_tree('/path/to/directory/of/notebooks')
>>> import pandas as pd
>>> df = pd.DataFrame(findings['notebooks'], columns=findings['labels'])

More features to add:
cellwise:
  writes data to:?
  uses shell: line begins with '!'
    -> similar for '%', '%%', ...
    -> linewise?
repo-wise:
  cluster repo:
    examine lengths of intersections of the sets of cell hashes
    relative to the overall notebook lengths
      maybe also check basenames

Other TODO:
  work with other notebook versions
  write unit tests for features
    -> base on cells extracted from working notebooks
  cellwise: actually compile code and inspect instead of regex/string match
"""
import os, re, ujson as json
from collections import defaultdict


def is_code(cell):
    return int(cell['cell_type'] == 'code')

SPARK_NAMES = [
    'pyspark',
    'spark',
    'sqlContext',
    'sqlCtx',
    'SQLContext',
    'SparkContext',
    'SparkSession'
]
SPARK_PATTERN = '|'.join(SPARK_NAMES)


def probably_uses_pyspark(cell):
    if cell['cell_type'] != 'code':
        return 0
    if re.search(SPARK_PATTERN, ''.join(cell['source'])):
        return 1
    return 0


def probably_uses_s3(cell): # XXX this is terrible
    if 's3://' in ''.join(cell['source']):
        return 1
    return 0


def draws_graph(cell):
    if 'plot(' in ''.join(cell['source']):
        return 1
    return 0


def has_traceback(cell):
    return int('Traceback' in ''.join(cell['source']))


def lines(cell):
    return len([l for l in cell['source'] if l.strip()])


def hash_cell(cell):
    # XXX add for other cell types
    if cell['cell_type'] != 'code':
        return 0
    # XXX make more resilient to trivial differences
    return hash(''.join(cell['source']))


def has_ordered_cells(notebook):
    i = 1
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        if i != cell['execution_count']:
            return 0
        i += 1
    return 1


CELLWISE = [
    probably_uses_pyspark,
    probably_uses_s3,
    draws_graph,
    has_traceback,
    lines
]

NOTEBOOKWISE = [
    has_ordered_cells,
]


class NotebookRepositoryAnalyzer(object):

    def __init__(self, notebooks=None, **config):
        self.cellwise = CELLWISE
        self.notebookwise = NOTEBOOKWISE
        if config:
            self.__dict__.update(config)
        self.findings = {}
        if notebooks:
            map(self.analyze_notebook, notebooks)

    def analyze_notebook(self, notebook, name):
        try:
            if notebook['nbformat'] != 4:
                return
        except KeyError:
            return
        self.findings['labels'] = ['is_code'] + [
            f.func_name for f in self.cellwise]
        self.findings['notebooks'] = self.findings.get('notebooks', [])
        cells = defaultdict(float)
        for cell in notebook['cells']:
            if is_code(cell):
                cells[0] += 1.0
                for i, f in enumerate(self.cellwise):
                    index = i + 1
                    cells[index] += f(cell)
        result = []
        width = range(len(cells))
        height = len(notebook['cells'])
        for i in width:
            result.append(round(cells[i]/height, 2))
        self.findings['notebooks'].append(result)

    def finish_analysis(self):
        return self.findings # XXX

        for f in self.repositorywise:
            self.findings[f.func_name] = f(self.findings)
        return self.findings


def analyze_tree(path):
    an = NotebookRepositoryAnalyzer()
    for root, dirnames, filenames in os.walk(path):
        for basename in filenames:
            if not basename.endswith('.ipynb'):
                continue
            notebook = json.load(open(os.path.join(root, basename)))
            an.analyze_notebook(notebook, basename)
    return an.finish_analysis()
