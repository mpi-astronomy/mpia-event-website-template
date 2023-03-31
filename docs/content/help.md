---
active: True
title: Help page
type: section
---

This page gives a small guidance about the edition of the pages.

# Stucture of website

The website itself is defined in the `docs/content` directory and configured via the `index.md` file (also index page).

Static files such as specific images should be stored in the `docs/static` directory.

## Content in Markdown

Any page is defined by a Markdown document (see [Markdown cheatsheet](https://www.markdownguide.org/cheat-sheet/)). Markdown is a simple, yet powerful, syntax to generate content.

Markdown is already a rich text format with simple syntax. It also allows one to use HTML code to extend the content not already covered by Markdown language. In addition to the basic syntax, you can also use icons from the [Font Awesome](https://fontawesome.com/icons?d=gallery) and [academicons](https://jpswalsh.github.io/academicons/) libraries.

## YAML Metadata Block

We use extensively the YAML front matter extension to store metadata about the individual pages and their configuration (see [extension-yaml_metadata_block](https://pandoc.org/MANUAL.html#extension-yaml_metadata_block) introduced by Pandoc). YAML is a very simple (bullet list) syntax  to represent complex structures. The metadata block is the block between `---` at the top of the files.

For example, the `help` page starts with the following metadata block
```yaml
active: True
title: Help page
type: section
```

The actual content of this block is flexible and only needs specific fields depending on the type of page one wants to create.

One of the important field is `active` which sets if a page should be included or not when listed in the index page.

## Index Page

The index page is the `index.md` file (`type: index`) which defines the event information throughout the site.

Example of metadata block for the index page:

```yaml
event:  # part of the top banner of the site
    - title: MPIA conference website template
    - subtitle: A simple generator using markdown and python
    - date: Date of the event
    - venue: Max Planck Institute for Astronomy, Heidelberg, Germany

organizers:
    - name: The Data Science Team
    - url: https://github.com/mpi-astronomy
    - logo: https://upload.wikimedia.org/wikipedia/commons/c/c6/Max-Planck-Institut_f%C3%BCr_Astronomie_Logo.svg  # -- MPIA logo
    - contact_url: "ds@mpia.de" # -- contact

imprint:
    - url: http://www.mpia.de/imprint
    - name: imprint

privacy-policy:
    - url: http://www.mpia.de/privacy-policy
    - name: privacy policy

content:   # the content and ordering of the sections
    - help
    - overview
    - organizers
    - participants
    - speakers
    - programme
    - venue-mpia
    - logistics
    - travel-mpia
    - code-of-conduct
```

## Other page templates

Below we list the differents section types  (e.g., `type: section` or `type: index`).

| Section Type | Description                                                 |
|--------------|-------------------------------------------------------------|
| `section`    | Base block, a simple freeform section                       |
| `schedule`   | The schedule page which takes its content from the metadata |
| `speakers`   | A speaker list with pictures and information                |

<i class="fa-solid fa-info"></i> See examples of content and metadata in the `docs/content` directory.

<i class="fa-regular fa-lightbulb"></i> More types can be added by defining new templates in the `src/themes/default/templates` directory.

# Template text

We provide typical text template for conference events happening at MPIA or the HdA, and Ringberg.
Feel free to submit a pull request if you want these to be updated or if you want to add more templates.

# Generating website

## Offline

### Python dependencies
You first need to install the python dependencies which come with this package (`markdown` and `pyyaml`)

```bash
pip install .
```

### Compile the website
Then you only need to run the `Makefile` in the `docs` directory:

```bash
make html
```

### Serve locally

Especially when drafting content, being able to quickly serve the content of the site locally is useful.

```bash
python -m http.server --directory="docs/_build/html"
```

## Hosted by GitHub Pages

In your repository settings, you need to setup the `Pages` options.

Set the branch to `gh-pages` and save.

The github action script automatically compiles the site into this branch every time a push is performed.