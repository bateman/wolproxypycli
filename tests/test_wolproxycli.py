"""Unit tests for the core module."""

import socket
from unittest.mock import Mock, call, patch

import pytest

import wolproxypycli.main as wolproxy


@pytest.mark.parametrize(
    "mac,packet",
    [
        (
            "000000000000",
            b"\xff\xff\xff\xff\xff\xff"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00",
        ),
        (
            "01:23:45:67:89:ab",
            b"\xff\xff\xff\xff\xff\xff"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab",
        ),
        (
            "ff-ff-ff-ff-ff-ff",
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff",
        ),
    ],
    ids=["no separator", "colons", "hyphens"],
)
@patch("socket.socket")
def test_wol(sock: Mock) -> None:
    """Test whether the magic packets are broadcasted to the specified network."""
    wolproxy.wol("133713371337", ip="example.com", port=7)
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().__enter__(),
        call().__enter__().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().__enter__().connect(("example.com", 7)),
        call()
        .__enter__()
        .send(
            b"\xff\xff\xff\xff\xff\xff"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
        ),
        call().__exit__(None, None, None),
    ]


@patch("socket.socket")
def test_wol_default(sock: Mock) -> None:
    """Test whether the magic packets are broadcasted using default values."""
    wolproxy.wol("133713371337")
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().__enter__(),
        call().__enter__().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().__enter__().connect(("255.255.255.255", 9)),
        call()
        .__enter__()
        .send(
            b"\xff\xff\xff\xff\xff\xff"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
        ),
        call().__exit__(None, None, None),
    ]


@patch("socket.socket")
def test_wol_interface(sock: Mock) -> None:
    """Test whether the magic packets are broadcasted to the specified network via specified interface."""
    wolproxy.wol(
        "133713371337",
        ip="example.com",
        port=7,
        interface="192.168.0.2",
    )
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().__enter__(),
        call().__enter__().bind(("192.168.0.2", 0)),
        call().__enter__().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().__enter__().connect(("example.com", 7)),
        call()
        .__enter__()
        .send(
            b"\xff\xff\xff\xff\xff\xff"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
        ),
        call().__exit__(None, None, None),
    ]


@patch("wolproxy_py.main.wol")
def test_main(wol: Mock) -> None:
    """Test if processed arguments are passed to send_magic_packet."""
    wolproxy.wolproxy_cli(["00:11:22:33:44:55", "-i", "host.example", "-p", "1337"])
    wolproxy.wolproxy_cli(["00:11:22:33:44:55", "-i", "host.example", "-p", "1337", "-n", "192.168.0.2"])
    assert wol.mock_calls == [
        call("00:11:22:33:44:55", ip="host.example", port=1337, interface=None),
        call(
            "00:11:22:33:44:55",
            ip="host.example",
            port=1337,
            interface="192.168.0.2",
        ),
    ]
