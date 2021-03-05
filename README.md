# lektor-markdown-header-anchors

This plugin extends the markdown support in Lektor in a way that headlines
are given anchors and a table of contents is collected.

## Enabling the Plugin

To enable the plugin run this command:

```shell
$ lektor plugins add markdown-header-anchors
```

## Configuring the Plugin

The plugin has a config file that is used to configure a few things.
Just create a file named `markdown-header-anchors.ini` into your
`configs/` folder. The config may contain the following entries:

```ini
anchor-type = random

[anchor-link]
enable = true
label = &#182;
place-left = false
spacer = &ensp;
class = anchor-link
```

| Configuration name | Description | Default value |
|---|---|---|
| anchor-type | If set to `random` the anchor will be a randomly generated hexstring. If not set or empty the anchor will be the slugified heading. | \<empty> |
| **[anchor-link]** | Section for configuring the anchor link. | |
| enable | If set to true an anchor link will be inserted next to the heading. | false |
| label | The label of the anchor link. This can be any text or html such as the default value. | `&#182;` (¶) |
| place-left | Whether the anchor link is placed left of the heading instead of right. | false |
| spacer | The text or html that is to be displayed between the anchor link and the heading. Any whitespace is removed from the value itself so instead html must be used e.g. `&ensp;`. | \<empty> |
| class | The class name of the anchor link. | anchor-link |

## Example

Using the configuration above, the markdown
```markdown
## Header
```
would generate the following html (newlines added for readability)
```html
<h2 id="e5bd93">
    Header
    <span class="anchor-link">
        &ensp;
        <a href="#e5bd93">&#182;</a>
    </span>
</h2>
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
