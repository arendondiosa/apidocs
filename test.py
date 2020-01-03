from docstring_parser import parse_docstring, docstring_to_yaml
from utils import file_docstring_to_yaml, folder_docstring_to_yaml


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

    # file_docstring_to_yaml(
    #     '/Users/rendon/LendingFront/originationservice/app/api/v1_1/resources/application_search.py')
    folder_docstring_to_yaml(
        '/Users/rendon/LendingFront/originationservice/app/api/v1_1/resources')


if __name__ == "__main__":
  main()
