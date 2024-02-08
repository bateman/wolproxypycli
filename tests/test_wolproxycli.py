"""Unit tests for the core module."""

import socket
from unittest.mock import Mock, call, patch

import pytest

import wolproxypycli
from wolproxypycli.main import STATUS_FAIL, STATUS_OK, wol


def generate_magic_packet(mac_address):
    """Generate a magic packet for the given MAC address."""
    mac_address_bytes = bytes.fromhex("".join(mac_address.split(":")))
    return b"\xff" * 6 + mac_address_bytes * 16


@pytest.mark.parametrize(
    "mac,packet",
    [
        ("000000000000", generate_magic_packet("00:00:00:00:00:00")),
        ("01:23:45:67:89:ab", generate_magic_packet("01:23:45:67:89:ab")),
        ("ff-ff-ff-ff-ff-ff", generate_magic_packet("ff:ff:ff:ff:ff:ff")),
    ],
    ids=["no separator", "colons", "hyphens"],
)
@patch("socket.socket")
def test_wol(sock: Mock, mac, packet) -> None:
    """Test whether the magic packets are broadcasted to the specified network."""
    wolproxypycli.main.wol(mac, ip="example.com", port=7)
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().__enter__(),
        call().__enter__().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().__enter__().connect(("example.com", 7)),
        call().__enter__().send(packet),
        call().__exit__(None, None, None),
    ]


@patch("socket.socket")
def test_wol_default(sock: Mock) -> None:
    """Test whether the magic packets are broadcasted using default values."""
    mac = "133713371337"
    packet = generate_magic_packet(mac)
    wolproxypycli.main.wol(mac)
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().__enter__(),
        call().__enter__().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().__enter__().connect(("255.255.255.255", 9)),
        call().__enter__().send(packet),
        call().__exit__(None, None, None),
    ]


@patch("socket.socket")
def test_wol_interface(sock: Mock) -> None:
    """Test whether the magic packets are broadcasted to the specified network via specified interface."""
    mac = "133713371337"
    packet = generate_magic_packet(mac)
    wolproxypycli.main.wol(mac, ip="example.com", port=7, interface="192.168.0.2")
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().__enter__(),
        call().__enter__().bind(("192.168.0.2", 0)),
        call().__enter__().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().__enter__().connect(("example.com", 7)),
        call().__enter__().send(packet),
        call().__exit__(None, None, None),
    ]


@patch("wolproxypycli.main.wolproxy_cli")
def test_main(wol: Mock) -> None:
    """Test if processed arguments are passed to send_magic_packet."""
    wolproxypycli.main.wolproxy_cli(["00:11:22:33:44:55"])
    wolproxypycli.main.wolproxy_cli(["00:11:22:33:44:55", "-i", "", "-p", ""])
    wolproxypycli.main.wolproxy_cli(["00:11:22:33:44:55", "-i", "host.example", "-p", "1337"])
    wolproxypycli.main.wolproxy_cli(["00:11:22:33:44:55", "-i", "host.example", "-p", "1337", "-n", "192.168.0.2"])
    assert wol.mock_calls == [
        call(["00:11:22:33:44:55"]),
        call(["00:11:22:33:44:55", "-i", "", "-p", ""]),
        call(["00:11:22:33:44:55", "-i", "host.example", "-p", "1337"]),
        call(["00:11:22:33:44:55", "-i", "host.example", "-p", "1337", "-n", "192.168.0.2"]),
    ]


@patch("wolproxypycli.main.wakeonlan.send_magic_packet")
def test_wol_success(mock_send_magic_packet):
    """Test successful wake on lan."""
    mac = "AA:BB:CC:DD:EE:FF"
    ip = "192.168.0.1"
    port = 9
    interface = "192.168.0.2"
    assert wol(mac, ip, port, interface) == STATUS_OK
    mock_send_magic_packet.assert_called_once_with(mac, ip_address=ip, port=port, interface=interface)


@patch("wolproxypycli.main.wakeonlan.send_magic_packet")
def test_wol_failure(mock_send_magic_packet):
    """Test failed wake on lan."""
    mock_send_magic_packet.side_effect = Exception("Test exception")
    assert wol("AA:BB:CC:DD:EE:FF") == STATUS_FAIL
