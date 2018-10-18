#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
        name = "blwwwapi",
        version = "1.0.4",
        install_requires = [
                "bottle",
                "beautifulsoup4",
                "Django",
                "feedparser",
                "requests",
                "tornado"
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
        url = "https://github.com/bunsenlabs/bunsen-website"
)

