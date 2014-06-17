import os
import sys


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


def list_web_files(files):
    return [f for f in files if '/web/' in f]


def list_fi_files(files):
    return [f for f in files if not '/web/' in f]


def list_web_files_nested(files):
    return [f for f in files if len(f.split('/')) > f.split('/').index('web')+2]


def list_web_files_flat(files):
    return [f for f in files if len(f.split('/')) <= f.split('/').index('web')+2]


def get_web_repos_nested(files):
    return [{'xtls': [f], 'repo_name': f.split('/')[-2]+'.web'} for f in files]


def get_web_repos_flat(files):
    return [{'xtls': [f], 'repo_name': f.split('/')[-3]+'.web'} for f in files]


def merge_web_repos(repos):
    merged = []
    for r in repos:
        if len(merged) > 0:
            r_merged = False
            for m in merged:
                if r['repo_name'] == m['repo_name']:
                    m = merge(m, r)
                    r_merged = True
                    break
            if r_merged == False:
                merged.append(r)
        else:
            merged.append(r)
    return merged



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


def create_repos(data, existing_repo='/home/ubuntu/maps/',
                 repo_prefix='/home/ubuntu/test_repos/'):
    for d in data:
        repo = repo_prefix+d['repo_name']
        print 'setting up repo: '+repo
        if not os.path.isdir(repo):
            os.mkdir(repo)
        cwd = os.getcwd()
        os.chdir(repo)
        os.system('git init')
        xtls = [xtl.split(existing_repo)[1]
                for xtl in d['xtls'] if os.path.exists(xtl)]
        os.chdir(existing_repo)
        # exports git log of a file as a 'patch' which we apply to the new repo
        os.system('git log --pretty=email --patch-with-stat --reverse ' +
                  '-- '+' '.join(xtls)+' | (cd '+repo+' && git am)')
        os.chdir(repo)
        for xtl in xtls:
            if os.path.exists(xtl):
                # rewrites history with file at the top level instead of deeply nested
                os.system('git filter-branch -f --tree-filter \'if [ -f '+ xtl +
                          ' ]; then mv '+xtl+' .; fi\' HEAD')
        os.chdir(cwd)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        all_files = list_files(sys.argv[2])
        fi_maps = get_maps(list_fi_files(all_files))
        fi_repos = merge_shared_repos(fi_maps)
        web_files = list_web_files(all_files)
        web_repos = merge_web_repos(
            get_web_repos_nested(
                list_web_files_nested(web_files)) +
            get_web_repos_flat(
                list_web_files_flat(web_files)))
        all_repos = fi_repos + web_repos
        #create_repos(all_repos)
    else:
        print('usage: python repo_splitter dir')
