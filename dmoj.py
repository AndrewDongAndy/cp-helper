from .judge import Judge

from bs4 import BeautifulSoup


class Dmoj(Judge):
    name = 'DMOJ'
    github_repo = 'dmoj-solutions'
    github_directory = ''

    @staticmethod
    def link(problem_id):
        return f'https://dmoj.ca/problem/{problem_id}'

    @staticmethod
    def get_contest_suffix(index):
        # DMOJ contests usually use 1, 2, ...
        return f'{index + 1}'

    @classmethod
    def get_input_data(cls, html: str) -> list[str]:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('h4')
        input_data: list[str] = []
        for tag in tags:
            if tag.text.startswith('Sample Input'):
                nxt = tag.next_sibling
                if nxt == '\n':
                    nxt = nxt.next_sibling
                data = nxt.text
                input_data.append(data)
        return input_data
