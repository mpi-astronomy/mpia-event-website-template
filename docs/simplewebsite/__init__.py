import os
import sys
import importlib

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

try:
    __version__ = metadata.version(__package__ or __name__)
except:
    __version__ = "dev"


def generate(cfgfile: str = None):
    """ Generates the website from a given configuration file. """
    if cfgfile is None:
        cfgfile = os.path.join(os.getcwd(), 'config.yml')
    if not os.path.isfile(cfgfile):
        raise FileNotFoundError(f"{cfgfile} does not exist.")
    import yaml

    with open(cfgfile, 'r') as f:
        theme_name = yaml.load(f, yaml.FullLoader).get('theme', 'default')

    where = importlib.import_module(f"simplewebsite.themes.{theme_name}.index")

    generator = where.Generator.from_file(cfgfile)
    generator.generate()