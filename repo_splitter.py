import os
import sys
import shutil
from pprint import pprint


def calculate_maps():
    return get_maps(list_files('/Users/djfarquharson/repos/maps'))


def explicit_dependencies(files):
    return [gather_dependencies(f) for f in files]


def gather_dependencies(f):
    print 'parsing file: '+f
    return {'file': f,
            'deps': get_source_files(f).split(',') if is_output(f) else [],
            'repo_name': get_repo_name(f)}


def list_files(cwd):
    return [str(fmt_dir(parent)+f)
            for (parent, dirs, files) in os.walk(cwd)
            for f in files if f.endswith('.xtl')]


def fmt_dir(path):
    return path if path.endswith('/') else path+'/'


def get_maps(files):
    return [get_metadata(x) for x in files if is_output(x)]


def get_metadata(x):
    print 'parsing file: ' + x
    sources = get_source_files(x)
    repo_name = get_repo_name(x)
    return {'xtls': sources.split(',') + [x],
            'repo_name': repo_name}


def get_source_files(x):
    return '/'.join(x.split('/')[:-1]+[get_attr(x, 'sourceFiles')])


def get_repo_name(x):
    return get_attr(x, 'fullyQualifiedJavaName') \
        if has_attr(x, 'fullyQualifiedJavaName') \
        else get_attr(x, 'javaPackageName') + '.' + \
        get_attr(x, 'javaName') \
        if has_attr(x, 'javaPackageName') and has_attr(x, 'javaName') \
        else '.'.join('_'.join(x.split()).split('/')[1:])


def has_attr(x, attr):
    with open(x, 'r') as obj:
        data = obj.read()
    return attr in data


def get_attr(x, attr):
    with open(x, 'r') as obj:
        data = obj.read()
    iattr = data.index(attr)
    iequal = data.index('=', iattr)
    quote = data[iequal+1]
    iattrend = data.index(quote, iequal+2)
    return data[iequal+2:iattrend]


def is_output(x):
    return has_attr(x, 'sourceFiles') and len(get_attr(x, 'sourceFiles')) > 0 \
        and (has_attr(x, 'javaPackageName') or
             has_attr(x, 'fullyQualifiedJavaName'))


def merge_shared_repos(repos):
    repos_trimmed = []
    for repo in repos:
        merged = False
        for xtl in repo['xtls']:
            if get_sibling_repo(xtl, repos) is not None:
                result = merge(get_sibling_repo(xtl, repos), repo)
                print result
                repos_trimmed.append(result)
                merged = True
                break
    return repos_trimmed


def merge(x, y):
    x['xtls'] = list(set(x['xtls'] + y['xtls']))
    return x


def get_sibling_repo(xtl, repos):
    for repo in repos:
        if '../' not in xtl and xtl in repo['xtls']:
            return repo


def create_repos(data):
    for d in data:
        repo = '/Users/djfarquharson/test/unique_repos/'+d['repo_name']
        print 'setting up repo: '+repo
        if not os.path.isdir(repo):
            os.mkdir(repo)
        cwd = os.getcwd()
        os.chdir(repo)
        os.system('git init')
        for xtl in d['xtls']:
            if os.path.exists(xtl):
                os.chdir('/'.join(xtl.split('/')[:-1]))
                # exports git log of a file as a 'patch' which we apply to the new repo
                os.system('git log --pretty=email --patch-with-stat --reverse ' +
                          '-- '+xtl.split('/')[-1]+' | (cd '+repo+' && git am)')
                os.chdir(repo)
                # rewrites history with file at the top level instead of deeply nested
                inner_xtl = '/'.join(xtl.split('/')[6:])
                os.system('git filter-branch -f --tree-filter \'if [ -f '+ inner_xtl +
                          ' ]; then mv '+inner_xtl+' .; fi\' HEAD')
        os.chdir(cwd)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        maps = get_maps(list_files(sys.argv[1]))
        #merged = merge_shared_repos(maps)
        #create_repos(merged)
    else:
        print('usage: python repo_splitter dir')
