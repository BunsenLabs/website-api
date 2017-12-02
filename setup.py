#!/usr/bin/env python3

from setuptools import setup

setup(
        name = "bunsenlabs_website_api_services",
        version = "1.0.0",
        scripts = [
                "tracker_status.py",
                "news_server.py",
        ],
        install_requires = [
                "bottle",
                "beautifulsoup4",
                "Django",
                "feedparser",
                "requests",
        ],
        include_package_data = True,

        author = "Jens John",
        author_email = "dev@2ion.de",
        description = "BunsenLabs Website API Services",
        license = "GPL3",
        keywords = "bunsenlabs service website",
        url = "https://github.com/bunsenlabs/bunsen-website"
)

