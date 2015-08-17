#!/usr/bin/env python

"""Quick-and-dirty approximation of hibidi on XHTML.

This doesn't really perform the bidi algorithm at each level.
It only infers the base direction of each element and takes it
as default for the whole element.

This means that in::

    <foo>
        ltr
        <bar>??</bar>
        RTL
        <quux>??</quux>
        RTL
        <baz>??</baz>
        ltr
    </foo>

the neutral element quux will not be inferred as RTL although it should be
according to the spec.

I do intend to implement it fully, but for now this is enough for 98% of mixed
documents out there...

Code by Beni Cherniavsky to process rst with hibidi.
See http://docutils.sourceforge.net/FAQ.html#bidi for details.
"""

import unicodedata
from xml.dom.minidom import parseString, Node, Text

def hibidi_unicode(u, root='html/body', encoding='utf-8'):
    """Takes an XML unicode string, returns a new one."""
    return hibidi_str(u.encode(encoding), root).decode(encoding)

def hibidi_str(s, root='html/body', encoding=None):
    """Takes an XML string, returns a new one."""
    doc = parseString(s)
    hibidi_dom(doc, root)
    return doc.toxml(encoding=encoding or doc.encoding)

def hibidi_dom(doc, root='html/body'):
    """Takes a dom object, mutates it in-place."""
    nodes = [doc]
    for name in root.split('/'):
        nodes = [n for node in nodes
                   for n in node.getElementsByTagName(name)]
    for node in nodes:
        infer_dirs(node)
        assign_dirs(node)
        apply_dirs(node)

def text_dir(c):
    """Classify a character as 'R'/'L'/''."""
    dir = unicodedata.bidirectional(c)
    if dir in ('L',):
        return 'L'
    if dir in ('R', 'AL'):
        return 'R'
    return ''

def infer_dirs(node):
    """Infer (store & return) dirs in bottom-up order."""
    if node.nodeType != Node.ELEMENT_NODE:
        return ''
    # recurse anyway - to infer dir of all elements
    dirs = map(infer_dirs, node.childNodes)
    # first strong dir will be returned.
    def gen_dirs():
        # explicit dir attr?
        try:
            attr = node.attributes['dir']
            yield {'rtl': 'R', 'ltr': 'L'}[attr.value.lower()]
        except KeyError:
            pass
        # directly contains strong text?
        for child in node.childNodes:
            # text nodes don't get their own dir - they are not elements
            if child.nodeType in (Node.TEXT_NODE,  Node.CDATA_SECTION_NODE):
                for c in child.nodeValue:
                    yield text_dir(c)
        # from child nodes
        for dir in dirs:
            yield dir
    for dir in gen_dirs():
        if dir:
            node.dir = dir
            #node.attributes['inferred_dir'] = dir #@@@
            return dir
    node.dir = ''
    return ''

def assign_dirs(node, base_dir=''):
    """Assign dirs to neutral nodes."""
    if node.nodeType != Node.ELEMENT_NODE:
        return
    if not node.dir:
        node.dir = base_dir
        #node.attributes['assigned_dir'] = base_dir #@@@
    for child in node.childNodes:
        assign_dirs(child, node.dir)

LRM = Text()
LRM.data = u'\N{LEFT-TO-RIGHT MARK}'
RLM = Text()
RLM.data = u'\N{RIGHT-TO-LEFT MARK}'

def apply_dirs(node, base_dir=''):
    """Create dir attributes where needed."""
    if node.nodeType != Node.ELEMENT_NODE:
        return
    dir = node.dir
    if dir is not None and dir != base_dir:
        node.attributes['dir'] = {'R': 'RTL', 'L': 'LTR'}[dir]

        # The following helps OpenOffice's HTML parser.  The proper solution
        # is to implement hibidi on OpenOffice documents after the conversion
        # (or fix the parser to use dir attributes), so I don't want this on
        # by default.
        ## mark = {'R': RLM, 'L': LRM}[dir]
        ## if not (node.childNodes[0].nodeType == Node.TEXT_NODE and
        ##         node.childNodes[0].data.startswith('\n')):
        ##     node.childNodes.insert(0, mark)
        ## if not (node.childNodes[-1].nodeType == Node.TEXT_NODE and
        ##         node.childNodes[-1].data.endswith('\n')):
        ##     node.childNodes.append(mark)
        ## node.attributes['lang'] = {'R': 'he', 'L': 'en'}[dir]
        ## node.attributes['align'] = {'R': 'right', 'L': 'left'}[dir]
    for child in node.childNodes:
        apply_dirs(child, dir)

if __name__ == '__main__':
    import sys
    sys.stdout.write(hibidi_str(sys.stdin.read()))
