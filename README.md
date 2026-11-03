# IPv4 Conversions

`ipv4-conversions` converts an IPv4 address between dotted-decimal notation and four dotted 8-bit binary octets. It is available as a Python library, a command-line tool, and an interactive prompt.

## Requirements

- Python 3.10 or newer
- [`bin-dec-conversions`](https://pypi.org/project/bin-dec-conversions/), which supplies the binary/decimal conversions for each octet
- [`questionary`](https://pypi.org/project/questionary/), used by the interactive prompt

## Installation

```bash
pip install .
```

## Library usage

```python
from ipv4_conversions import binary_to_ipv4, ipv4_to_binary

ipv4_to_binary("192.168.1.1")
# "11000000.10101000.00000001.00000001"

binary_to_ipv4("11000000.10101000.00000001.00000001")
# "192.168.1.1"
```

Both functions require exactly four octets. Decimal octets must be in the range `0` to `255`; binary octets must each contain exactly eight `0` or `1` characters. Invalid input raises `ValueError`.

| Function | Description |
| --- | --- |
| `ipv4_to_binary(ipv4: str) -> str` | Converts dotted-decimal IPv4 notation to four zero-padded, dotted binary octets. |
| `binary_to_ipv4(binary: str) -> str` | Converts four dotted 8-bit binary octets to dotted-decimal IPv4 notation. |

## Command line

```bash
# Binary address to dotted decimal
ipv4-conversions --to-decimal 11000000.10101000.00000001.00000001
# The dotted-decimal equivalent of ... is: 192.168.1.1

# Dotted decimal to binary address
ipv4-conversions --to-binary 192.168.1.1
# The binary equivalent of 192.168.1.1 is: 11000000.10101000.00000001.00000001
```

The short options are `-d` for `--to-decimal` and `-b` for `--to-binary`. The options are mutually exclusive.

For each option, you can insert one or more addresses, and the program will output multiple conversions. For example:

```bash
ipv4-conversions --to-binary 192.168.0.0 192.168.1.0
# The binary equivalent of 192.168.0.0 is: 11000000.10101000.00000000.00000000
# The binary equivalent of 192.168.1.0 is: 11000000.10101000.00000001.00000000
```

Also, you can shorten the output to the sole result with '-s' or '--short' flag:
```bash
ipv4-conversions --to-binary 192.168.0.1 --short
# 11000000.10101000.00000000.00000001
```

Running `ipv4-conversions` without options opens the interactive menu.

## Interactive menu

Run the command without any options to open the interactive menu:

```bash
ipv4-conversions
```

Choose **Binary address to dotted decimal** or **Dotted decimal to binary address**, then enter the address when prompted. Choose **Exit** to quit.

## Development

You can install development tools, such as pytest and ruff, using this command: 

```bash
pip install -e ".[dev]"
```

### Test suite

The pytest suite covers valid conversions in both directions, round-trip conversions, and invalid IPv4 and binary input. Run it from the project root with:

```bash
python3 -m pytest
```

## Project structure

```
ipv4_conversions/
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   └── ipv4_conversions/
│       ├── __init__.py
│       ├── cli.py
│       └── core.py
└── tests/
    ├── test_conversions.py
    └── test_invalid.py
```

## License

Released under the MIT License. See [LICENSE](LICENSE).
