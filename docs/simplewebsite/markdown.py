""" A convenient interface to Markdown input and output. """
from typing import Tuple
import markdown
import yaml
import os


def _pop_meta(content) -> Tuple[str, dict]:
    """ Extract meta data from a markdown content.

    Meta data section starts with `---` and ends with `---`
    This function expects the meta data in one block, in yaml format.
    """
    header = []
    rest = []
    header_content = False
    for line in content.splitlines():
        if line.startswith('---'):
            header_content = ~header_content
            continue
        if header_content:
            header.append(line)
        else:
            rest.append(line)

    meta = yaml.load('\n'.join(header), yaml.FullLoader)
    if meta is None:
        meta = {}

    return '\n'.join(rest), meta


def _parse_md(mdtxt: str, **kwargs) -> str:
    """ Parse a markdown string.

    Parameters
    ----------
    mdtxt : str
        The markdown string to parse.
    extensions: Sequence[str]
        A list of extensions.  If an item is an instance of a subclass of
        `markdown.extension.Extension`, the  instance will be used as-is. If an
        item is of type string, first an entry point will be loaded. If that
        fails, the string is assumed to use Python dot notation
        (`path.to.module:ClassName`) to load a markdown.Extension subclass. If
        no class is specified, then a `makeExtension` function is called within
        the specified module.
    extension_configs: dict
        Configuration settings for extensions.
    output_format: str
        Format of output. Supported formats are:
        * "xhtml": Outputs XHTML style tags. Default.
        * "html": Outputs HTML style tags.
    tab_length: int
        Length of tabs in the source. Default: 4

    Returns
    -------
    html : str
        The parsed html string.
    """
    extensions_ = kwargs.pop("extensions", None)
    return markdown.markdown(mdtxt, extensions=extensions_, **kwargs)


class Markdown(str):
    """Convenient upgraded string object with meta data
    """

    # default extensions (note the meta extension is internally replaced)
    extensions = ['extra']

    def __new__(cls, *args, **kwargs):
        meta = kwargs.pop("meta", {})
        obj = str.__new__(cls, *args, **kwargs)
        obj.meta = meta
        return obj

    def parse_meta(self):
        """ Parse the meta data from the markdown string. """
        txt, meta = _pop_meta(self)
        if meta:
            return self.__class__(txt, meta=meta)
        return self

    def copy(self):
        """ Return a copy of the Markdown object. """
        return self.__class__(self[:],
                              meta=self.meta.copy())

    def to_md(self):
        """ Convert to markdown string with meta header if defined.

        Returns
        -------
        md : str
            The markdown string.
        """
        if self.meta:
            return '---\n' + yaml.dump(self.meta) + '---\n' + self
        return self

    def to_html(self, **kwargs):
        """ return the hmtl representation of the markdown string. """
        return self._repr_html_()

    def _repr_html_(self):
        """ return the hmtl representation of the markdown string. """
        return _parse_md(self, extensions=self.extensions)

    @classmethod
    def from_file(cls, path: str) -> 'Markdown':
        """ Read a markdown file and return a Markdown object. """
        return parse_file(path)


def parse_file(fname: str, **kwargs):
    """ Parse file with markdown and potentially a header metadata."""
    with open(fname, 'r') as fin:
        res = Markdown(fin.read(), **kwargs)
    return res.parse_meta()