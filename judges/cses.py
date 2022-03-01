from .judge import Judge

from pprint import pprint

from bs4 import BeautifulSoup


class Cses(Judge):
    name = 'CSES'
    github_repo = 'cp-solutions'
    github_directory = 'cses'

    @staticmethod
    def link(problem_id):
        return f'https://cses.fi/problemset/task/{problem_id}'

    @staticmethod
    def local_directory_and_filename_no_ext(problem_id, suffix=None):
        filename = f'cses_{problem_id}'
        if suffix is not None:
            filename += f'_{suffix}'
        return (f'cses_{problem_id}', filename)

    @classmethod
    def get_input_data(cls, html: str) -> list[str]:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.select('[id^=example]~code')
        # print(tags)
        input_data: list[str] = []
        if tags:
            input_data.append(tags[0].text)
        # for tag in tags:
        #     pprint(tag)
        #     input_data.append(tag.text)
        return input_data
