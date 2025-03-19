from setuptools import setup, find_packages

setup(
    name="html2gfm",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
    ],
    author="SREENATH KUMAR MOPURI",
    description="A library to convert HTML to GitHub Flavored Markdown",
    license="Apache",
)
