import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'sensed',
    version = '1.0',
    author = 'R. Cody Maden',
    description = 'A sensor network server and client library.',
    license = 'MIT',
    keywords = 'sensor network sensed',
    url = 'http://github.com/sli/sensed',
    packages = ['sensed', 'tests'],
    scripts = ['bin/sensed'],
    long_description = read('README.md'),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking'
    ]
)
