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


def clean_multiple_white_spaces(string):
    return ' '.join(string.split())


def pre_process(docstring):
    """Parse the docstring into its components.
    :returns: a dictionary of form
              {
                  "short_description": ...,
                  "long_description": ...,
                  "params": [{"name": ..., "doc": ..., "example": ..., "type": ...}, ...],
                  "returns": ...
              }
    """
    processed_text = []

    if docstring:
        # Replace
        docstring = docstring.replace("'", "\"")

        trim_text = trim(docstring)
        text_splitted = trim_text.split('\n')
        new_line = ""

        for line in text_splitted:
            if not line or ':param' in line or ':return' in line:
                processed_text.append(new_line)
                new_line = ""
            
            new_line += line + " "

    return "\n".join(processed_text)


def parse_docstring(docstring):
    """
    Parse the docstring into its components.
    :docstring: String, docstring content
    :returns: a dictionary of form. Ie,
        {
            "short_description": ...,
            "long_description": ...,
            "params": [{"name": ..., "doc": ..., "example": ..., "type": ...}, ...],
            "returns": ...
        }
    """

    short_description = long_description = returns = ""
    params_type_list = ['String', 'string', 'Str', 'str',
                   'Integer', 'integer', 'Int', 'int',
                   'Boolean, boolean, Bool, bool',
                   'Dict', 'dict', 'Dictionary', 'dictionary',
                   'List', 'list', 'Lst', 'lst']
    params = []

    if docstring:
        docstring = pre_process(trim(docstring))
        
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

            # Params
            if params_returns_desc:
                params = []

                for name, doc in PARAM_REGEX.findall(params_returns_desc):
                    example = ""

                    for word in ['Ie.', 'Ie,', 'ie.', 'ie', 'IE.', 'IE']:
                        if word in doc:
                            doc = doc.replace(word, 'Ie,')
                            doc, example = doc.split('Ie,')
                            example = example.replace('\n', '') # Clean end of line
                            example = clean_multiple_white_spaces(example) # Clean multiple white spaces

                    # Define params type
                    param_type = doc.split(' ', 1)[0]

                    for char in ['.', ',']:
                        if char in param_type:
                            param_type = param_type.replace(char, '')

                    if param_type in params_type_list:
                        doc = ' '.join(doc.split(' ')[1:])
                    else:
                        param_type = ''

                    params.append({"name": name, "doc": trim(doc), "example": example, "type": param_type})

                # Return
                match = RETURNS_REGEX.search(params_returns_desc)
                if match:
                    returns = reindent(match.group("doc"))
                    return_doc = ''
                    return_example = ''

                    for word in ['Ie.', 'Ie,', 'ie.', 'ie', 'IE.', 'IE']:
                        if word in returns:
                            returns = returns.replace(word, 'Ie,')
                            return_doc, return_example = returns.split('Ie,')
                            return_example = return_example.replace('\n', '') # Clean end of line
                            return_example = clean_multiple_white_spaces(return_example) # Clean multiple white spaces

                    returns = { "doc": return_doc, "example": return_example }

    return {
        "short_description": short_description,
        "long_description": long_description,
        "params": params,
        "returns": returns
    }


def docstring_to_yaml(docstring_dict):
    """

    """
    yaml = ''



    return docstring_dict


def main():
    """
    Main function
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
        :param owner_data: Dict. data from an owner. Ie, 
            { 
                owner_id: 10, 
                owner_type: 'OWNER' 
            }
        :param is_credit_memo_file: Boolean. indicates if the file comes from credit memo. Ie, True
        :param custom_document_type: str, the custom document type if it is not related to application. Ie. 'payments'
        :param origin: String, origin of the call. Ie, 'PP'
        :param document_form: Document form data. DocumentForm
        :return: the generated File data. Ie, {
                owner_id: 10, 
                owner_type: 'OWNER'
            }
    """

    docstring = parse_docstring(data)
    print(docstring_to_yaml(docstring))


if __name__== "__main__":
  main()