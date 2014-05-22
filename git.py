import subprocess
import sys
import os


ILLEGAL_ARGS = {'--delete', '-d', '|'}
ALLOWED_CMDS = {'add', 'status', 'log', 'init', 'branch',
                    'commit', 'diff', 'merge', 'checkout',
                    'ls-files'}


def execute(args):
    if any(arg in ILLEGAL_ARGS for arg in args):
        return ('Did not execute. Requested disallowed arg(s): ' +
                str(set(args) & ILLEGAL_ARGS).
                replace('set(', '').
                replace(')', ''))
    elif args[0] in ALLOWED_CMDS:
        p = subprocess.Popen(' '.join(['git']+args), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        return p.communicate()
    else:
        return 'Did not execute. Requested disallowed cmd: ' + args[0]


def log_to_dict(log):
    mylist = []
    for line in log.split('\n'):
        if len(line) > 0:
            if line.startswith('commit'):
                uuid = line.split()[1]
                curdict = {}
                curdict['id'] = uuid
                mylist.append(curdict)
            else:
                content = line.split()
                if len(content) > 0 and ':' in content[0]:
                    curdict[content[0].replace(':', '')] = \
                        ' '.join(content[1:])
                else:
                    if 'message' in curdict.keys():
                        curdict['message'] += '\n'+' '.join(content)
                    else:
                        curdict['message'] = ' '.join(content)
    return mylist


def git_add(filename):
    add = execute(['add', filename])
    print add
    print 'file: '+filename
    print 'added successfully'


def git_commit(message):
    commit = execute(['commit', '-m', '"'+message+'"'])
    print commit
    print 'committed successfully!'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python git.py chain of git commands')
    else:
        print(execute(sys.argv[1:]))
