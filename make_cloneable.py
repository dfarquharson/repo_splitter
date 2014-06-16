import os


def append_config(d):
    conf = d+'/.git/config'
    if os.path.exists(conf):
        with open(conf, 'a') as f:
            f.write('[receive]\n\tdenyCurrentBranch = warn\n\tdenyDeleteCurrent = warn')


def add_post_receive(d):
    pr = d+'/.git/hooks/post-receive'
    with open(pr, 'w') as f:
        f.write('#!/bin/sh\n' +
                'git --git-dir=. --work-tree=$PWD/.. reset --hard')
    os.chmod(pr, 0775)


def main():
    for d in os.listdir('.'):
        print(os.getcwd()+'/'+d)
        if os.path.isdir(d+'/.git'):
            append_config(d)
            add_post_receive(d)


if __name__ == '__main__':
    main()
