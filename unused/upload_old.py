import base64
import os
import shutil
import sys
import requests

import dotenv
dotenv.load_dotenv()

BASE_URL = 'https://api.github.com'
GITHUB_USERNAME: str = os.getenv('GITHUB_USERNAME')
GITHUB_TOKEN: str = os.getenv('GITHUB_TOKEN')


def github_api_url(path: str) -> str:
    return f'{BASE_URL}{path}'


session = requests.Session()
session.auth = (GITHUB_USERNAME, GITHUB_TOKEN)


OWNER = 'AndrewDongAndy'


def str_to_base64_str(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


def upload_solution(local_folder, local_file, github_repo, github_filepath, delete_local=True):
    local_filepath = f'{local_folder}/{local_file}'
    url = github_api_url(
        f'/repos/{OWNER}/{github_repo}/contents/{github_filepath}')

    res = session.get(url)

    if res.status_code == 200:
        sha = res.json()['sha']
        commit_message = f'Update existing solution for problem {local_file} from Python script'
    else:
        sha = None
        commit_message = f'Upload new solution for problem {local_file} from Python script'

    try:
        with open(local_filepath) as f:
            content = f.read()
    except FileNotFoundError:
        return False

    data = dict(
        message=commit_message,
        content=str_to_base64_str(content),
        sha=sha,
    )

    res = session.put(url, json=data)

    # print(f'{res.status_code=}, {res.reason=}')
    # data = res.json()
    # print(data)
    # message = data['message']
    # print(message)

    if 200 <= res.status_code < 300:
        print(
            f'successfully pushed {local_filepath} to GitHub repo {github_repo}, path {github_filepath}')
        print(f'message: {commit_message}')
        if delete_local:
            shutil.rmtree(local_folder)
            print(f'deleted directory {local_folder} locally')
        return True
    print(f'local file {local_filepath} not uploaded')
    return False


def upload_atcoder_solution(id: str) -> bool:
    return upload_solution(
        id,
        f'{id}.cpp',
        'misc-cp',
        f'atcoder/{id}.cpp'
    )


def upload_boj_solution(id: str) -> bool:
    return upload_solution(
        f'boj_{id}',
        f'boj_{id}.cpp',
        'misc-cp',
        f'boj/boj_{id}.cpp',
    )


def upload_cf_solution(id: str) -> bool:
    return upload_solution(
        id,
        f'{id}.cpp',
        'codeforces',
        f'{id}.cpp',
    )


def upload_cf_solution_gym(id: str) -> bool:
    return upload_solution(
        f'gym_{id}',
        f'gym_{id}.cpp',
        'codeforces',
        f'gym_{id}.cpp'
    )


def upload_dmoj_solution(id: str, directory: str=None) -> bool:
    if directory is None:
        directory = 'dmoj-solutions'
    return upload_solution(
        id,
        f'{id}.cpp',
        directory,
        f'{id}.cpp',
    )


# AtCoder
# contest_id = 'abc211'
# num_problems = 6
# problem_suffixes = [chr(ord('a') + i) for i in range(num_problems)]
# problem_suffixes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
# for suffix in problem_suffixes:
#     id = f'{contest_id}_{suffix}'
#     upload_atcoder_solution(id)

# Baekjoon Online Judge
# upload_boj_solution('20051')
# boj_ids = []
# boj_ids = sys.argv[1:]
# for id in boj_ids:
#     upload_boj_solution(id)

# Codeforces
# upload_cf_solution('1394C')
# contest_id = '1552'
# problem_suffixes = ['A', 'B', 'C', 'D', 'E', 'F', 'H']
# for suffix in problem_suffixes:
#     id = f'{contest_id}{suffix}'
#     upload_cf_solution(id)

# Codeforces Gym
# gym_id = '100015'
# problem_suffixes = ['C', 'D', 'F']
# for suffix in problem_suffixes:
#     id = f'{gym_id}{suffix}'
#     upload_cf_solution_gym(id)

# DMOJ
# contest_id = 'cpc21c1p'
# problem_suffixes = ['1', '2', '4']
# for suffix in range(6):
#     id = f'{contest_id}{suffix}'
#     upload_dmoj_solution(id)
