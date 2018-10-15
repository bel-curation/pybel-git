pybel-git
=========
Git and continuous integration tools for PyBEL.

Using Travis-CI
---------------
To configure Travis-CI to evaluate the changed BEL files in a GitHub
repository on each commit, the following travis.yml file can be used:

.. code-block:: yaml

	sudo: false
	cache: pip
	language: python
	python:
	- 3.6
	install:
	- pip install git+https://github.com/cthoyt/pybel-git
	script:
	- pybel-git ci

Currently, the build doesn't use a cached resource file, so this job
might take a long time. The `travis_wait <https://docs.travis-ci.
com/user/common-build-problems/#build-times-out-because-no-output-
was-received>`_ command can be used so the script reads
``travis_wait 30 pybel-git ci`` and the job will be allowed to run for
thirty (30) minutes.

An example can be found at https://github.com/cthoyt/pybel-git-test.

Interfacing with GitLab
-----------------------
PyBEL-Git contains extra scripts to assist in automatic checking and feedback
for projects residing in GitLab that are using the Git Flow workflow of branching
and making merge requests.

This script checks each branch, compiles the BEL documents that have changed
compared to master, and puts comments on the merge request with the warnings
and feedback on the syntactic and semantic correctness of the BEL files.

It can be run with:

.. code-block:: bash

	pybel-git ci_gitlab \
	    --url "https://gitlab.scai.fraunhofer.de"  # the url of the desired gitlab instance \
	    --project-id 449  # the gitlab project id, shown at the top of the page for the repository \

This script uses `EasyConfig <https://github.com/scolby33/easy_config>`_ and can also be configured
via the environment variables ``GITLAB_URL``, ``GITLAB_PROJECT_ID``, and ``GITLAB_TOKEN``.

TO-DO: using continuous integration with GitLab, especially in private settings (such as Jenkins)
