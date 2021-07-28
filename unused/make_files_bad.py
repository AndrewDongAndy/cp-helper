"""
A script for making the program directories and files for a
variety of different contests.
"""


from cp_helper.judges.judge import Judge
from cp_helper.judges.atcoder import AtCoder
from cp_helper.judges.boj import Boj
from cp_helper.judges.codeforces import Codeforces
from cp_helper.judges.dmoj import Dmoj


def prompt_choices(prompt: str, choices: list[str], trailing_space=True) -> int:
    if trailing_space:
        prompt += ' '
    while True:
        for i, choice in enumerate(choices, start=1):
            print(f'{i} - {choice}')
        try:
            r = int(input(prompt))
        except ValueError:
            print('Invalid argument.')
            continue
        if r < 1 or r > len(choices):
            print('Invalid choice.')
            continue
        return r - 1


def prompt_string(prompt: str, trailing_space=True) -> str:
    if trailing_space:
        prompt += ' '
    return input(prompt)


judges = [AtCoder, Boj, Codeforces, Dmoj, Judge]
judge_id = prompt_choices(
    'Enter contest judge.',
    [judge.name for judge in judges]
)
JudgeClass = judges[judge_id]
print()

types = ['single problem', 'for contest']
type_id = prompt_choices(
    'Single problem or for a contest?',
    types
)
print()

if type_id == 0:
    if not JudgeClass.name.startswith('generic'):
        prompt = f'Enter the {JudgeClass.name} problem ID.'
    else:
        prompt = 'Enter the file name.'
    problem_id = prompt_string(prompt)
    suffix = prompt_string('Enter the filename suffix (blank for no suffix).')
    if suffix == '':
        suffix = None
    JudgeClass.write_template(problem_id, suffix=suffix)
else:
    contest_prefix = prompt_string('Enter the contest prefix.')
    r = prompt_string('Enter either:\n'
                      '- the number of files to create; or,\n'
                      '- the problem ID suffixes, separated by spaces.\n', False)
    ids = r.split(' ')
    if len(ids) == 1:
        num_problems = int(ids[0])
        assert num_problems <= 15
        JudgeClass.make_contest_files(contest_prefix, num_problems=num_problems)
    else:
        JudgeClass.make_contest_files(contest_prefix, problem_id_suffixes=ids)

    # BOJ
    # start = 7993
    # end = 7996
    # ids = list(range(start, end + 1))
    # for i in ids:
    #     Boj.write_template(f'{i}')

    # Codeforces
    # Codeforces.write_template_gym('100015', 'D')

    # Google Code Jam
    # GoogleCodeJam.write_template('D')
    # GoogleCodeJam.make_contest_files(num_problems=4)
    # GoogleCodeJam.make_contest_files(
    #     prefix='',
    #     problem_id_suffixes=['A', 'B', 'C', 'D'],
    # )

    # Google Kick Start
    # GoogleKickStart.make_contest_files('kickstart_', num_problems=4)

    # Kattis
    # Kattis.write_template('busyboard')
    # Kattis.make_contest_files('', 10)

    # USACO
    # LINKS = [
    #     'http://www.usaco.org/index.php?page=viewproblem&cpid=1104',
    #     'http://www.usaco.org/index.php?page=viewproblem&cpid=1105',
    #     'http://www.usaco.org/index.php?page=viewproblem&cpid=1106',
    # ]
    # Usaco.make_contest_files('usaco', num_problems=3, links=LINKS)

    # Miscellaneous
    # Platform.write_template('H')
    # count = 5
    # ids = [chr(ord('A') + i) for i in range(count)]
    # for id in ids:
    #     Platform.write_template(id)
