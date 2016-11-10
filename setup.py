from setuptools import setup

setup(
    name='jupyter-parser',
    version='0.0.1',
    py_modules=['parser'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        jupyter-parser=jupyter_parser:parse
    ''',
)
