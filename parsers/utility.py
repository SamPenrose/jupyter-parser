import os

def header(text):
    rows, columns = os.popen('stty size', 'r').read().split()
    text = ' ' + text + ' '
    return text.center(int(columns), "#")
