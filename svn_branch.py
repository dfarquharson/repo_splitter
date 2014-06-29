import os
from git import execute as _git


def make_svn_branch(dirs):
    for repo in [x for x in dirs]:
        os.chdir(repo)
        _git(['checkout', 'master'])
        _git(['checkout', '-b', 'SVN'])
        _git(['checkout', 'master'])
