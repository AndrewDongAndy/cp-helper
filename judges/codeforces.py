from .judge import Judge, scrape_html

from bs4 import BeautifulSoup
import requests


def contest_url(contest_id: str) -> str:
    return f'https://codeforces.com/contest/{contest_id}'


class Codeforces(Judge):
    name = 'Codeforces'
    github_repo = 'cp-solutions'
    github_directory = 'codeforces'

    @staticmethod
    def link(problem_id: str):
        # check if gym
        gym = False
        if problem_id.startswith('gym_'):
            gym = True
            problem_id = problem_id[4:]

        for i, char in enumerate(problem_id):
            if char.isalpha():
                break
        contest_id = problem_id[:i]  # the number
        problem = problem_id[i:]  # the index of the problem, e.g. A, B, B1, C2
        # print(f'determined contest id: {contest_id}; problem id: {problem}')

        if gym:
            return f'https://codeforces.com/gym/{contest_id}/problem/{problem}'
        return f'https://codeforces.com/contest/{contest_id}/problem/{problem}'

    @classmethod
    def write_template_gym(cls, gym_id, problem: str):
        cls.write_template(
            f'gym_{gym_id}{problem}',
            link=f'https://codeforces.com/gym/{gym_id}/problem/{problem}',
        )

    @classmethod
    def get_input_data(cls, html: str) -> list[str]:
        soup = BeautifulSoup(html, 'html.parser')
        pre_tags = soup.select('div.input > div.title + pre')
        input_data = [tag.text.lstrip() for tag in pre_tags]
        return input_data

    @classmethod
    def download_contest(cls, contest_id) -> bool:
        res = scrape_html(contest_url(contest_id))
        if not (200 <= res.status_code < 300):
            return False
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        anchor_tags = soup.select('tr > td.id > a')
        problems = [tag.text.strip() for tag in anchor_tags]
        cls.make_contest_files(contest_id, problem_id_suffixes=problems)
