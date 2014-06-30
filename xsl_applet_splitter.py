import os
import sys


def list_files(cwd):
    return [fmt_dir(parent, f)
            for (parent, dirs, files) in os.walk(cwd)
            for f in files if '.git' not in parent]


def fmt_dir(path, f):
    return str((path if path.endswith('/') else path+'/')+f)


def get_files_with_extensions(cwd, exts=['.xsl', '.jpg', '.gif', '.png']):
    return [fmt_dir(parent, f)
            for (parent, dirs, files) in os.walk(cwd)
            for f in files if '.git' not in parent and
            any(f.endswith(ext) for ext in exts)]


def delete_non_matching(cwd, exts=['.xsl', '.jpg', '.gif', '.png']):
    ''' actually does the magic for the xsl repo creation'''
    for (parent, dirs, files) in os.walk(cwd):
        for f in files:
            if '.git' not in parent and '.git' not in f and \
               not any(f.endswith(ext) for ext in exts):
                os.remove(fmt_dir(parent, f))
