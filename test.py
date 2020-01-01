from docstring_parser import parse_docstring, docstring_to_yaml

def main():
    """
    Main function
    """
    data = """
        Getting a list of applications applying some filters and sort fields as params        
        :return: Json, Applications from the query. Ie
            {
                data: {
                    'applications': [
                        {
                            application_business": 4687,
                            "application_number": "497083110106922",
                            "cents_on_the_dollar": 0.0,
                            "channel": "ISO",
                            "client_id": 6,
                            ...
                        }
                        ...
                    ],
                    'total_applications': 100
                }
            }
        """

    docstring = parse_docstring(data)
    # print(docstring)
    print(docstring_to_yaml(docstring))


if __name__ == "__main__":
  main()
