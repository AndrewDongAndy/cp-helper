from .judge import Judge

from bs4 import BeautifulSoup
import requests


def contest_url(contest_id: str) -> str:
    return f'https://atcoder.jp/contests/{contest_id}'


class AtCoder(Judge):
    name = 'AtCoder'
    github_repo = 'cp-solutions'
    github_directory = 'atcoder'

    @staticmethod
    def link(problem_id):
        """
        problem_id is of the following form: abc123_b
        """
        i = problem_id.index('_')
        assert i != -1
        contest_id = problem_id[:i]
        return f'https://atcoder.jp/contests/{contest_id}/tasks/{problem_id}'

    @staticmethod
    def get_contest_suffix(index) -> str:
        return chr(ord('a') + index)

    @classmethod
    def get_input_data(cls, html: str) -> list[str]:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('h3')
        input_data: list[str] = []
        for tag in tags:
            if tag.text.startswith('Sample Input'):
                nxt = tag.next_sibling
                if nxt == '\n':
                    nxt = nxt.next_sibling
                data = nxt.text.replace('\r\n', '\n')
                input_data.append(data)
        return input_data

    # this doesn't work for live contests since the problems are not published
    # when the contest starts (only when the contest is over?)
    # @classmethod
    # def download_contest(cls, contest_id) -> bool:
    #     res = requests.get(contest_url(contest_id))
    #     if not (200 <= res.status_code < 300):
    #         return False
    #     html = res.text
    #     soup = BeautifulSoup(html, 'html.parser')
    #     tags = soup.select('span.lang-en > div.row tbody > tr > td')
    #     problems = list(filter(lambda s: len(s) == 1, [tag.text.strip().lower() for tag in tags]))
    #     cls.make_contest_files(f'{contest_id}_', problem_id_suffixes=problems)
