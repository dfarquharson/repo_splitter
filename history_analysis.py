import git as G
import os


def get_history(dirs):
    result = []
    cwd = os.getcwd()
    for d in dirs:
        os.chdir(d)
        log = G.log_to_dict(G.execute(['log'])[0])
        result.append([d, log])
    os.chdir(cwd)
    return result
