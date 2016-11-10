import re

class NotebookSparkPlugin(object):
    '''
    are all the cells in the correct order?
    '''

    spark_variables = [
    'pyspark',
    'sc',
    'spark',
    'sqlContext',
    'sqlCtx',
    'SQLContext',
    'SparkContext',
    'SparkSession']

    def __init__(self):
        self.is_spark_notebook = {}


    def parse_notebook(self, filename, notebook):
        if 'cells' not in notebook:
            # we don't handle v3 for now
            # there is no way to see execution count
            return

        self.is_spark_notebook[filename] = False
        pattern = '|'.join(NotebookSparkPlugin.spark_variables)

        cells = notebook['cells']
        execution_cells = [cell for cell in cells if cell['cell_type'] == 'code']
        for cell in execution_cells:
            source = cell['source']
            source = ''.join(source)
            if re.search(pattern, source):
                self.is_spark_notebook[filename] = True

    def summary(self):
        spark_notebooks = sum(self.is_spark_notebook.values())
        total_notebooks = len(self.is_spark_notebook)

        print('Spark Notebooks: %s / %s' %(spark_notebooks, total_notebooks))
        for (filename, is_spark) in self.is_spark_notebook.items():
            print('\t%s : %s' %(filename, is_spark))
