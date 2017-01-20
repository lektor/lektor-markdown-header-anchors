from setuptools import setup

setup(
    name='lektor-markdown-header-anchors',
    description='Adds support for anchors and table of contents to Markdown.',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    url='http://github.com/lektor/lektor-markdown-header-anchors',
    version='0.2',
    license='BSD',
    py_modules=['lektor_markdown_header_anchors'],
    entry_points={
        'lektor.plugins': [
            'markdown-header-anchors = lektor_markdown_header_anchors:MarkdownHeaderAnchorsPlugin',
        ]
    }
)
