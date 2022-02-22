from .judge import Judge

from pprint import pprint

from bs4 import BeautifulSoup


class Boj(Judge):
    name = 'Baekjoon Online Judge'
    github_repo = 'cp-solutions'
    github_directory = 'boj'

    @staticmethod
    def link(problem_id):
        return f'https://www.acmicpc.net/problem/{problem_id}'

    @staticmethod
    def local_directory_and_filename_no_ext(problem_id, suffix=None):
        filename = f'boj_{problem_id}'
        if suffix is not None:
            filename += f'_{suffix}'
        return (f'boj_{problem_id}', filename)

    @classmethod
    def get_input_data(cls, html: str) -> list[str]:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.select('pre.sampledata')
        input_data: list[str] = []
        for tag in tags:
            if tag.get('id').startswith('sample-input'):
                data = tag.text.replace('\r\n', '\n')
                input_data.append(data)
        return input_data
