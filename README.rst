PyBEL-Git |build| |zenodo|
==========================
Git and continuous integration tools for PyBEL to assist in curating BEL.

If you've found ``pybel-git`` useful in your work, please consider citing [1]_:

.. [1] Hoyt, C. T., *et al*. (2019). `Re-curation and rational enrichment of knowledge graphs in Biological Expression
       Language <https://doi.org/10.1093/database/baz068>`_. *Database*, 2019, baz068.

Usage with Continuous Integration
---------------------------------
Below are examples on using ``pybel-git`` within the configuration
of several continuous integration services. Additonaly, the ``-r``
option can be used to specify required annotations. For example,
``-r Confidence`` can be used during re-curation.

Using GitHub and Travis-CI
~~~~~~~~~~~~~~~~~~~~~~~~~~
To configure `Travis-CI <https://travis-ci.com>`_ to evaluate the 
BEL files that have changed in the latest commit to a in a GitHub 
repository on each commit, the following ``travis.yml`` file can 
be used:

.. code-block:: yaml

   sudo: false
   cache: pip
   language: python
   python:
     - '3.7'
   install:
     - pip install pybel-git
   script:
     - pybel-git ci

Currently, the build doesn't use a cached resource file, so this job
might take a long time. The `travis_wait <https://docs.travis-ci.
com/user/common-build-problems/#build-times-out-because-no-output-
was-received>`_ command can be used so the script reads
``travis_wait 30 pybel-git ci`` and the job will be allowed to run for
thirty (30) minutes.

An example repository can be found at https://github.com/cthoyt/pybel-git-test.
An example build for this repository can be found at https://travis-ci.com/cthoyt/pybel-git-test/builds/87612373.

Using GitLab with GitLab CI/CD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To configure `GitLab CI/CD <https://docs.gitlab.com/ee/ci>`_ to 
evaluate the BEL files that have changed in the latest commit to
a GitLab repository, the following ``.gitlab-ci.yml`` can be used:

.. code-block:: yaml

   test:
     image: python:3.7
     script:
       - pip install pybel-git
       - pybel-git ci

As with GitHub/Travis-CI, this configuration does not use a cached
resource file. GitLab CI/CD doesn't seem to offer a wait time, but
it might also not have an issue with timing out, either.

An example repository can be found at https://gitlab.com/cthoyt/pybel-gitlab-example.
An example build for this repository can be found at https://gitlab.com/cthoyt/pybel-gitlab-example/-/jobs/113454179

Using Atlassian BitBucket with Bitbucket Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To configure a BitBucket Pipelines to evaluate BEL files that have 
been changed in the latest commit to a BitBucket repository, the 
following ``bitbucket-pipelines.yml`` ca be used:

.. code-block:: yaml

   image: python:3.7

   pipelines:
     default:
       - step:
           caches:
             - pip
           script: 
             - pip install pybel-git
             - pybel-git ci

An example repository can be found at https://bitbucket.org/pybel/pybel-bitbucket-example.
An example build for this repository can be found at
https://bitbucket.org/pybel/pybel-bitbucket-example/addon/pipelines/home#!/results/2.

Usage with Git Service and Continuous Integration
-------------------------------------------------
Deeper Integration with GitLab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

.. |build| image:: https://travis-ci.com/pybel/pybel-git.svg?branch=master
    :target: https://travis-ci.com/pybel/pybel-git

.. |zenodo| image:: https://zenodo.org/badge/152552674.svg
   :target: https://zenodo.org/badge/latestdoi/152552674
