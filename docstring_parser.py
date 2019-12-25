# https://github.com/openstack/rally/blob/7153e0cbc5b0e6433313a3bc6051b2c0775d3804/rally/common/plugin/info.py#L63-L110

import re
import sys

PARAM_OR_RETURNS_REGEX = re.compile(":(?:param|returns)")
RETURNS_REGEX = re.compile(":return: (?P<doc>.*)", re.S)
PARAM_REGEX = re.compile(":param (?P<name>[\*\w]+): (?P<doc>.*?)"
                         "(?:(?=:param)|(?=:return)|(?=:raises)|\Z)", re.S)


def trim(docstring):
    """trim function from PEP-257"""
    if not docstring:
        return ""
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    # Current code/unittests expects a line return at
    # end of multiline docstrings
    # workaround expected behavior from unittests
    if "\n" in docstring:
        trimmed.append("")

    # Return a single string:
    return "\n".join(trimmed)


def reindent(string):
    return "\n".join(l.strip() for l in string.strip().split("\n"))


def pre_process(docstring):
    """

    """
    processed_text = []
    processed_params = []

    if docstring:
        # Replace
        docstring = docstring.replace("'", "\"")

        trim_text = trim(docstring)
        text_splitted = trim_text.split('\n')
        new_line = ""

        for idx, line in enumerate(text_splitted):
            if not line:
                processed_text.append(new_line)
                new_line = ""
            if ':return' in line or ':param' in line:
                processed_params.append(new_line)
                new_line = ""

            new_line += " " + line

    return "\n".join(processed_text + processed_params)


def parse_docstring(docstring):
    """Parse the docstring into its components.
    :returns: a dictionary of form
              {
                  "short_description": ...,
                  "long_description": ...,
                  "params": [{"name": ..., "doc": ...}, ...],
                  "returns": ...
              }
    """

    short_description = long_description = returns = ""
    params = []

    if docstring:
        docstring = trim(docstring)

        lines = docstring.split("\n", 1)
        short_description = lines[0]

        if len(lines) > 1:
            long_description = lines[1].strip()

            params_returns_desc = None

            match = PARAM_OR_RETURNS_REGEX.search(long_description)
            if match:
                long_desc_end = match.start()
                params_returns_desc = long_description[long_desc_end:].strip()
                long_description = long_description[:long_desc_end].rstrip()

            if params_returns_desc:
                params = [
                    {"name": name, "doc": trim(doc)}
                    for name, doc in PARAM_REGEX.findall(params_returns_desc)
                ]

                match = RETURNS_REGEX.search(params_returns_desc)
                if match:
                    returns = reindent(match.group("doc"))

    return {
        "short_description": short_description,
        "long_description": long_description,
        "params": params,
        "returns": returns
    }


def docstring_to_yaml(docstring_dict):
    """

    """



data = """
Generate and unique name for the document, store the file locally, then
request documentservice to upload the file

long description
Generate and unique name for the document, store the file locally, then
request documentservice to upload the file
    :param token: String, authentication token. Ie, "kj2xlj3lkjlj"
    :param client_id: ID of the current client, Ie. 1
    :param document_file: Document to be uploaded. FileStorage
    :param stipulation_type: String, stipulation type. Ie, "STANDARD"
    :param stipulation_id: Integer, stipulation identifier. Ie. 1
    :param application_id: Integer, unique application identifier. Ie, 2
    :param owner_data: Dict. data from an owner. Ie, { owner_id: 10, owner_type: 'OWNER' }
    :param is_credit_memo_file: Boolean. indicates if the file comes from credit memo. Ie, True
    :param custom_document_type: str, the custom document type if it is not related to application. Ie. 'payments'
    :param origin: String, origin of the call. Ie, 'PP'
    :param document_form: Document form data. DocumentForm
    :return: the generated File data. Ie, {
            owner_id: 10, 
            owner_type: 'OWNER'
        }
"""

print(pre_process(data))
# pre_process(data)
