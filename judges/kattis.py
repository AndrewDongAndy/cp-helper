from .judge import Judge

from bs4 import BeautifulSoup
import requests


def contest_url(contest_id: str) -> str:
    return f'https://{contest_id}.kattis.com/problems'


class Kattis(Judge):
    name = 'Kattis'
    github_repo = 'cp-solutions'
    github_directory = 'kattis'

    @staticmethod
    def link(problem_id: str) -> str:
        # if '_' in problem_id:
        #     subdomain, problem_code = problem_id.split('_')
        # else:
        #     subdomain = 'open'
        #     problem_code = problem_id
        # return f'https://{subdomain}.kattis.com/problems/{problem_code}'
        return 'kattis source is too annoying to track'

    @staticmethod
    def get_suffix_for_contest(index) -> str:
        return chr(ord('A') + index)

    @classmethod
    def get_input_data(cls, html: str) -> list[str]:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.select('table.sample')
        print(tags)
        return []
        input_data: list[str] = []
        for tag in tags:
            if tag.text.startswith('Sample Input'):
                nxt = tag.next_sibling
                if nxt == '\n':
                    nxt = nxt.next_sibling
                data = nxt.text
                input_data.append(data)
        return input_data

    # @classmethod

    # @classmethod
    # def download_contest(cls, contest_id) -> bool:
    #     res = requests.get(contest_url(contest_id))
    #     if not (200 <= res.status_code < 300):
    #         return False
    #     html = res.text
    #     soup = BeautifulSoup(html, 'html.parser')
    #     anchor_tags = soup.select('tr > td.id > a')
    #     problems = [tag.text.strip() for tag in anchor_tags]
    #     cls.make_contest_files(contest_id, problem_id_suffixes=problems)
