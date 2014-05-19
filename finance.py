import os
from sys import argv


def get_repos(directory):
    return [{'xnet': d,
             'last_revision': '',
             'previous_revision': '',
             'days_between_revisions': ''} for d in os.listdir(directory)]


if __name__ == '__main__':
    print(get_repos('/Users/djfarquharson/test/unique_repos/')
          if len(argv) == 1 else 'usage: python finance.py')
