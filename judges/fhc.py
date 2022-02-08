from .judge import Judge


ROUND_PAIRS = [
    ('qual', 'qualification-round'),
    ('round1', 'round-1'),
    ('round2', 'round-2'),
    ('round3', 'round-3'),
    ('finals', 'final-round')
]


def get_round_for_link(r: str) -> str:
    for short, long in ROUND_PAIRS:
        if r == short:
            return long
    assert False


def get_github_path(link: str):
    parts = link.split('/')
    year, round, problems, problem = parts[-4:]
    assert problems == 'problems' # kind of make sure link format didn't change
    for short, long in ROUND_PAIRS:
        if round == long:
            round = short
            break
    else:
        assert False
    return f'{year}/{round}/{problem}.cpp'


class Fhc(Judge):
    name = 'Facebook Hacker Cup'
    github_repo = 'cp-solutions'
    github_directory = 'fhc'

    @staticmethod
    def link(problem_id: str) -> str:
        # use format '<year>_<round>_<problem>'
        # e.g. 2021_round2_a
        # <round> is one of: qual | round1 | round2 | round3 | finals
        year, round, problem = problem_id.split('_')
        round = get_round_for_link(round)
        problem = problem.upper()

        return f'https://www.facebook.com/codingcompetitions/hacker-cup/{year}/{round}/problems/{problem}'

    @staticmethod
    def local_directory_and_filename_no_ext(problem_id, suffix=None):
        year, round, problem = problem_id.split('_')
        year, round, problem = problem_id.split('_')
        round = get_round_for_link(round)
        problem = problem.upper()
        
        directory = problem
        filename = f'{problem}'
        return (directory, filename)

    @classmethod
    def get_input_data(cls, html: str) -> list[str]:
        # print(html)
        return []
        # TODO: find a way to do this?

    @classmethod
    def upload_solution(cls, file: str, delete_local=True) -> bool:
        with open(file) as f:
            for line in f.readlines():
                if line.startswith(' * problem: '):
                    problem_url = line[3:].split()[1].strip()
                    break
        return super().upload_solution(
            file,
            github_path=get_github_path(problem_url),
            delete_local=delete_local,
        )
