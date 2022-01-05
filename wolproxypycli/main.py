"""The main module of the wolproxypy application."""

import wakeonlan
from typer import Typer

from config import logger

wolproxy_cli = Typer()

STATUS_OK = "success"
STATUS_FAIL = "failure"


@wolproxy_cli.command()
def wol(
    mac: str,
    ip: str = wakeonlan.BROADCAST_IP,
    port: int = wakeonlan.DEFAULT_PORT,
    interface: str = None,
) -> str:
    """Wake up computers having any of the given mac addresses.

    Wake on lan must be enabled on the host device. Leverages the PyPy package wakeonlan.

    Args:
        mac: One or more mac addresses of machines to wake. Acceptable formats
            are: 'AA:BB:CC:DD:EE:FF' or 'AA-BB-CC-DD-EE-FF' or 'AABBCCDDEEFF' or 'AABBCC.DDEEFF'.
    Keyword Args:
        ip: the ip address of the host to send the magic packet to.
        port: the port of the host to send the magic packet to.
        interface: the ip address of the network adapter to route the magic packet through.

    Returns:
        status: "success" if the magic packet was sent successfully; "failure" otherwise.
    """
    logger.info("Sending WOL magic packet to address %s", mac)
    if ip is None or ip == "":
        ip = "255.255.255.255"
    if port is None or port <= 0 or port > 65535:
        port = 9
    try:
        wakeonlan.send_magic_packet(*(mac,), ip_address=ip, port=port, interface=interface)
        status = STATUS_OK
    except Exception as ex:
        logger.error(ex)
        status = STATUS_FAIL
    return status


def run() -> None:
    """Run wake on lan as a CLI application."""
    wolproxy_cli()


if __name__ == "__main__":
    run()
