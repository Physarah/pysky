import setuptools
from configparser import ConfigParser

with open("README.md",  "r") as fh:
    LONG_DESCRIPTION = fh.read()

conf = ConfigParser()
conf.read(['setup.cfg'])
metadata = dict(conf.items('metadata'))
VERSION = metadata.get('version', '0.0.dev')
PACKAGENAME = metadata.get('package_name', 'pysky')
DESCRIPTION = metadata.get(
    'description', 'A wrapper to parse the EUCLID NASA science centre sky background model in python')
AUTHOR = metadata.get('author', 'Sarah Caddy')
AUTHOR_EMAIL = metadata.get('author_email', 'sarah.caddy@hdr.edu.au')
LICENSE = metadata.get('license', 'MIT')
URL = metadata.get('url', '')
__minimum_python_version__ = metadata.get("minimum_python_version", "3.7")


setuptools.setup(name=PACKAGENAME,
                 version=VERSION,
                 description=DESCRIPTION,
                 author=AUTHOR,
                 author_email=AUTHOR_EMAIL,
                 license=LICENSE,
                 url=URL,
                 long_description=LONG_DESCRIPTION,
                 python_requires='>={}'.format(__minimum_python_version__)
                 )
