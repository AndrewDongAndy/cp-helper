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
        if '_' in problem_id:
            subdomain, problem_code = problem_id.split('_')
        else:
            subdomain = 'open'
            problem_code = problem_id
        return f'https://{subdomain}.kattis.com/problems/{problem_code}'
        # return 'kattis source is too annoying to track'

    @staticmethod
    def get_suffix_for_contest(index) -> str:
        return chr(ord('A') + index)

    @classmethod
    def get_input_data(cls, html: str) -> list[str]:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.select('table.sample')
        input_data: list[str] = []
        for table in tags:
            assert table['summary'] == 'sample data'
            pre_tags = table.select('tr > td > pre')
            assert len(pre_tags) == 2
            data = pre_tags[0].text
            input_data.append(data)
        return input_data

    @classmethod
    def download_contest(cls, contest_id: str) -> bool:
        res = requests.get(contest_url(contest_id))
        if not (200 <= res.status_code < 300):
            return False
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select('table#contest_problem_list > tbody > tr')
        letters = []
        link_suffixes = []
        for row in rows:
            letter = row.select_one('th.problem_letter').text.strip()
            anchor = row.find('a', href=True)
            link = anchor['href']
            letters.append(letter)
            link_suffixes.append(link.split('/')[-1])
        # print(letters, links)
        # print(problems)
        links = [
            f'https://{contest_id}.kattis.com/problems/{suffix}'
            for suffix in link_suffixes
        ]
        cls.make_contest_files(
            # prefix=f'{contest_id}_',
            problem_id_suffixes=letters,
            links=links,
        )
