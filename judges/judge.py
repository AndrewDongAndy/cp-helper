"""
The base class.


TODO: "sanitize" problem IDs, e.g.:

AtCoder problem IDs are always lowercase
Boj problem IDs are always numbers with at least 4 digits
Codeforces problem IDs are always uppercase
DMOJ and Kattis problem IDs are always (?) lowercase
"""


import base64
from datetime import datetime
from importlib import resources
import os
from typing import Optional
import requests

from send2trash import send2trash

from .. import templates

import dotenv
dotenv.load_dotenv()

GITHUB_USERNAME: str = os.getenv('GITHUB_USERNAME')
GITHUB_TOKEN: str = os.getenv('GITHUB_TOKEN')

session = requests.Session()
session.auth = (GITHUB_USERNAME, GITHUB_TOKEN)

web_page_session = requests.Session()
web_page_session.headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}


def github_api_url(path: str) -> str:
    return f'https://api.github.com{path}'


def str_to_base64_str(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


def scrape_html(url: str) -> Optional[str]:
    res = web_page_session.get(url)
    if 200 <= res.status_code < 300:
        return res.text
    print(
        f'request to get input data from {url} failed with code {res.status_code}')
    print(f'reason: {res.reason}')


SOURCE_EXTENSIONS = [
    '.cpp',
    '.py',
    '.clean_cpp',  # clean C++; no debug.h include
]

# TODO: clean_cpp doesn't actually work right now

TEMPLATES = dict()
for ext in SOURCE_EXTENSIONS:
    TEMPLATES[ext] = resources.read_text(templates, f'template{ext}')

# the default template to use is f'template.{DEFAULT_LANGUAGE}'
DEFAULT_LANGUAGE = 'cpp'


class Judge:
    """Default values for a Judge. This class should be extended."""
    name = 'generic judge'
    github_repo = 'cp-solutions'
    github_directory = 'misc'

    @staticmethod
    # TODO: in Python 3.10, type this as str | None
    def link(problem_id: str) -> str:
        return 'no source provided'

    @staticmethod
    def local_directory_and_filename_no_ext(problem_id, suffix=None):
        directory = problem_id

        filename = problem_id
        if suffix is not None:
            filename += '_' + suffix

        return (directory, filename)

    @classmethod
    def write_template(cls, problem_id, suffix=None, link=None, lang=None) -> None:
        if lang is None:
            lang = DEFAULT_LANGUAGE
        ext = f'.{lang}'

        directory, filename = cls.local_directory_and_filename_no_ext(
            problem_id, suffix=suffix)
        filename += ext
        if link is None:
            link = cls.link(problem_id)

        if not os.path.isdir(directory):
            os.mkdir(directory)

        code_file = os.path.join(directory, filename)

        # check for overwriting
        if os.path.isfile(code_file):
            while True:
                response = input(
                    f'File {code_file} already exists. Overwrite? ([y]/n) '
                ).lower().strip()
                if response == '':
                    response = 'y'
                if response in ['y', 'n']:
                    break
            if response == 'n':
                # don't overwrite; return
                print(f'File {code_file} not overwritten.')
                return

        if ext in TEMPLATES:
            template = TEMPLATES[ext]
        else:
            print(
                f'no template found for language "{lang}"; using empty template')
            template = ''

        # format template
        now = datetime.now().strftime('%x %X')
        template = template.replace('DATE', now)
        template = template.replace('FILENAME', filename)
        template = template.replace('PROBLEM_LINK', link)

        # write to files
        with open(code_file, 'w') as out:
            out.write(template)

        # use vscode workspace setup instead
        # build_command = BUILD_COMMAND.replace('FILENAME', filename)
        # build_file = os.path.join(directory, 'b.bat')
        # with open(build_file, 'w') as out:
        #     out.write(build_command)

        input_file = os.path.join(directory, 'in1')
        # only write input_file if doesn't exist
        if not os.path.isfile(input_file):
            with open(input_file, 'w') as out:
                pass  # don't write anything; just make the file

        # pull input data from the problem link
        try:
            html = scrape_html(link)
            if html is not None:
                input_data = cls.get_input_data(html)
            else:
                input_data = []
        except requests.exceptions.MissingSchema:
            input_data = []
        # write input data
        for i, data in enumerate(input_data, start=1):
            in_file = os.path.join(directory, f'in{i}')
            with open(in_file, 'w') as f:
                f.write(data)

        confirmation = 'template '
        if cls.name is not None:
            confirmation += f'for {cls.name} problem '
        confirmation += f'written to {code_file}'
        confirmation += f'; {len(input_data)} input files downloaded'
        print(confirmation)

    @staticmethod
    def get_contest_suffix(index) -> str:
        return chr(ord('A') + index)  # default is A, B, ...

    @classmethod
    def make_contest_files(cls, prefix='', num_problems=None,
                           problem_id_suffixes=None, links=None) -> None:
        if problem_id_suffixes is None:
            assert num_problems is not None and num_problems >= 1
            problem_id_suffixes = [
                cls.get_contest_suffix(i)
                for i in range(num_problems)
            ]

        if links is None:
            links = [None for _ in problem_id_suffixes]
        else:
            assert len(links) == len(problem_id_suffixes)
        for suffix, link in zip(problem_id_suffixes, links):
            problem_id = f'{prefix}{suffix}'
            cls.write_template(problem_id, link=link)

    @classmethod
    def get_input_data(cls, html: str) -> list[str]:
        return []

    @classmethod
    def upload_solution(cls, file: str, github_path=None, delete_local=True) -> bool:
        # file - full path of the file to remove
        try:
            with open(file) as f:
                solution = f.read()
        except FileNotFoundError:
            print(f'ERROR: file {file} not found')
            return False

        head, tail = os.path.split(file)
        if github_path is None:
            github_path = tail

        assert cls.github_directory != ''
        github_filepath = f'{cls.github_directory}/{github_path}'

        url = github_api_url(
            f'/repos/{GITHUB_USERNAME}/{cls.github_repo}/contents/{github_filepath}')

        # check if file already exists
        # if it does, need to get the sha
        res = session.get(url)
        if res.status_code == 200:
            sha = res.json()['sha']
            commit_message = f'Update existing solution {github_path} from Python script'
        else:
            sha = None
            commit_message = f'Upload new solution {github_path} from Python script'

        # upload the new data
        data = dict(
            message=commit_message,
            content=str_to_base64_str(solution),
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
                f'successfully pushed {tail} to GitHub repo {cls.github_repo}, path {github_filepath}')
            print(f'message: {commit_message}')
            if delete_local:
                source_files = sum(
                    int(os.path.splitext(s)[1] in SOURCE_EXTENSIONS)
                    for s in os.listdir(head)
                )
                if source_files == 1:
                    # no more source files;
                    # shutil.rmtree(head)
                    send2trash(head)
                    print(f'deleted locally: directory {head}')
                else:
                    assert source_files > 1
                    # delete the file
                    send2trash(file)
                    print(f'deleted locally: file {file}')
            return True

        print(f'local file {tail} not uploaded')
        return False
