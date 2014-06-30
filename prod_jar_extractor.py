import os
from subprocess import check_output as _sh
from git import execute as _git


def fmtrepo(x):
    return x.replace('_', '.').replace('.jar', '')


def calculate_fi_jars(d='/opt/git/tmp/fi_jars/'):
    jarlist = [x for x in os.listdir(d) if x.endswith('.jar')]
    return [(d+x, fmtrepo(x)) for x in jarlist]


def match_jars_to_repos(d='/opt/git/tmp/new_repos/', jars=calculate_fi_jars()):
    repo_list = os.listdir(d)
    return [(d+x, jar) for x in repo_list
            for jar in jars
            if x == jar[1]]


def calculate_web_jars(d='/opt/git/tmp/web_jars/'):
    pass
    #return [(x, fmtrepo(x)) for x in os.listdir(d)]


def view_xtls_in_jar(jar):
    try:
        return [x for x in _sh('jar tf '+jar+' | grep .xtl', shell=True).split('\n')
                if len(x) > 0]
    except:
        return []


def apply_prod_xtls(jar, xtls, repo):
    if len(xtls) > 0:
        cwd = os.getcwd()
        os.chdir(repo)
        _git(['checkout', '-b', 'SVN'])
        _git(['checkout', 'master'])
        os.chdir(cwd)
        _sh('jar xf '+jar+' '+' '.join(xtls), shell=True)
        print 'dos2unix '+' '.join(xtls)
        _sh('dos2unix '+' '.join(xtls), shell=True)
        _sh('mv '+' '.join(xtls)+' '+repo, shell=True)
        os.chdir(repo)
        _git(['add']+xtls)
        _git(['commit', '-m', '"updated master with prod xtls: '+' '.join(xtls)+'"'])
        if 'SVN' in _git(['branch', '--contains', 'master'])[0]:
            _git(['branch', '-d', 'SVN'])
        os.chdir(cwd)


def update_repos(repos):
    for repo in repos:
        jar = repo[1][0]
        apply_prod_xtls(jar, view_xtls_in_jar(jar), repo[0])


#def update_repos():
# if repo.endswith('.web') look in web_jars
# else look in fi_jars
# jar tf jar-file (view the contents)
# jar xf jar-file f1.xtl f2.xtl (extract just f1.xtl and f2.xtl)
    #pass
