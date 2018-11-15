# lektor-markdown-header-anchors

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
  <li><a href="#{{ item.anchor }}">{{ item.title }}</a>
  {% if item.children %}
    <ul>{{ loop(item.children) }}</ul>
  {% endif %}
  </li>
{% endfor %}
</ul>
```

## Configuring the Plugin

The plugin has a config file that is used to configure a few things 
for the anchor type. Just create a file named `markdown-header-anchors.ini`
into your `configs/` folder.

```ini
anchor-type = custom
``` 

You can configure different `anchor-type` to render different style anchor link.
There are two anchor types:

- **custom** - Extract custom anchor from the origin header.

The header should match the syntax: `text (#anchor)`, if matched, text and anchor 
get the value respectively, otherwise fallback to the `slugify` function.

This syntax give the user the ability to customize the TOC anchor link.

>`# How Lektor Works (#anchor-text)` renders to `<h1 id="anchor-text">How Lektor Works</h1>`

However this is a pretty workaround and useful way for those non-ascii languages, 
such as CJK to use the custom anchor as the slug.

> `# 中文标题 (#chinese-title)` renders to `<h1 id="chinese-title">中文标题</h1>`

- **random** - Generate a random id as an anchor, for users who is using no-ascii head text.

If the **anchor-type** value is missing or incorrect, this will fallback to 
the default `slugify` style which using built-in `slugify()` function 
to render ascii slug as the anchor.