import os


def update_config(d):
    conf = d+'/.git/config'
    if os.path.exists(conf):
        sharedRepo = '\tsharedRepository = 0664\n'
        with open(conf, 'r') as f:
            data = f.readlines()
        if sharedRepo in data:
            return
        else:
            if '[receive]\n' in data:
                data.insert(data.index('[receive]\n'), sharedRepo)
            else:
                data.append(sharedRepo)
            with open(conf, 'w') as f:
                f.write(''.join(data))


def append_config(d):
    conf = d+'/.git/config'
    if os.path.exists(conf):
        with open(conf, 'a') as f:
            f.write('\tsharedRepository = 0664' +
                    '\n[receive]\n\tdenyCurrentBranch = warn' +
                    '\n\tdenyDeleteCurrent = warn')


def add_post_receive(d):
    pr = d+'/.git/hooks/post-receive'
    with open(pr, 'w') as f:
        f.write('#!/bin/sh\n' +
                'git --git-dir=. --work-tree=$PWD/.. reset --hard')
    os.chmod(pr, 0775)


def make_cloneable(repos):
    for repo in repos:
        print(repo)
        if os.path.isdir(repo+'/.git/'):
            append_config(repo)
            add_post_receive(repo)


#def main():
    #for d in os.listdir('.'):
        #print(os.getcwd()+'/'+d)
        #if os.path.isdir(d+'/.git'):
            #append_config(d)
            #add_post_receive(d)


if __name__ == '__main__':
    main()
