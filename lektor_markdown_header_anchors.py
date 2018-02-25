from lektor.pluginsystem import Plugin
from lektor.utils import slugify
from markupsafe import Markup
from collections import namedtuple, Counter


TocEntry = namedtuple('TocEntry', ['level', 'anchor', 'title', 'children'])


def uniquify(count, raw):
    anchor = slugify(raw)
    count[anchor] += 1
    if count[anchor] > 1:
        anchor = '%s~%d'%(anchor, count[anchor])
    return anchor


class MarkdownHeaderAnchorsPlugin(Plugin):
    name = 'Markdown Header Anchors'
    description = 'Adds anchors to markdown headers.'

    def on_markdown_config(self, config, **extra):
        class HeaderAnchorMixin(object):
            def header(renderer, text, level, raw):
                anchor = uniquify(renderer.meta['uniquify'], raw)
                renderer.meta['toc'].append(TocEntry(level, anchor, Markup(text), []))
                return '<h%d id="%s">%s</h%d>' % (level, anchor, text, level)
        config.renderer_mixins.append(HeaderAnchorMixin)

    def on_markdown_meta_init(self, meta, **extra):
        meta['toc'] = []
        meta['uniquify'] = Counter()

    def on_markdown_meta_postprocess(self, meta, **extra):
        stack = [TocEntry(-1, None, None, [])]

        for entry in meta['toc']:
            while stack[-1].level >= entry.level:
                stack.pop()
            stack[-1].children.append(entry)
            stack.append(entry)
    
        meta['toc'] = stack[0].children
