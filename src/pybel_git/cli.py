# -*- coding: utf-8 -*-

"""Command line interface for PyBEL-Git."""

import os
import sys

import click
from git import Repo

from pybel import Manager, from_path
from pybel.cli import connection_option
from pybel_git.git import get_changed

EMOJI = '🔔'


@click.group()
def main():
    """Git utilities for PyBEL."""


# TODO download pre-built cache?

@main.command()
@click.option('-d', '--directory', default=os.getcwd(), type=click.Path(file_okay=False, dir_okay=True),
              help='Directory of git repository')
@connection_option
def ci(directory: str, connection: str):
    """Run in continuous integration setting."""
    repo = Repo(directory)

    file_names = get_changed(repo)
    if not file_names:
        click.secho(f'{EMOJI} no BEL files changed')
        sys.exit(0)

    manager = Manager(connection=connection)

    failures = []
    for file_name in file_names:
        click.echo(f'{EMOJI} file changed: {file_name}')
        graph = from_path(file_name, manager=manager)
        if graph.warnings:
            failures.append((file_name, graph))
        click.echo(f'{EMOJI} done checking: {file_name}')
    if not failures:
        sys.exit(0)

    click.echo('')
    for file_name, graph in failures:
        click.secho(f'failed: {file_name} - {graph}', fg='red')
    sys.exit(1)


@main.command()
@click.option('-d', '--directory', default=os.getcwd(), type=click.Path(file_okay=False, dir_okay=True),
              help='Directory of git repository')
@connection_option
@click.option('--project-id', type=int)
@click.option('--url')
@click.option('--token')
def ci_gitlab(directory: str, connection: str, project_id: int, url: str, token: str):
    """Run in a continuous integration setting with communication to GitLab."""
    from pybel_git.gitlab import GitlabConfig, gitlab_feedback

    gitlab_config = GitlabConfig.load(
        project_id=project_id,
        url=url,
        token=token,
    )
    project = gitlab_config.get_project()
    repo = Repo(directory)
    manager = Manager(connection=connection)

    gitlab_feedback(
        project=project,
        repo=repo,
        manager=manager,
    )
