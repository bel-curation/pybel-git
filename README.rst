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
`travis_wait 30 pybel-git ci` and the job will be allowed to run for
thirty (30) minutes.
