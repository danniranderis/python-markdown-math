# -*- coding: utf-8 -*-

'''
Math extension for Python-Markdown
==================================

Adds support for displaying math formulas using [MathJax](http://www.mathjax.org/).

Author: 2015, Dmitry Shachnev <mitya57@gmail.com>.
'''

import markdown

class MathExtension(markdown.extensions.Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'enable_dollar_delimiter': [False, 'Enable single-dollar delimiter'],
            'render_to_span': [False,
                'Render to span elements rather than script for fallback'],
        }
        super(MathExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        def handle_match_inline(m):
            # Create parent element
            node_both = markdown.util.etree.Element('span')

            # if render_to_span (fallback for non-js) is set - create an
            # element for that
            if self.getConfig('render_to_span'):
                node_span = markdown.util.etree.Element('span')
                node_span.set('class', 'MathJax_Preview')
                node_span.text = ("\\\\(" + markdown.util.AtomicString(
                    m.group(3)) + "\\\\)")
                node_both.append(node_span)

            # Create MathJax element
            node_script = markdown.util.etree.Element('script')
            node_script.set('type', 'math/tex')
            node_script.text = markdown.util.AtomicString(m.group(3))
            node_both.append(node_script)

            return node_both

        def handle_match(m):
            node = markdown.util.etree.Element('script')
            node.set('type', 'math/tex; mode=display')
            if '\\begin' in m.group(2):
                node.text = markdown.util.AtomicString(m.group(2) + m.group(4) + m.group(5))
            else:
                node.text = markdown.util.AtomicString(m.group(3))
            return node

        inlinemathpatterns = (
            markdown.inlinepatterns.Pattern(r'(?<!\\|\$)(\$)([^\$]+)(\$)'),  #  $...$
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\\\()(.+?)(\\\))')     # \(...\)
        )
        mathpatterns = (
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\$\$)([^\$]+)(\$\$)'), # $$...$$
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\\\[)(.+?)(\\\])'),    # \[...\]
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\\begin{([a-z]+?\*?)})(.+?)(\\end{\3})')
        )
        if not self.getConfig('enable_dollar_delimiter'):
            inlinemathpatterns = inlinemathpatterns[1:]
        for i, pattern in enumerate(inlinemathpatterns):
            pattern.handleMatch = handle_match_inline
            md.inlinePatterns.add('math-inline-%d' % i, pattern, '<escape')
        for i, pattern in enumerate(mathpatterns):
            pattern.handleMatch = handle_match
            md.inlinePatterns.add('math-%d' % i, pattern, '<escape')

def makeExtension(*args, **kwargs):
    return MathExtension(*args, **kwargs)
