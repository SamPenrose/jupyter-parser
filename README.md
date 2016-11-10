# jupyter-parser

jupyter-parser is a jupyter notebook parser that attempts to gather information
about the varying ways in which a notebook may be used. The current plugins written
to parse notebook files are found in the **plugins** directory and are described
below

Plugins
- CellsCorrectPlugin: determines whether or not cells are in the correct execution order
- NotebookLibrariesPlugin: determines the modules imported from the notebooks (can be local)
- NotebookSparkPlugin: uses a regular expression to search for any pyspark variables

Plugins are included in the constructor of the main parser(JupyterParser).
This architecture is likely to be temporary as the goal of being language/file
agnostic is in the future.

This library should be used with **[gist-dl](https://github.com/cameres/gist-dl)** in order to quickly download example notebooks from **[gist.github.com](http://gist.github.com)**.
