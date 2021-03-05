from lektor.pluginsystem import Plugin
import uuid
from lektor.utils import slugify
from markupsafe import Markup
from collections import namedtuple


TocEntry = namedtuple('TocEntry', ['anchor', 'title', 'children'])


class MarkdownHeaderAnchorsPlugin(Plugin):
    name = 'Markdown Header Anchors'
    description = u'Lektor plugin that adds anchors and table of contents to markdown headers.'

    def on_markdown_config(self, config, **extra):
        class HeaderAnchorMixin(object):
            def header(renderer, text, level, raw):
                if self.get_config().get('anchor-type') == "random":
                    anchor = uuid.uuid4().hex[:6]
                else:
                    anchor = slugify(raw)
                renderer.meta['toc'].append((level, anchor, Markup(text)))
                if self.get_config().get_bool('anchor-link.enable'):
                    label = self.get_config().get('anchor-link.label', '&#182;')
                    classname = self.get_config().get('anchor-link.class', 'anchor-link')
                    spacer = self.get_config().get('anchor-link.spacer', '')
                    if self.get_config().get_bool('anchor-link.place-left'):
                        anchorlink = '<span class="%s"><a href="#%s">%s</a>%s</span>' % (classname, anchor, label, spacer)
                        formatstring = '<h%d id="%s">%s%s</h%d>' % (level, anchor, anchorlink, text, level)
                    else:
                        anchorlink = '<span class="%s">%s<a href="#%s">%s</a></span>' % (classname, spacer, anchor, label)
                        formatstring = '<h%d id="%s">%s%s</h%d>' % (level, anchor, text, anchorlink, level)
                else:
                    formatstring = '<h%d id="%s">%s</h%d>' % (level, anchor, text, level)
                return formatstring
        config.renderer_mixins.append(HeaderAnchorMixin)

    def on_markdown_meta_init(self, meta, **extra):
        meta['toc'] = []

    def on_markdown_meta_postprocess(self, meta, **extra):
        prev_level = None
        toc = []
        stack = [toc]

        for level, anchor, title in meta['toc']:
            if prev_level is None:
                prev_level = level
            elif prev_level == level - 1:
                stack.append(stack[-1][-1][2])
                prev_level = level
            elif prev_level > level:
                while prev_level > level:
                    # Just a simple workaround for when people do weird
                    # shit with headlines.
                    if len(stack) > 1:
                        stack.pop()
                    prev_level -= 1
            stack[-1].append(TocEntry(anchor, title, []))

        meta['toc'] = toc
