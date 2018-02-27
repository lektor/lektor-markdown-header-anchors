from collections import Counter

import py
import mistune

from lektor.markdown import MarkdownConfig


def make_toc(plugin, text):
    
    cfg = MarkdownConfig()
    plugin.on_markdown_config(cfg)

    renderer = cfg.make_renderer()
    md = mistune.Markdown(renderer, **cfg.options)

    meta = {}
    md.renderer.meta = meta

    plugin.on_markdown_meta_init(meta)
    md(text)
    plugin.on_markdown_meta_postprocess(meta)

    return meta['toc']


def iter_entries(*entries):
    for entry in entries:
        yield entry
        for child in entry.children:
            for e in iter_entries(child):
                yield e


def test_unique_anchors(plugin):
    text = """
# H1
# H1
    """
    cnt = Counter(e.anchor for e in iter_entries(*make_toc(plugin, text)))
    assert cnt.most_common(1)[0][1] == 1


def test_inverse_headers(plugin):
    text = """
#### H4
## H2
    """
    toc = make_toc(plugin, text)
    assert len( make_toc(plugin, text) ) == 2


def test_two_level_jump(plugin):
    text = """
## H2
#### H4
    """
    toc = make_toc(plugin, text)
    assert len(toc) == 1
    assert len(toc[0].children) == 1
