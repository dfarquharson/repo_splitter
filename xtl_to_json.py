import sys
import json
from lxml import etree


def xtl_to_json(elem, parent):
    if not parent:
        parent['name'] = unicode(elem.tag)
        parent['atts'] = dict(elem.attrib)
        parent['children'] = []
        for child in list(elem):
            xtl_to_json(child, parent)
    else:
        if unicode(elem.tag) == "<built-in function ProcessingInstruction>":
            this = {'name': 'java'}
        else:
            this = {'name': unicode(elem.tag)}
        if elem.attrib:
            this['atts'] = dict(elem.attrib)
        if elem.text and any(type(elem.text) == t for t in [str, unicode]) \
           and not elem.text.isspace():
            this['text'] = elem.text
        if parent:
            parent['children'].append(this)
        if list(elem):
            this['children'] = []
        for child in list(elem):
            xtl_to_json(child, this)


def main(xtl_file):
    """Given an .xtl file returns contents converted to JSON"""
    try:
        tree = etree.parse(xtl_file)
    except:
        return None
    root = tree.getroot()
    doc = {}
    xtl_to_json(root, doc)
    return json.JSONEncoder().encode(doc)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("needs one argument that is a .xtl file")
        exit(1)
    print(main(sys.argv[1]))
