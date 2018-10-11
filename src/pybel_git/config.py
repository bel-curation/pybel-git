# -*- coding: utf-8 -*-

"""Configuration for PyBEL-Git."""

import logging

from easy_config import EasyConfig

log = logging.getLogger(__name__)


class PyBELGitConfig(EasyConfig):
    """Configuration for PyBEL-Git."""
    NAME = 'pybel_git'
    FILES = []


pybel_git_config = PyBELGitConfig.load()
log.info('loaded pybel-git configuration: %s', pybel_git_config)
