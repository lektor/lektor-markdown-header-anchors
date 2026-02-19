import inspect
import re
from pathlib import Path

from lektor.context import Context
from lektor.metaformat import serialize
from lektor.project import Project
from markupsafe import Markup
import pytest

from lektor_markdown_header_anchors import MarkdownHeaderAnchorsPlugin


def write_file(path, contents):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents)


@pytest.fixture
def env(tmp_path):
    project_dir = tmp_path
    project_file = project_dir / "test.lektorproject"
    write_file(project_file, "")
    write_file(
        project_dir / "models/page.ini",
        (
            "[fields.body]\n"
            "type = markdown\n"
        )
    )

    project = Project.from_file(project_file)
    return project.make_env()


@pytest.fixture
def pad(env):
    pad = env.new_pad()
    with Context(pad=pad):
        yield pad


@pytest.fixture
def make_markdown(pad):
    def make_markdown(markdown_src):
        fields = [("body", markdown_src)]
        write_file(
            Path(pad.env.root_path, "content/contents.lr"),
            "".join(serialize(fields))
        )
        return pad.root["body"]

    yield make_markdown


def test_html(make_markdown):
    markdown = make_markdown("# This & That\n")
    assert re.match(
        r"<h1 id=([\"'])this-that\1>This &amp; That</h1>\s*\Z",
        markdown.html
    )


def test_toc(make_markdown):
    markdown = make_markdown(inspect.cleandoc(
        """
        ## Heading One
        ## Heading Two
        ### Heading 2.1
        ## Heading Three
        """
    ))
    toc = markdown.meta["toc"]
    assert toc == [
        ('heading-one', Markup('Heading One'), []),
        ('heading-two', Markup('Heading Two'), [
            ('heading-2.1', Markup('Heading 2.1'), []),
        ]),
        ('heading-three', Markup('Heading Three'), []),
    ]


def test_plugin_description(env):
    plugin = MarkdownHeaderAnchorsPlugin(env, "dummy-id")
    assert plugin.description.startswith("Lektor plugin that adds anchors")


@pytest.mark.parametrize("heading, expected_anchor", [
    ("`keyword`", "keyword"),
    ("b&amp;", "b"),
    ("b&_amp;_", "b-amp"),
    ("&_amp;_", "amp"),
])
def test_anchor(make_markdown, heading, expected_anchor):
    markdown = make_markdown(f"# {heading}\n")
    (entry,) = markdown.meta['toc']
    assert entry.anchor == expected_anchor
