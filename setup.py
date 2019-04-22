#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
        name = "blwwwapi",
        version = "1.0.5",
        install_requires = [
                "bottle==0.12.16",
                "beautifulsoup4==4.7.1",
                "Django==2.2",
                "feedparser==5.2.1",
                "requests==2.21.0",
                "tornado==5.1.1",
                "PyYAML==3.13",
                "Cerberus==1.2"
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

