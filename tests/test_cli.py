import io
import sys

import pytest

from kalja.cli import main


def test_cli_mutates_text_argument(
    capsys,
) -> None:
    exit_code = main(
        [
            "--intensity",
            "0",
            "Missä te olette?",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Missä te olette?\n"


def test_cli_generates_multiple_variants(
    capsys,
) -> None:
    exit_code = main(
        [
            "--count",
            "3",
            "--intensity",
            "0",
            "kalja",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "kalja\nkalja\nkalja\n"


def test_cli_reads_from_stdin(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(
        sys,
        "stdin",
        io.StringIO("Missä te olette?"),
    )

    exit_code = main(["--intensity", "0"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "Missä te olette?\n"


def test_cli_rejects_invalid_intensity() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "--intensity",
                "1.5",
                "kalja",
            ]
        )

    assert exc_info.value.code == 2


def test_cli_rejects_negative_count() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "--count",
                "-1",
                "kalja",
            ]
        )

    assert exc_info.value.code == 2


def test_cli_accepts_minimum_intensity(capsys) -> None:
    assert main(["--intensity", "0", "kalja"]) == 0
    assert capsys.readouterr().out == "kalja\n"


def test_cli_accepts_maximum_intensity() -> None:
    assert main(["--intensity", "1", "--seed", "42", "kalja"]) == 0


def test_cli_rejects_intensity_above_one() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--intensity", "1.01", "kalja"])

    assert exc_info.value.code == 2


def test_cli_rejects_zero_count() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--count", "0", "kalja"])

    assert exc_info.value.code == 2


def test_cli_accepts_finnish_layout(capsys) -> None:
    exit_code = main(
        [
            "--layout",
            "fi",
            "--intensity",
            "0",
            "kalja",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "kalja\n"


def test_cli_accepts_us_layout(capsys) -> None:
    exit_code = main(
        [
            "--layout",
            "us",
            "--intensity",
            "0",
            "hello",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "hello\n"


def test_cli_rejects_unknown_layout() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "--layout",
                "de",
                "hello",
            ]
        )

    assert exc_info.value.code == 2
