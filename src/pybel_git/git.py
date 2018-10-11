# -*- coding: utf-8 -*-

"""Git utilities."""

from typing import List, Optional

from git import Repo

from pybel import BELGraph, Manager, from_lines


def get_changed(repo: Repo) -> List[str]:
    """Get a list of files that have changed in the last commit."""
    head_commit = repo.git.rev_parse('HEAD')
    output = repo.git.diff_tree('--no-commit-id', '--name-only', '-r', head_commit)

    return [
        name
        for name in output.split('\n')
        if name.endswith('.bel')
    ]


def get_bel(repo: Repo, branch: str, manager: Optional[Manager] = None, use_tqdm: bool = False) -> BELGraph:
    lines = get_bel_lines(repo, branch)
    return from_lines(lines, manager=manager, use_tqdm=use_tqdm)


def get_bel_lines(repo: Repo, branch: str) -> List[str]:
    for file_name in get_changed_from_master(repo, branch):
        if file_name.endswith('.bel'):
            return _get_bel_lines(repo, branch, file_name)


def get_changed_from_master(repo: Repo, other_branch_name: str) -> List[str]:
    commit_something = repo.git.merge_base(other_branch_name, 'origin/master')
    return repo.git.diff('--name-only', other_branch_name, commit_something).split('\n')


def _get_bel_lines(repo: Repo, branch: str, file_name: str) -> List[str]:
    print(f'working on {file_name}')
    repo.git.checkout(branch)
    file_blob = repo.head.commit.tree / file_name
    contents = file_blob.data_stream.read().decode('utf8')
    lines = contents.split('\n')
    return lines
