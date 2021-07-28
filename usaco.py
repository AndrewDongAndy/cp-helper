from .judge import Judge


class Usaco(Judge):
    @staticmethod
    def get_contest_suffix(index):
        return f'{index + 1}'
