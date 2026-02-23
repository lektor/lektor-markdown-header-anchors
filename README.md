# lektor-markdown-header-anchors

[![CI Badge][CI Badge]][CI] [![PyPI Version Badge][PyPI Version Badge]][PyPI]

[CI Badge]: https://github.com/lektor/lektor-markdown-header-anchors/actions/workflows/ci.yml/badge.svg
[CI]: https://github.com/lektor/lektor-markdown-header-anchors/actions/workflows/ci.yml
[PyPI Version Badge]: https://img.shields.io/pypi/v/lektor-markdown-header-anchors
[PyPI]: https://pypi.org/project/lektor-markdown-header-anchors/

This plugin extends the markdown support in Lektor in a way that headlines
are given anchors and a table of contents is collected.

## Enabling the Plugin

To enable the plugin run this command:

```shell
$ lektor plugins add markdown-header-anchors
```

## In Templates

Within templates it becomes possible to access the `.toc` property of
markdown data.  It's a list where each item has the following attributes:

* `anchor`: the name of the anchor
* `title`: the title of the headline as HTML
* `children`: a list of headers below that header

Example rendering:

```jinja
<h4>Table Of Contents</h4>
<ul class="toc">
{% for item in this.body.toc recursive %}
  <li><a href="#{{ item.anchor }}">{{ item.title }}</a>{%
   if item.children %}<ul>{{ loop(item.children) }}</ul>{% endif %}</li>
{% endfor %}
</ul>
```
