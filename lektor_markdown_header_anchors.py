import uuid
from collections import namedtuple
from html.parser import HTMLParser
from importlib import metadata

import mistune
from lektor.pluginsystem import Plugin
from markupsafe import escape
from markupsafe import Markup
from slugify import slugify

TocEntry = namedtuple('TocEntry', ['anchor', 'title', 'children'])


class MarkdownHeaderAnchorsPlugin(Plugin):
    name = 'Markdown Header Anchors'

    @property
    def description(self) -> str:
        dist = metadata.distribution(self.__module__)
        return dist.metadata.get("summary")

    def on_markdown_config(self, config, **extra):
        anchor_type = self.get_config().get('anchor-type')
        config.renderer_mixins.append(
            renderer_mixin_factory(anchor_type)
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


def renderer_mixin_factory(anchor_type=None):
    def render_header(text, level, meta, raw=None):
        if anchor_type == "random":
            anchor = uuid.uuid4().hex[:6]
        else:
            if raw is None:
                # Mistune2 does not make the raw un-marked-up text available,
                # so we have to regenerate it here by stripping HTML tags from
                # the markup.
                #
                # NB: slugify() decodes HTML entities, as does _strip_tags().
                # We need to encode here again to prevent double-decoding.
                raw = escape(_strip_tags(text))
            anchor = slugify(raw)
        meta['toc'].append((level, anchor, Markup(text)))
        return '<h%d id="%s">%s</h%d>' % (level, anchor, text, level)

    class RendererMixin_mistune0(object):
        def header(self, text, level, raw):
            return render_header(text, level, self.meta, raw)

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


def _strip_tags(inline_html: str) -> str:
    """Strip HTML tags from inline content.

    This is a fairly stupid HTML tag stripper.  All tags are assumed to be inline.

    NB: This should not be used for security/sanitization purposes. (E.g.
    the bodies of <script> tags are not stripped.)
    """
    parser = _StripTagsParser()
    parser.feed(inline_html)
    return parser.close()


class _StripTagsParser(HTMLParser):
    _data: list[str]

    def reset(self) -> None:
        super().reset()
        self._data = []

    def handle_data(self, data: str) -> None:
        self._data.append(data)

    def close(self) -> str:
        super().close()
        return "".join(self._data)
