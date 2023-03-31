import os
import shutil
import yaml
import textwrap
from typing import Tuple, Sequence

from ...markdown import Markdown


def _merge_subdicts(root: dict) -> dict:
    """ Merge/flatten nested dictionaries into one. """
    res = root[0].copy()
    for sub in root[1:]:
        res.update(sub)
    return res


class Content(dict):
    """ Parent class for all widgets. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    @property
    def active(self):
        """ Return True if the widget is active. """
        return self['meta'].get('active', False)

    @property
    def theme_dir(self):
        """ Root directory of the theme."""
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def template_dir(self):
        """ Root directory of the theme."""
        return os.path.join(self.theme_dir, 'templates')

    def build(self, **kwargs: dict):
        """ Build the section. """
        raise NotImplementedError


class Section(Content):
    """ A section of the website. """

    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'section.html')

    def build(self, **kwargs: dict):
        """ Build the section.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        with open(self.template, 'r') as f:
            template = f.read()

        title = self['meta']['title']
        name = self['name']
        section_class = self.get('section_class', '')

        template = template.replace('{{name}}', name)\
                           .replace('{{other-classes}}', section_class)\
                           .replace('{{title}}', title)\
                           .replace('{{description}}', self['content'].to_html())

        # generate menu reference
        ref = f"""<li><a class="page-scroll" href="#section-{name:s}">{title:s}</a></li>"""
        return template, ref

class Speakers(Content):
    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'speakers.html')

    def build(self, **kwargs: dict):
        """ Generates a speaker list section

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        with open(self.template, 'r') as f:
            template = f.read()

        title = self['meta']['title']
        name = self['name']
        section_class = self.get('section_class', '')

        # data
        items = self['meta']['speakers']
        item_format = textwrap.dedent("""
        <div class="speaker-item">
            <img src="{{headshot}}" style="height:150px">
            <h4>{{name}}</h4>
            <p>{{description}}</p>
        </div>""")
        speakers_ = []
        for entry in items:
            speakers_.append(
                item_format.replace('{{headshot}}', entry['image'])\
                           .replace('{{name}}', entry['name'])\
                           .replace('{{description}}', entry['title'])
            )
        template = template.replace('{{name}}', name)\
                        .replace('{{other-classes}}', section_class)\
                        .replace('{{title}}', title)\
                        .replace('{{description}}', self['content'].to_html())\
                        .replace('{{speakers-content}}', '\n'.join(speakers_))

        # generate menu reference
        ref = f"""<li><a class="page-scroll" href="#section-{name:s}">{title:s}</a></li>"""
        return template, ref


class Schedule(Content):
    """ Schedule section widget """

    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'schedule.html')

    def build(self, **kwargs: dict):
        """ Generates a program page.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        with open(self.template, 'r') as f:
            template = f.read()

        title = self['meta']['title']
        name = self['name']
        section_class = self.get('section_class', '')

        # data
        items = self['meta']['program']
        hl_item_format = """{time} <font color="0080FF">{title}</font> <br>"""
        item_format = """{time} {title} <br>"""
        description_format = """<span style="display:inline-block; width: 6em;"></span><i>{description}</i><br>"""

        day = None
        program_ = []
        for entry in items:
            item = {'day': "", 'time': '', 'title': '', 'description': False, 'highlight': False}
            item.update(entry)
            for k, v in item.items():
                item[k] = Markdown(v).to_html()\
                                     .replace('</p>', '')\
                                     .replace('<p>', '') if isinstance(v, str) else v
            day_ = item['day']
            if day_ != day:
                day = day_
                program_.append(f"""<h2 id="day-{day:s}">{day:s}</h2>""")
                day = day_
            if item.get('highlight', False):
                program_.append(hl_item_format.format(**item))
            else:
                program_.append(item_format.format(**item))
            if item['description']:
                for line in item['description'].split('\n'):
                    program_.append(description_format.format(description=line))

        template = template.replace('{{name}}', name)\
                        .replace('{{other-classes}}', section_class)\
                        .replace('{{title}}', title)\
                        .replace('{{description}}', self['content'].to_html())\
                        .replace('{{program-content}}', '\n'.join(program_))

        # generate menu reference
        ref = f"""<li><a class="page-scroll" href="#section-{name:s}">{title:s}</a></li>"""
        return template, ref


def content_from_file(filename: str,
                      **kwargs) -> "Content":
    """
    Parameters
    ----------
    filename : str
        The name of the program file to write.
    template_dir : str
        The name of the template files to use.

    Returns
    -------
    content: Content
        The content object to be used in the website.
    """
    content = Markdown.from_file(filename)
    content_type = content.meta.get('type', 'section')
    name = filename.split('/')[-1].split('.')[0]

    # add relevant categories
    type_mapping = {'section': Section, 'schedule': Schedule,
                    'speakers': Speakers, 'sponsors': Section,
                    'participants': Section,}

    return type_mapping[content_type](
        filename = filename,
        name = name,
        content=content,
        meta=content.meta,
        type=content_type,
        **kwargs)


class Generator(dict):
    """ Main page generator. """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    @classmethod
    def from_file(cls, path: str) -> 'Generator':
        with open(path, 'r') as f:
            return cls(**yaml.load(f, yaml.FullLoader))

    def build(self, fname: str, **kwargs):
        """ Generates the content of a markdown file.

        Parameters
        ----------
        fname : str
            The name of the markdown file to read.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        content = content_from_file(fname, **kwargs)
        return content.build(**kwargs)

    @property
    def theme_dir(self):
        """ Root directory of the theme."""
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def template_dir(self):
        """ Root directory of the theme."""
        return os.path.join(self.theme_dir, 'templates')

    @property
    def index_template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'index.html')

    def generate(self):
        root_dir = self['sourcedir']
        build_dir = self['builddir']
        static_dir = self['staticdir']
        index = Markdown.from_file(os.path.join(root_dir, 'index.md'))
        header = index.meta

        print(textwrap.dedent(f"""
        Generating website...
        ----------------------
        configuration:
            * content directory: {root_dir}
            * static content directory: {static_dir}
            * building directory: {build_dir}
            * theme directory: {self.theme_dir}
        """))

        with open(self.index_template, 'r') as f:
            template = f.read()

        event = _merge_subdicts(header['event'])
        organizers = _merge_subdicts(header['organizers'])
        imprint = _merge_subdicts(header['imprint'])
        privacy = _merge_subdicts(header['privacy-policy'])

        template = template.replace(r'{{event-title}}', event['title'])\
                           .replace(r'{{event-date}}', event['date'])\
                           .replace(r'{{event-venue}}', event['venue'])\
                           .replace(r'{{event-subtitle}}', event['subtitle'])\
                           .replace(r'{{organizer-logo}}', organizers['logo'])\
                           .replace(r'{{imprint-url}}', imprint['url'])\
                           .replace(r'{{imprint-name}}', imprint['name'])\
                           .replace(r'{{privacy-policy-url}}', privacy['url'])\
                           .replace(r'{{privacy-policy-name}}', privacy['name'])\
                           .replace(r'{{contact-url', organizers['contact_url'])

        # keep various sections
        sections = []
        # Navigation bar
        nav = []

        for section in header['content']:
            fname = os.path.join(root_dir, section + '.md')
            # alternate background color of sections
            if len(sections) % 2 == 0:
                section_class = ''
            else:
                section_class = "gray-bg"
            txt, reference = self.build(fname, section_class=section_class)
            sections.append(txt)
            nav.append(reference)

        template = template.replace('{{sections}}', ''.join(sections))\
                           .replace('{{nav-content}}', '\n'.join(nav))


        # construct the output folder
        if os.path.exists(build_dir):
            # remove if exists
            shutil.rmtree(build_dir)

        # copy theme resource files
        shutil.copytree(os.path.join(self.theme_dir, 'resources'), build_dir)

        # copy static files
        shutil.copytree(self['staticdir'],
                        os.path.join(build_dir, "static"))

        # export the index.html
        with open(os.path.join(build_dir, "index.html"), 'w') as f:
            f.write(template)

        print("\nWebsite generated into {}".format(build_dir))



def generate_index(path: str = None):
    """ Generates the index.html file. """
    if path is None:
        path = os.path.join(os.getcwd(), 'config.yml')
    generator = Generator.from_file(path)
    generator.generate()