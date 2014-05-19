import os


def list_files(cwd):
    return [str(fmt_dir(parent)+f)
            for (parent, dirs, files) in os.walk(cwd)
            for f in files]


def fmt_dir(path):
    return path if path.endswith('/') else path+'/'


def get_ext(x):
    return x.split('/')[-1].split('.')[-1]


def get_extensions(xs):
    exts = {}
    for x in xs:
        ext = get_ext(x)
        if ext in exts:
            exts[ext] += 1
        else:
            exts[ext] = 1
    return exts
