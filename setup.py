#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
#   Author(s): Milan Falesnik   <milan@falesnik.net>
#                               <mfalesni@redhat.com>
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from setuptools import setup


setup(
    name="kwargify",
    version="1.1.2",
    author="Milan Falešník",
    author_email="milan@falesnik.net",
    description="Python function kwargifier",
    license="GPLv2",
    keywords="kwargs",
    url="https://github.com/mfalesni/python-kwargify",
    py_modules=["kwargify"],
    install_requires=[],
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ]
)
