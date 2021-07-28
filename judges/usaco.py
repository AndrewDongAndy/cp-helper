from .judge import Judge


class Usaco(Judge):
    name = 'USACO'
    github_repo = 'cp-solutions'
    github_directory = 'usaco'

    @staticmethod
    def get_contest_suffix(index):
        return f'{index + 1}'
