from setuptools import setup, find_packages

with open('README.rst') as f:
    readme  =  f.read()

setup(
    name = "mvmv",
    version = "1.1",

    author = "William Mak, Prajjwal Bhandari, Matt Olan",
    author_email = "william@wmak.io, pbhandari@pbhandari.ca, hello@olanmatt.com",
    url = "https://github.com/wmak/mvmv",

    description = "Movie Mover - move your movies where they belong.",
    long_description = readme,
    license = 'MIT',

    packages = find_packages(exclude=['*.tests']),
    test_suite = "mvmv.tests",
    entry_points={
        "console_scripts": [
            "mvmv = mvmv.cli:main"
        ],
    },
    install_requires = [
        "fuzzywuzzy >= 0.4.0",
        "python-Levenshtein >= 0.11.2",
        "watchdog >= 0.8.2",
    ],
)
