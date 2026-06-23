# SPDX-License-Identifier: AGPL-3.0-or-later
"""Installer for SearXNG package."""

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]

with open('requirements-dev.txt') as f:
    dev_requirements = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]

setup(
    name='searxng',
    description="SearXNG is a metasearch engine. Users are neither tracked nor profiled.",
    long_description=long_description,
    license="AGPL-3.0-or-later",
    author='SearXNG',
    author_email='contact@searxng.org',
    python_requires=">=3.10",
    version="1.0.0",
    keywords='metasearch searchengine search web http',
    url="https://docs.searxng.org",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    project_urls={"Code": "https://github.com/searxng/searxng", "Issue tracker": "https://github.com/searxng/searxng/issues"},
    entry_points={
        'console_scripts': ['searxng-run = searx.webapp:run']
    },
    packages=find_packages(
        include=[
            'searx',
            'searx.*',
            'searx.*.*',
            'searx.*.*.*',
        ]
    ),
    package_data={
        'searx': [
            'settings.yml',
            '*.toml',
            '*.msg',
            'data/*.json',
            'data/*.txt',
            'data/*.ftz',
            'favicons/*.toml',
            'infopage/**',
            'static/**',
            'templates/**',
            'translations/**',
        ],
    },
    install_requires=requirements,
    extras_require={'test': dev_requirements},
)

