[![Travis CI status](https://api.travis-ci.org/mitya57/python-markdown-math.svg)][Travis]
[Travis]: https://travis-ci.org/mitya57/python-markdown-math

Math extension for Python-Markdown
==================================

This extension adds math formulas support to [Python-Markdown].

[Python-Markdown]: https://github.com/waylan/Python-Markdown

Installation
------------

### Install from PyPI

```
$ pip install python-markdown-math
```

### Install locally

Use `setup.py build` and `setup.py install` to build and install this
extension, respectively.

The extension name is `mdx_math`, so you need to add that name to your
list of Python-Markdown extensions.
Check [Python-Markdown documentation] for details on how to load
extensions.

[Python-Markdown documentation]: http://pythonhosted.org/Markdown/extensions/

Usage
-----

To use this extension, you need to include [MathJax] library in HTML files, like:

```html
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js"></script>
```

[MathJax]: http://www.mathjax.org/

Also, you need to specify a configuration for MathJax. Please note that
most of standard configuratons include `tex2jax` extension, which is not needed
with this code.

Example of MathJax configuration:

```html
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  config: ["MMLorHTML.js"],
  jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
  extensions: ["MathMenu.js", "MathZoom.js"]
});
</script>
```

To pass the extension to Python-Markdown, use `mdx_math` as extension name.
For example:

```python
>>> md = markdown.Markdown(extensions=['mdx_math'])
>>> md.convert('$$e^x$$')
'<p>\n<script type="math/tex; mode=display">e^x</script>\n</p>'
```

Usage from the command line:

```
$ echo "\(e^x\)" | python3 -m markdown -x mdx_math
<p>
<script type="math/tex">e^x</script>
</p>
```

Math Delimiters
---------------

For inline math, use `\(...\)`.

For standalone math, use `$$...$$`, `\[...\]` or `\begin...\end`.

The single-dollar delimiter (`$...$`) for inline math is disabled by
default, but can be enabled by passing `enable_dollar_delimiter=True`
in the extension configuration.

If you want to render to span elements when JavaScript is disabled or unavailable as to improve fallback,
use `render_to_span=True`.

Notes
-----

If you use [ReText](https://github.com/retext-project/retext), this extension
is not needed as it is included by default.
