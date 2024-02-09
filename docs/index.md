# wolproxypycli

This is a simple package for sending Wake-On-LAN packets to other host in a local network. This started as a pet-project to put together and test a series of technologies I'm interested in.
The all WOL packet sending is managed by the Python package [wakeonlan](https://pypi.org/project/wakeonlan/), for which wolproxypycli acts as a wrapper.

## Installation

### As a package

The wolproxypycli package is available on PyPI. You can choose either of the following option to install the dependency in your project:

* `poetry add wolproxypycli` - Install via poetry
* `pip install wolproxypycli` - Install via pip


### As a local project

1. `git clone https://github.com/bateman/wolproxypy` - Clone the project from GitHub.
2. `make install` - Install all dependencies via [poetry](https://python-poetry.org/).
3. `make docs` - Build the documentation site via [mkdocs](https://www.mkdocs.org/).

## Usage

### Programmatically

Once installed in your project, you can access it programmatically as follows:

```python
from wolproxypycli import wol

wol(macaddress)
```

Acceptable formats for supplying a mac address are:

- `AA:BB:CC:DD:EE:FF`
- `AA-BB-CC-DD-EE-FF`
- `AABBCCDDEEFF`
- `AABBCC.DDEEFF`

As optional parameters you can supply also:

- `ip` - the ip address of the host to send the magic packet to.
- `port` - the port of the host to send the magic packet to.
- `interface` the ip address of the network adapter to route the magic packet through.

Please, refer to the [module documentation](cli.md) for more.

### Command line

The following assumes that you cloned the image locally as described in the Installation step 1 above. You can run the tool from the command line as follows:

`poetry run wolproxypycli <MAC>`

The CLI has been built using [Typer](https://typer.tiangolo.com/), so the following command will give yout this pretty-printed help menu with all the arguments.

`poetry run wolproxypycli --help`

```
Usage: wolproxypycli [OPTIONS] MAC

  Wake up computers having any of the given mac addresses.

  Wake on lan must be enabled on the host device. Leverages the PyPy package
  wakeonlan.

  Args:     mac: One or more mac addresses of machines to wake.

  Keyword Args:     ip: the ip address of the host to send the magic packet
  to.     port: the port of the host to send the magic packet to.
  interface: the ip address of the network adapter to route the magic packet
  through.

  Returns:     status: "success" if the magic packet was sent successfully;
  "failure" otherwise.

Arguments:
  MAC  [required]

Options:
  --ip TEXT                       [default: 255.255.255.255]
  --port INTEGER                  [default: 9]
  --interface TEXT
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```
