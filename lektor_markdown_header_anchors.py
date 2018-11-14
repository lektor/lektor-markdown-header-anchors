import re
import uuid
from collections import namedtuple

from lektor.pluginsystem import Plugin
from lektor.utils import slugify
from markupsafe import Markup

TocEntry = namedtuple('TocEntry', ['anchor', 'title', 'children'])


class MarkdownHeaderAnchorsPlugin(Plugin):
    name = 'Markdown Header Anchors'
    description = u'Lektor plugin that adds anchors and table of contents to markdown headers.'

    def on_markdown_config(self, config, **extra):
        class HeaderAnchorMixin(object):
            def header(renderer, text, level, raw):
                anchor_type = self.get_config().get('anchor-type')
                if anchor_type == "random":
                    anchor = uuid.uuid4().hex[:6]
                elif anchor_type == "custom":
                    # Extract custom anchor from origin header.
                    # The header should match the syntax:
                    # `text (#anchor)`,
                    # if matched, text and anchor get the value respectively,
                    # otherwise fallback to slugify function.
                    #
                    # Firstly, this syntax give the user the ability to
                    # customize the TOC anchor link.
                    # `# How Lektor Works (#anchor-text)` renders to
                    # <h1 id="anchor-text">How Lektor Works</h1>
                    #
                    # However this is a pretty workaround and useful way for
                    # those non-ascii languages, such as CJK to use the
                    # custom anchor as the slug.
                    # `# 中文标题 (#chinese-title)` renders to
                    # <h1 id="chinese-title">中文标题</h1>
                    match = re.search(r'(.*)\(#(.*)\)', text)
                    if match:
                        text, anchor = match.groups()
                        anchor = anchor.replace(' ', '')
                    else:
                        anchor = slugify(raw)
                else:
                    anchor = slugify(raw)
                renderer.meta['toc'].append((level, anchor, Markup(text)))
                return '<h%d id="%s">%s</h%d>' % (level, anchor, text, level)

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
