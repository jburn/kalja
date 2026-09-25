import argparse
import sys
from collections.abc import Sequence

from .mutator import mutate, variants


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
        "-i",
        "--intensity",
        type=float,
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
        type=int,
        default=1,
        help="Number of variants to generate (default: 1).",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    text = args.text

    if text is None:
        text = sys.stdin.read()

    try:
        if args.count == 1:
            print(
                mutate(
                    text,
                    intensity=args.intensity,
                    seed=args.seed,
                )
            )
        else:
            results = variants(
                text,
                count=args.count,
                intensity=args.intensity,
                seed=args.seed,
            )

            for result in results:
                print(result)

    except ValueError as exc:
        parser.error(str(exc))

    return 0
