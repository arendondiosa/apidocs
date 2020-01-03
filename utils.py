# https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
from os.path import isfile, join
from itertools import izip
from glob import glob

import re

from docstring_parser import parse_docstring, docstring_to_yaml


def grouped(iterable, n):
    return izip(*[iter(iterable)]*n)


def get_tab_size(line):
    count = 0

    for char in line:
        if char == ' ':
            count += 1
    return count


def file_docstring_to_yaml(input_file, output_file=None):
    """

    """
    content = []
    http_rules = ['get', 'post', 'put', 'delete']
    output_data = ''

    with open(input_file, 'r') as f:
        content = f.readlines()

    content = [x for x in content]

    docstring_indexes = [e for e, line in enumerate(content) if '"""' in line]

    last_index = 0
    # Get sublist with docstrings
    for init, end in grouped(docstring_indexes, 2):
        docstring = content[init + 1:end]
        docstring = ''.join(docstring)  # Docstring to string

        for http_rule in http_rules:
            if ('def ' + http_rule + '(') in content[init - 1]:
                docstring = parse_docstring(docstring)
                docstring = docstring_to_yaml(
                    docstring, get_tab_size(content[init]) / 4)

        output_data += ''.join(content[last_index:init + 1])
        output_data += docstring

        last_index = end
    output_data += ''.join(content[last_index:len(content)])

    if output_file is None:
        output_file = input_file

    text_file = open(output_file, "w")
    text_file.write(output_data)
    text_file.close()


def folder_docstring_to_yaml(path):
    """

    """
    files = glob(path + "/*.py")

    for file in files:
        file_docstring_to_yaml(file)