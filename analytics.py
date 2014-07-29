import os
import ast
from xtl_to_json import main as _xtj


def get_xtls(cwd):
    return [os.path.join(parent, f)
            for (parent, dirs, files) in os.walk(cwd)
            for f in files if f.endswith('.xtl')]


def hasattval(xtl, att, val):
    print xtl
    atts = ast.literal_eval(_xtj(xtl))
    if atts is None:
        return False
    atts = atts['children'][0]['atts']
    return att in atts and atts[att] == val


def hassubstring(xtl, substr):
    with open(xtl, 'r') as f:
        return substr in f.read()
