Monorepo support built around ``git subtree``.

Installation
============

.. code:: sh

    pip install git_monorepo

Usage
=====

Simply create a mapping file called ``monorepo.yml`` in the root of your
git directory:

.. code:: yaml

    mappings:
      adhesive: git@github.com:germaniumhq/adhesive.git
      oaas:
        oaas: git@github.com:germaniumhq/oaas.git
        grpc-compiler: git@github.com:germaniumhq/oaas-grpc-compiler.git
        registry-api: git@github.com:germaniumhq/oaas-registry-api.git
        registry: git@github.com:germaniumhq/oaas-registry.git
        grpc: git@github.com:germaniumhq/oaas-grpc.git
        simple: git@github.com:germaniumhq/oaas-simple.git
      tools:
        git-monorepo: git@github.com:bmustiata/git-monorepo.git

Custom Branch
-------------

If you want to use a different branch name in all the remote
repositories instead of the same name as the local branch, specify it as
such:

.. code:: yaml

    mappings:
      # ...
    branch: master

    **Note**

    This branch name applies for both pulling *and* pushing.

Squash Commits
--------------

``subtree`` creates the commits, including merges into the upstream
repos. This could severely pollute the history of the upstream repos.
Because of this reason, squashing is implicitly enabled.

To disable squash the history into single commits, set the ``squash``
property:

.. code:: yaml

    mappings:
      # ...
    squash: false

pull
----

To pull the repos (including initial setup), use:

.. code:: sh

    git mono pull

In case upstream changes happened in the remote repos, so a pull is
required before the push, use the ``--no-sync`` flag, so it won’t
automatically merge and mark the changes as already synchronized to the
remote repo.

Implicity having a ``pull`` should be done on a clean repo, and a ``pull
--no-sync`` if upstream changes are present.

push
----

To push the repos do:

.. code:: sh

    git mono push

This takes into account the current branch name, so pushes can happen
also with branches.

At the end of the operation, if something was pushed, a new file to
track the status named ``.monorepo.sync`` is created and committed
automatically. This file holds a list of commits that were pushed, so
your merges can also be dealed with correctly, by adding both entries
when solving a potential conflict for a project.

mv
--

This renames the entry in the synchronized commits, and does the
equivalent of:

.. code:: sh

    git mv old/path new/path

With a special commit so ``git-subtree`` can find it.

    **Note**

    You still need to manually update the ``monorepo.yml`` manually with
    the new location.

    **Note**

    The feature is currently deemed unstable.
