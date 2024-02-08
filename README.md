# wolproxypycli
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wolproxypycli)
![GitHub](https://img.shields.io/github/license/bateman/wolproxypycli)

[![pypi](https://github.com/bateman/wolproxypycli/actions/workflows/publish.yml/badge.svg)](https://github.com/bateman/wolproxypycli/actions/workflows/publish.yml)
[![Documentation Status](https://readthedocs.org/projects/wolproxypycli/badge/?version=latest)](https://wolproxypycli.readthedocs.io/en/latest/?badge=latest)


![PyPI](https://img.shields.io/pypi/v/wolproxypycli)
![PyPI - Format](https://img.shields.io/pypi/format/wolproxypycli)
![PyPI - Downloads](https://img.shields.io/pypi/dm/wolproxypycli)


[![Known Vulnerabilities](https://snyk.io/test/github/bateman/wolproxypycli/badge.svg)](https://snyk.io/test/github/bateman/wolproxypycli)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/bateman/wolproxypycli)

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

A PyPI module and Typer (CLI) app for sending Wake-On-LAN packets

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. To install the project, first install Poetry, then run the following command in the project root directory:

```bash
poetry install
```

or

```bash
make install
```

## Development installation
To install the package with all development dependencies, run:

```bash
make install-dev
```


## Usage

Wake on lan must be enabled on the target host device before usage.

For more details, check the [documentation](https://wolproxypycli.readthedocs.io/en/latest).

### Command line

This tool is typically used to send a Wake-on-LAN packet to a device on your network. The `<MAC>` argument should be replaced with the MAC address of the device you want to wake up.

Here's an example:

```bash
poetry run wolproxypycli 00:11:22:33:44:55
```

To see the full list of options, run:

```bash
poetry run wolproxypycli --help
```

```
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────╮
│ * mac                 TEXT     [default: None] [required]                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────╮
│ --ip                  TEXT     [default: 255.255.255.255]                                              │
│ --port                INTEGER  [default: 9]                                                            │
│ --interface           TEXT     [default: None]                                                         │
│ --install-completion  Install completion for the current shell.                                        │
│ --show-completion     Show completion for the current shell, to copy it or customize the installation. │
│ --help                Show this message and exit.                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Module

First, make sure to install the module via `poetry`:

```bash
poetry add wolproxypycli
```

or `pip`:

```bash
pip install wolproxypycli
```

Here's a basic example of how to use `wolproxypycli`:

```python
from wolproxypycli import wol
...

wol.send(mac="AA:BB:CC:DD:EE:FF")
```

## License

This project is licensed under the terms of the [MIT License](LICENSE).
