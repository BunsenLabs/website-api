#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
        name = "blwwwapi",
        version = "1.0.7",
        install_requires = [
                "flask",
                "Flask-RESTful",
                "beautifulsoup4",
                "Django",
                "feedparser",
                "requests",
                "PyYAML>=5.1.1",
                "pydantic>=1.6.1",
        ],
        packages = find_packages(),
        entry_points={
                "console_scripts": [
                        "blwwwapi = blwwwapi.__main__:main"
                ]
        },
        author = "Jens John",
        author_email = "dev@2ion.de",
        description = "BunsenLabs Website API Services",
        license = "GPL3",
        keywords = "bunsenlabs service website",
        url = "https://github.com/bunsenlabs/bunsen-website",
        include_package_data=True,
)

