import argparse
import sys

import questionary

from .core import binary_to_ipv4, ipv4_to_binary


def main() -> int:
    parser = argparse.ArgumentParser(prog="ipv4-conversions")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d",
        "--to-decimal",
        dest="to_decimal",
        nargs="+",
        metavar="BINARY",
        type=str,
        help="Convert a binary IPv4 address to dotted-decimal notation",
    )
    group.add_argument(
        "-b",
        "--to-binary",
        dest="to_binary",
        nargs="+",
        metavar="DECIMAL",
        type=str,
        help="Convert a dotted-decimal IPv4 address to binary",
    )
    parser.add_argument("-s", "--short", action="store_true")

    args = parser.parse_args()

    if args.to_decimal is not None:
        for ip in args.to_decimal:
            try:
                result = binary_to_ipv4(ip)
            except ValueError as e:
                parser.error(str(e))
            if not args.short:
                print(f"The dotted-decimal equivalent of {ip} is: {result}")
            else:
                print(result)
    elif args.to_binary is not None:
        for ip in args.to_binary:
            try:
                result = ipv4_to_binary(ip)
            except ValueError as e:
                parser.error(str(e))
            if not args.short:
                print(f"The binary equivalent of {ip} is: {result}")
            else:
                print(result)
    else:
        conversion = questionary.select(
            "Which conversion do you want to perform?",
            choices=[
                "Binary address to dotted decimal",
                "Dotted decimal to binary address",
                "Exit",
            ],
        ).ask()

        match conversion:
            case "Binary address to dotted decimal":
                while True:
                    try:
                        binary = input(
                            "Insert four dotted 8-bit binary octets: "
                        ).strip()
                        print(
                            f"The dotted-decimal equivalent of {binary} is: "
                            f"{binary_to_ipv4(binary)}"
                        )
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                    else:
                        break
            case "Dotted decimal to binary address":
                while True:
                    try:
                        ipv4 = input("Insert a dotted-decimal IPv4 address: ").strip()
                        print(
                            f"The binary address equivalent of {ipv4} is: "
                            f"{ipv4_to_binary(ipv4)}"
                        )
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                    else:
                        break
            case "Exit":
                sys.exit("Program terminated")
    return 0


if __name__ == "__main__":
    main()
