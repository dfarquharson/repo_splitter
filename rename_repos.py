import os
import sys
import shutil


def get_dirs(cwd):
    return ['/Users/djfarquharson/test/unique_repos/'+x
            for x in os.listdir(cwd)]


def rename_dirs(dirs):
    for d in dirs:
        print 'inspecting dir: '+d
        xtls = [x for x in os.listdir(d) if x.endswith('.xtl')]
        if len(xtls) > 2:
            new_name = '.'.join(d.split('.')[:-1] + ['shared'])
            if os.path.isdir(new_name):
                print 'copying files from '+d+' to '+new_name
                for xtl in xtls:
                    if not os.path.exists(d+'/'+xtl):
                        shutil.copy(d+'/'+xtl, new_name)
                shutil.rmtree(d)
            else:
                print 'renaming '+d+' to '+new_name
                print xtls
                print len(xtls)
                os.rename(d, new_name)


if __name__ == '__main__':
    rename_dirs(get_dirs(sys.argv[1]))
