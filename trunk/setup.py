#! /usr/bin/env python

from distutils.core import setup

setup(
    name = 'meshconvert',
    version = '0.2',    
    package_dir = {'':'src'},
    packages = ['meshconvert'],
    scripts = ['scripts/meshconvert'],
    author = 'Denis Barbier',
    author_email = 'barbier(at)linuxfr.org',
    description = 'Mesh converter for FEM applications',
    license = 'GPLv3',
    url = 'http://code.google.com/p/meshconvert/',
)

