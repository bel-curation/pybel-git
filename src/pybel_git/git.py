# -*- coding: utf-8 -*-

"""Git utilities."""

from typing import Iterable, List, Optional

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
    """Get the BEL graph for the first BEL document found."""
    line_groups = list(get_bel_lines(repo, branch))
    lines = line_groups[0]
    return from_lines(lines, manager=manager, use_tqdm=use_tqdm)


def get_bel_lines(repo: Repo, branch: str) -> Iterable[List[str]]:
    """Yield the list of lines from each BEL file in the given branch."""
    for file_name in get_changed_from_master(repo, branch):
        if file_name.endswith('.bel'):
            yield _get_bel_lines(repo, branch, file_name)


def get_changed_from_master(repo: Repo, other_branch_name: str, master_branch_name: str = 'origin/master') -> List[str]:
    """List all files differing between the master and given branch."""
    commit_something = repo.git.merge_base(other_branch_name, master_branch_name)
    return repo.git.diff('--name-only', other_branch_name, commit_something).split('\n')


def _get_bel_lines(repo: Repo, branch: str, file_name: str) -> List[str]:
    print(f'working on {file_name}')
    repo.git.checkout(branch)
    file_blob = repo.head.commit.tree / file_name
    contents = file_blob.data_stream.read().decode('utf8')
    lines = contents.split('\n')
    return lines
