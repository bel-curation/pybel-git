# -*- coding: utf-8 -*-

"""Command line interface for PyBEL-Git."""

import os
import sys

import click
from git import Repo

from pybel import Manager, from_path
from pybel.cli import connection_option
from .commands import get_changed

EMOJI = '🔔'


@click.group()
def main():
    """PyBEL Git utilities."""


# TODO download pre-built cache?

@main.command()
@click.option('-d', '--directory', default=os.getcwd(), type=click.Path(file_okay=False, dir_okay=True),
              help='Directory of git repository')
@connection_option
def ci(directory: str, connection: str):
    """Run in continuous integration setting."""
    click.echo(f'{EMOJI} checking directory: {directory}')

    repo = Repo(directory)
    head_commit = repo.git.rev_parse('HEAD')
    click.echo(f'{EMOJI} head commit: {head_commit}')

    file_names = get_changed(repo)
    if not file_names:
        sys.exit(0)

    manager = Manager(connection=connection)
    failures = []
    for file_name in file_names:
        click.echo(f'{EMOJI} file changed: {file_name}')
        graph = from_path(file_name, manager=manager)
        if graph.warnings:
            failures.append(graph)

    sys.exit(1 if failures else 0)
