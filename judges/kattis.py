from .judge import Judge


class Kattis(Judge):
    name = 'Kattis'
    github_repo = 'cp-solutions'
    github_directory = 'kattis'

    @staticmethod
    def link(problem_id):
        return f'https://open.kattis.com/problems/{problem_id}'

    @staticmethod
    def get_suffix_for_contest(index) -> str:
        return chr(ord('A') + index)
