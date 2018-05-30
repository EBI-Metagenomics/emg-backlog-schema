import os
from setuptools import find_packages, setup

# with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
#     README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

_base = os.path.dirname(os.path.abspath(__file__))
_requirements = os.path.join(_base, 'requirements.txt')

install_requirements = []
with open(_requirements) as f:
    install_requirements = f.read().splitlines()


setup(
    name='emg_backlog_schema',

    version='0.3.7',
    description="Django DB schema for EBI-Metagenomics",

    author="Miguel Boland",
    author_email="mdb@ebi.ac.uk",

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requirements,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    entry_points={
        'console_scripts': [
            'emgbacklog=backlog_cli.manage:main',
        ],
    },
)
