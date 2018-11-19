# -*- coding: utf-8 -*-

"""Utilities for interacting with the HBP repository on GitLab."""

import logging
from io import StringIO
from typing import Iterable, Optional, Set

import click
from easy_config import EasyConfig
from git import GitCommandError, Repo
from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectManager

from pybel import Manager
from pybel.struct import get_unused_annotations, get_unused_namespaces
from .git import get_bel

logger = logging.getLogger(__name__)

FAILING = 'Failing'
PASSING = 'Passing'
WARNING = 'Warning'


class GitlabConfig(EasyConfig):
    """Configuration for GitLab."""

    NAME = 'gitlab'
    FILES = []

    project_id: int
    url: str
    token: str

    def get_gitlab(self) -> Gitlab:
        """Get a Gitlab instance using this configuration."""
        return Gitlab(self.url, private_token=self.token)

    def get_project(self) -> Project:
        """Get a project instance using this configuration."""
        gl = self.get_gitlab()
        projects: ProjectManager = gl.projects
        project: Project = projects.get(self.project_id)
        return project


def gitlab_feedback(  # noqa: C901
        project: Project,
        repo: Repo,
        manager: Manager,
        skip: Optional[Set[str]] = None,
        automerge: bool = False
):
    """Get feedback for all branches in the project.

    Warning: modifies the git repository in place.

    :param project:
    :param repo:
    :param manager:
    :param skip:
    :param automerge:
    :return:
    """
    for mr in project.mergerequests.list():
        bname = f'origin/{mr.source_branch}'

        if skip and mr.title in skip:
            click.secho(f'Skipping {bname}: {mr.title}', fg='yellow')
            continue

        if mr.title.startswith('WIP:'):
            click.secho(f'WIP      {bname}: {mr.title}', fg='yellow')
            continue  # skipping work in progress

        if FAILING in mr.labels:
            click.secho(f'skipping {bname}: {mr.title}', fg='red')
            continue  # still needs to be addressed

        if PASSING in mr.labels:
            click.secho(f'skipping {bname}: {mr.title}', fg='green')
            continue

        if WARNING in mr.labels:
            click.secho(f'skipping {bname}: {mr.title}', fg='yellow')
            continue

        click.secho(f'{bname}: {mr.title}', fg='cyan')
        try:
            bel_graph = get_bel(repo, bname, manager=manager)
        except GitCommandError:
            logger.exception(f'GitCommandError: Skipping {bname}')
        except Exception as e:
            click.echo(str(e))

            mr_note = mr.notes.create({'body': f'## Failure\n{e}'})
            mr_note.save()

            mr.labels.append(FAILING)
            mr.save()
        else:
            unused_namespaces = get_unused_namespaces(bel_graph)
            unused_annotations = get_unused_annotations(bel_graph)

            if not bel_graph.warnings:
                click.secho(f'Passed {bname}: {mr.title}\n', fg='green')
                mr.labels.append(PASSING)
                mr.save()

                if unused_annotations:
                    comment_unused(mr, unused_annotations, 'Annotations')

                if unused_namespaces:
                    comment_unused(mr, unused_namespaces, 'Namespaces')

                if automerge:
                    mr.merge()

                continue

            else:
                body = StringIO()
                if bel_graph.warnings:
                    print('## Warnings\n', file=body)
                    print('```', file=body)
                    print(get_warnings_for_pager(bel_graph.warnings), file=body)
                    print('```', file=body)
                if unused_namespaces:
                    print('## Unused Namespaces\n', file=body)
                    print('```', file=body)
                    for namespace in sorted(unused_namespaces):
                        print(namespace, file=body)
                    print('```', file=body)
                if unused_annotations:
                    print('## Unused Annotations\n', file=body)
                    print('```', file=body)
                    for annotation in sorted(unused_annotations):
                        print(annotation, file=body)
                    print('```', file=body)

                body_val = body.getvalue()

                mr_note = mr.notes.create({'body': f'# Issues\n{body_val}'})
                mr_note.save()

                mr.labels.append(WARNING)
                mr.save()

        click.echo('')


def comment_unused(mr, unused_terminologies: Iterable[str], title: str):
    """Add a comment to a given merge request based on the unused terminologies given."""
    sio = StringIO()
    print(f'## Unused {title}\n', file=sio)
    print('```', file=sio)
    for namespace in sorted(unused_terminologies):
        print(namespace, file=sio)
    print('```', file=sio)

    mr.labels.append(title)
    mr.save()

    mr_note = mr.notes.create({'body': sio.getvalue()})
    mr_note.save()


def get_warnings_for_pager(warnings, sep='\t'):
    """Output the warnings from a BEL graph.

    :param warnings: A list of 4-tuples representing the warnings
    :param str sep: The separator. Defaults to tab.
    :rtype: str
    """
    max_line_width = max(
        len(str(line_number))
        for line_number, _, _, _ in warnings
    )

    max_warning_width = max(
        len(exc.__class__.__name__)
        for _, _, exc, _ in warnings
    )

    s1 = '{:>' + str(max_line_width) + '}' + sep
    s2 = '{:>' + str(max_warning_width) + '}' + sep

    def _make_line(line_number, line, exc):
        s = s1.format(line_number)
        s += s2.format(exc.__class__.__name__)
        s += line + sep
        s += str(exc)
        return s

    return '\n'.join(
        _make_line(line_number, line, exc)
        for line_number, line, exc, _ in warnings
    )
