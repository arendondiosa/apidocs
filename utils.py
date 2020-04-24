# https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
from os.path import isfile, join
from itertools import izip
from glob import glob

import re

from docstring_parser import parse_docstring, docstring_to_yaml


def grouped(iterable, n):
    """
    Create subgroups of elements in a List
    :param iterable: List, List to split in groups. Ie, [1, 2, 3, 4, 5]
    :param n: Integer, Number of subgroups. Ie, 2
    :return: List, Subgroups. Ie, [
            (1, 2), (3, 4), ...
        ]
    """
    return izip(*[iter(iterable)] * n)


def get_tab_size(line):
    """
    Returns the initial tab size in a line
    :param line: String, Line to inspect. Ie, "    Some line with tabs"
    :return: Integer, Tab size in spaces. Ie, 4
    """
    count = 0

    for char in line:
        if char == ' ':
            count += 1
    return count


def comment_block(block_string, comment=False):
    """
    Comment/Uncomment a block of strings
    :param block_string: String, block of code to comment.
    :param comment: Boolean, Flag to enable/disable functionality
    """
    block = block_string.split('\n')

    if comment:
        commented_block = ['# ' + line for line in block if line]
    else:
        commented_block = [line.replace('# ', '') for line in block if line]

    commented_block = '\n'.join(commented_block) + '\n'
    return commented_block


def file_docstring_to_yaml(input_file, output_file=None, resource=None, comment=None):
    """
    Parse all docstrings in a file.
    :param input_file: String, name of a file or directory. Ie, "/Users/user/LendingFront/originationservice/app/api/"
    :param output_file: String, name of a file or directory to store the content parsed. Ie, "/Users/user/LendingFront/originationservice/app/api/"
    :param resource: Boolean, Enable the parser for endpoints type resource. Ie, True or False
    :param comment: Boolean, Comment a docstring when is parsed. Ie, True or False
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
        parse = False

        if resource:
            for http_rule in http_rules:
                if ('def ' + http_rule + '(') in content[init - 1]:
                    parse = True
        else:
            parse = True

        if parse:
            docstring = parse_docstring(docstring)
            docstring = docstring_to_yaml(
                docstring, get_tab_size(content[init]) / 4)

            output_data += ''.join(content[last_index:init + 1])
            output_data += comment_block(docstring, comment)

            last_index = end
    output_data += ''.join(content[last_index:len(content)])

    if output_file is None:
        output_file = input_file

    text_file = open(output_file, "w")
    text_file.write(output_data)
    text_file.close()


def display_docs_file(input_file):
    """
    Display a list of docstrings in a file
    :param input_file: String, name of a file or directory. Ie, "/Users/user/LendingFront/originationservice/app/api/"
    """
    with open(input_file, 'r') as f:
        content = f.readlines()

    content = [x for x in content]

    docstring_indexes = [e for e, line in enumerate(content) if '"""' in line]

    # Get sublist with docstrings
    for init, end in grouped(docstring_indexes, 2):
        docstring = content[init + 1:end]
        docstring = ''.join(docstring)  # Docstring to string

        print(docstring)


def folder_docstring_to_yaml(path, file_extension='py', output_file=None, resource=None, comment_docstring=None):
    """
    Parse all docstrings inside a folder. Iterates over all files
    :param path: String, name of a file or directory. Ie, "/Users/user/LendingFront/originationservice/app/api/"
    :param file_extension: String, file suffix or a filename extension. Ie, "py", "txt"
    :param output_file: String, name of a file or directory to store the content parsed. Ie, "/Users/user/LendingFront/originationservice/app/api/"
    :param resource: Boolean, Enable the parser for endpoints type resource. Ie, True or False
    :param comment_docstring: Boolean, Comment a docstring when is parsed. Ie, True or False
    """
    files = glob(path + "/*." + file_extension)

    for file in files:
        file_docstring_to_yaml(file, output_file, resource, comment_docstring)


def folder_display_docs(path, file_extension='py'):
    """
    Display all docstrings inside a folder. Iterates over all files
    :param path: String, name of a file or directory. Ie, "/Users/user/LendingFront/originationservice/app/api/"
    :param file_extension: String, file suffix or a filename extension. Ie, "py", "txt"
    """
    files = glob(path + "/*." + file_extension)

    for file_item in files:
        print('--- PATH: {0}'.format(file_item))
        print('--- DOCSTRING(s):')
        display_docs_file(file_item)
