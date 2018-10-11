# -*- coding: utf-8 -*-


from typing import List

from git import Repo


def get_changed(repo: Repo) -> List[str]:
    """Get a list of files that have changed in the last commit."""
    head_commit = repo.git.rev_parse('HEAD')
    output = repo.git.diff_tree('--no-commit-id', '--name-only', '-r', head_commit)

    return [
        name
        for name in output.split('\n')
        if name.endswith('.bel')
    ]
