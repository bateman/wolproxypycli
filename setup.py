"""Setup configuration for the 'wolproxypycli' package.

The 'wolproxypycli' package is a PyPI module and Typer (CLI) app for sending Wake-On-LAN packets.
"""

from setuptools import find_packages, setup

setup(
    name="wolproxypycli",
    version="0.1.6",
    description="A PyPI module and Typer (CLI) app for sending Wake-On-LAN packets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Fabio Calefato",
    author_email="fabio.calefato@uniba.it",
    url="https://github.com/bateman/wolproxypycli",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
