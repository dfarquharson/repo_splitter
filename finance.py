import os
from git import execute as _git
from git import log_to_dict as _log
from sys import argv
from pprint import pprint


def get_log(repo):
    cwd = os.getcwd()
    os.chdir(repo)
    log = _log(_git(['log'])[0])
    os.chdir(cwd)
    return log


def get_next_revision(log):
    for l in log:
        if 'jstauffe' not in l['Author']:
            yield l


def get_repos(directory):
    entries = []
    for d in os.listdir(directory):
        log = get_log(directory+'/'+d)
        rev_generator = get_next_revision(log)
        try:
            last_rev = rev_generator.next()
            prev_rev = rev_generator.next()
        except StopIteration:
            last_rev = ''
            prev_rev = ''
        entries.append({'xnet': d,
                        'last_revision': last_rev,
                        'previous_revision': prev_rev,
                        'days_between_revisions': ''})
    return entries


if __name__ == '__main__':
    print(get_repos('/Users/djfarquharson/test/unique_repos/')
          if len(argv) == 1 else 'usage: python finance.py')
