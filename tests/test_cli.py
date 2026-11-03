import sys

import pytest
import questionary

from ipv4_conversions.cli import main


# command-line prompts with flags
def test_verbose_result(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["ipv4-conversions", "--to-decimal", "11000000.10101000.00000000.00000001"],
    )
    assert main() == 0
    assert (
        "The dotted-decimal equivalent of 11000000.10101000.00000000.00000001 is: 192.168.0.1"
    ) in capsys.readouterr().out

    monkeypatch.setattr(sys, "argv", ["ipv4-conversions", "--to-binary", "192.168.0.1"])
    assert main() == 0
    assert (
        "The binary equivalent of 192.168.0.1 is: 11000000.10101000.00000000.00000001"
        in capsys.readouterr().out
    )


def test_short_result(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ipv4-conversions",
            "--to-decimal",
            "11000000.10101000.00000000.00000001",
            "--short",
        ],
    )
    assert main() == 0
    assert "192.168.0.1" in capsys.readouterr().out

    monkeypatch.setattr(
        sys, "argv", ["ipv4-conversions", "--to-binary", "192.168.0.1", "--short"]
    )
    assert main() == 0
    assert "11000000.10101000.00000000.00000001" in capsys.readouterr().out


def test_multiple_addresses(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["ipv4-conversions", "--to-binary", "192.168.0.1", "192.168.1.0"],
    )
    assert main() == 0
    assert capsys.readouterr().out == (
        "The binary equivalent of 192.168.0.1 is: "
        "11000000.10101000.00000000.00000001\n"
        "The binary equivalent of 192.168.1.0 is: "
        "11000000.10101000.00000001.00000000\n"
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ipv4-conversions",
            "--to-decimal",
            "11000000.10101000.00000000.00000001",
            "11000000.10101000.00000001.00000000",
        ],
    )
    assert main() == 0
    assert capsys.readouterr().out == (
        "The dotted-decimal equivalent of "
        "11000000.10101000.00000000.00000001 is: 192.168.0.1\n"
        "The dotted-decimal equivalent of "
        "11000000.10101000.00000001.00000000 is: 192.168.1.0\n"
    )


def test_multiple_addresses_short_output(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ipv4-conversions",
            "--to-binary",
            "192.168.0.1",
            "192.168.1.0",
            "--short",
        ],
    )
    assert main() == 0
    assert capsys.readouterr().out == (
        "11000000.10101000.00000000.00000001\n11000000.10101000.00000001.00000000\n"
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ipv4-conversions",
            "--to-decimal",
            "11000000.10101000.00000000.00000001",
            "11000000.10101000.00000001.00000000",
            "--short",
        ],
    )
    assert main() == 0
    assert capsys.readouterr().out == "192.168.0.1\n192.168.1.0\n"


@pytest.mark.parametrize(
    "option, address, expected_error",
    [
        ("--to-binary", "", "empty"),
        ("--to-binary", "192.168.1", "four decimal octets"),
        ("--to-binary", "192.168.1.256", "outside the range 0-255"),
        ("--to-binary", "192.168.a.1", "not a decimal octet"),
        ("--to-decimal", "", "empty"),
        (
            "--to-decimal",
            "11000000.10101000.00000001",
            "four 8-bit binary octets",
        ),
        (
            "--to-decimal",
            "1100000.10101000.00000001.00000001",
            "exactly 8 bits",
        ),
        (
            "--to-decimal",
            "11000000.10101000.0000000a.00000001",
            "invalid character",
        ),
    ],
)

# invalid prompts
def test_invalid_address_exits_with_argument_error(
    monkeypatch, capsys, option, address, expected_error
):
    monkeypatch.setattr(sys, "argv", ["ipv4-conversions", option, address])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert expected_error in captured.err
    assert captured.out == ""


@pytest.mark.parametrize("option", ["--to-decimal", "-d", "--to-binary", "-b"])
def test_conversion_option_requires_an_address(monkeypatch, capsys, option):
    monkeypatch.setattr(sys, "argv", ["ipv4-conversions", option])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2
    assert "expected at least one argument" in capsys.readouterr().err


@pytest.mark.parametrize(
    "decimal_option, binary_option",
    [
        ("--to-decimal", "--to-binary"),
        ("--to-decimal", "-b"),
        ("-d", "--to-binary"),
        ("-d", "-b"),
    ],
)
def test_rejects_both_conversion_options(
    monkeypatch, capsys, decimal_option, binary_option
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ipv4-conversions",
            decimal_option,
            "11000000.10101000.00000000.00000001",
            binary_option,
            "192.168.0.1",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2
    assert "not allowed with argument" in capsys.readouterr().err


# interactive menu
class FakeQuestion:
    def __init__(self, answer):
        self.answer = answer

    def ask(self, *args, **kwargs):
        return self.answer


def test_interactive_menu_to_binary(monkeypatch, capsys):
    calls = []
    answers = iter(["192.168.1.256", "192.168.0.1"])

    def fake_input(prompt=""):
        calls.append(prompt)
        return next(answers)

    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr(
        questionary,
        "select",
        lambda *a, **kw: FakeQuestion("Dotted decimal to binary address"),
    )
    monkeypatch.setattr(sys, "argv", ["ipv4-conversions"])

    assert main() == 0

    out = capsys.readouterr().out
    assert "outside the range 0-255" in out
    assert "11000000.10101000.00000000.00000001" in out
    assert len(calls) == 2


def test_interactive_menu_to_decimal(monkeypatch, capsys):
    calls = []
    answers = iter(
        ["11000000.10101000.00000001.111111111", "11000000.10101000.00000000.00000001"]
    )

    def fake_input(prompt=""):
        calls.append(prompt)
        return next(answers)

    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr(
        questionary,
        "select",
        lambda *a, **kw: FakeQuestion("Binary address to dotted decimal"),
    )
    monkeypatch.setattr(sys, "argv", ["ipv4-conversions"])

    assert main() == 0

    out = capsys.readouterr().out
    assert "exactly 8 bits" in out
    assert "192.168.0.1" in out
