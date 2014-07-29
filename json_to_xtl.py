import sys
import json
from lxml import etree
from collections import OrderedDict


def json_to_xtl(blob, parent):
    if blob['name'] == 'java':
        element = etree.ProcessingInstruction('java', blob['text']
                                              if 'text' in blob else '')
        parent.append(element)
    else:
        element = etree.SubElement(parent, blob['name'])
        if 'atts' in blob:
            atts = OrderedDict(sorted(blob['atts'].items()))
            for key in list(atts):
                val = unicode(atts[key])
                if len(val) > 0:
                    element.set(key, val)
        if 'text' in blob:
            element.text = unicode(blob['text'])
    if 'children' in blob:
        for child in list(blob['children']):
            json_to_xtl(child, element)


def main(json_file, stream=False):
    '''Given a .json file, writes an .xtl file.
       Returns a pointer to created .xtl file.'''
    if stream:
        data = json_file
    else:
        with open(json_file, 'r') as f:
            data = f.read().replace('\n', '')

    blob = json.loads(data)
    root = etree.Element('root')  # placeholder element
    tree = etree.ElementTree(root)
    json_to_xtl(blob, root)
    betterroot = tree.getroot()[0]
    tree = etree.ElementTree(betterroot)
    if stream:
        return etree.tostring(tree, pretty_print=True)
    else:
        xtl_file = json_file.replace('.json', '.xtl')
        with open(xtl_file, 'w') as f:
            f.write(etree.tostring(tree, pretty_print=True))
        return xtl_file

if __name__ == '__main__':
    print(main(sys.argv[1]) if len(sys.argv) == 2
          else 'needs one argument that is a .json file')
