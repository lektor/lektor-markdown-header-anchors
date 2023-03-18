import uuid
from collections import namedtuple

import mistune
from lektor.pluginsystem import Plugin
from markupsafe import Markup
from slugify import slugify

TocEntry = namedtuple('TocEntry', ['anchor', 'title', 'children'])


class MarkdownHeaderAnchorsPlugin(Plugin):
    name = 'Markdown Header Anchors'
    description = u'Lektor plugin that adds anchors and table of contents to markdown headers.'

    def on_markdown_config(self, config, **extra):
        config.renderer_mixins.append(
            renderer_mixin_factory(slugify=self._slugify)
        )

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

    def _slugify(self, text):
        if self.get_config().get('anchor-type') == "random":
            return uuid.uuid4().hex[:6]
        # NB: slugify decodes HTML entities in its input before slugifying
        return slugify(text)


def renderer_mixin_factory(slugify=slugify):
    def render_header(text, level, meta):
        anchor = slugify(text)
        meta['toc'].append((level, anchor, Markup(text)))
        return '<h%d id="%s">%s</h%d>' % (level, anchor, text, level)

    class RendererMixin_mistune0(object):
        def header(self, text, level, raw):
            return render_header(text, level, self.meta)

    class RendererMixin_mistune2(object):
        def heading(self, text, level):
            meta = self.lektor.meta  # Lektor >= 3.4
            return render_header(text, level, meta)

    if mistune.__version__.startswith("0."):
        return RendererMixin_mistune0
    elif mistune.__version__.startswith("2."):
        return RendererMixin_mistune2
    else:
        raise RuntimeError("unsupported mistune version")
