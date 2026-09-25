import argparse
import sys
from collections.abc import Sequence

from .keyboards import FI_DESKTOP, US_DESKTOP, KeyboardLayout
from .mutator import mutate, variants

_LAYOUTS: dict[str, KeyboardLayout] = {
    "fi": FI_DESKTOP,
    "us": US_DESKTOP,
}


def _positive_int(value: str) -> int:
    parsed = int(value)

    if parsed < 1:
        raise argparse.ArgumentTypeError("must be greater than or equal to 1")

    return parsed


def _intensity(value: str) -> float:
    parsed = float(value)

    if not 0.0 <= parsed <= 1.0:
        raise argparse.ArgumentTypeError("must be between 0.0 and 1.0")

    return parsed


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kalja",
        description="Finnish-focused text mutation and human-input fuzzing.",
    )

    parser.add_argument(
        "text",
        nargs="?",
        help="Text to mutate. Reads from stdin when omitted.",
    )
    parser.add_argument(
        "-l",
        "--layout",
        choices=_LAYOUTS,
        default="fi",
        help="Keyboard layout for keyboard errors (default: fi).",
    )
    parser.add_argument(
        "-i",
        "--intensity",
        type=_intensity,
        default=0.5,
        help="Mutation intensity from 0.0 to 1.0 (default: 0.5).",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible output.",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=_positive_int,
        default=1,
        help="Number of variants to generate (default: 1).",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    text = args.text
    layout = _LAYOUTS[args.layout]

    if text is None:
        text = sys.stdin.read()

    try:
        if args.count == 1:
            print(
                mutate(
                    text,
                    intensity=args.intensity,
                    layout=layout,
                    seed=args.seed,
                )
            )
        else:
            results = variants(
                text,
                count=args.count,
                intensity=args.intensity,
                layout=layout,
                seed=args.seed,
            )

            for result in results:
                print(result)

    except ValueError as exc:
        parser.error(str(exc))

    return 0
