# KALJA

KALJA is a small, dependency-free Python library for text mutation and human-input fuzzing.

It generates deliberately imperfect text for testing systems such as search, fuzzy matching, forms, parsers, typo correction, normalization, and NLP pipelines.

KALJA provides Finnish-focused defaults, including a Finnish desktop keyboard layout, while also supporting US QWERTY and custom keyboard layouts.

## Installation

```bash
pip install kalja
```

KALJA requires Python 3.10 or later.

## Quick start

```python
import kalja

result = kalja.mutate(
    "Missä te olette?",
    intensity=0.5,
    seed=42,
)

print(result)
```

`mutate()` applies a combination of supported mutation operations to the input text.

Providing a seed makes the result reproducible:

```python
first = kalja.mutate(
    "Missä te olette?",
    intensity=0.7,
    seed=42,
)

second = kalja.mutate(
    "Missä te olette?",
    intensity=0.7,
    seed=42,
)

assert first == second
```

## Generating variants

Use `variants()` to generate multiple mutated versions of the same input:

```python
import kalja

results = kalja.variants(
    "Voinko varata ajan huomiselle?",
    count=10,
    intensity=0.7,
    seed=42,
)

for result in results:
    print(result)
```

`count` controls the number of generated results.

Variants are not guaranteed to be unique. At low intensities or with short inputs, multiple mutation passes may produce the same output.

## Mutation intensity

The high-level `mutate()` and `variants()` APIs use an `intensity` value between `0.0` and `1.0`.

```python
kalja.mutate(text, intensity=0.0)
kalja.mutate(text, intensity=0.5)
kalja.mutate(text, intensity=1.0)
```

Intensity is a **relative fuzzing level**, not a direct probability.

Internally, KALJA scales the configured mutation rates:

```text
effective rate = maximum rate × intensity
```

This means `intensity=1.0` enables KALJA's full configured mutation rates. It does not mean that every character will be mutated.

At `intensity=0.0`, all mutation rates are zero and the original text is returned unchanged.

## Keyboard layouts

KALJA includes Finnish and US desktop keyboard layouts.

Finnish desktop is the default:

```python
import kalja

result = kalja.mutate(
    "Missä te olette?",
    layout=kalja.FI_DESKTOP,
    seed=42,
)
```

US QWERTY can be selected explicitly:

```python
result = kalja.mutate(
    "Where are you?",
    layout=kalja.US_DESKTOP,
    seed=42,
)
```

Keyboard-error mutations use physical key positions to select nearby keys.

The included layouts are:

- `kalja.FI_DESKTOP` — Finnish desktop QWERTY
- `kalja.US_DESKTOP` — US desktop QWERTY

Keyboard coordinates are approximate and are intended for neighboring-key mutation rather than exact physical keyboard simulation.

## Low-level mutations

KALJA also exposes individual mutation operations when precise control is needed.

### Keyboard errors

Replace characters with neighboring keys:

```python
result = kalja.keyboard_error(
    "Oulu 90100",
    rate=0.1,
    seed=42,
)
```

A different layout can be supplied:

```python
result = kalja.keyboard_error(
    "hello world",
    rate=0.1,
    layout=kalja.US_DESKTOP,
    seed=42,
)
```

### Character transposition

Randomly swap adjacent characters:

```python
result = kalja.transpose_chars(
    "kalja",
    rate=0.05,
    seed=42,
)
```

### Character omission

Randomly remove characters:

```python
result = kalja.drop_chars(
    "kalja",
    rate=0.02,
    seed=42,
)
```

### Character repetition

Randomly duplicate characters:

```python
result = kalja.repeat_chars(
    "kalja",
    rate=0.02,
    seed=42,
)
```

### Spacing

Randomly remove existing spaces or insert new spaces:

```python
result = kalja.mutate_spacing(
    "Missä te olette?",
    rate=0.02,
    seed=42,
)
```

### Casing

Randomly flip the case of characters with distinct upper- and lowercase forms:

```python
result = kalja.mutate_casing(
    "Olen Oulussa",
    rate=0.02,
    seed=42,
)
```

### Punctuation

Randomly omit or duplicate existing punctuation:

```python
result = kalja.mutate_punctuation(
    "Missä olet?",
    rate=0.02,
    seed=42,
)
```

## Rates

Low-level mutation functions use `rate` rather than `intensity`.

A rate is the probability associated with that specific mutation operation:

```python
kalja.drop_chars(
    "abcdef",
    rate=0.1,
    seed=42,
)
```

Here, each character has a `0.1` probability of being dropped.

This differs from the high-level `intensity` parameter, which scales several mutation rates at once.

## Configurable mutator

For more control, use `Mutator` directly:

```python
import kalja

mutator = kalja.Mutator(
    keyboard_error_rate=0.08,
    transposition_rate=0.04,
    omission_rate=0.02,
    repetition_rate=0.03,
    spacing_rate=0.02,
    casing_rate=0.01,
    punctuation_rate=0.02,
    layout=kalja.FI_DESKTOP,
    seed=42,
)

result = mutator.mutate("Olen täysin kunnossa.")
```

A `Mutator` owns its own pseudorandom number generator.

Repeated calls advance that generator:

```python
first = mutator.mutate("Missä te olette?")
second = mutator.mutate("Missä te olette?")
```

The two results may differ.

Recreating a `Mutator` with the same configuration and seed reproduces the same sequence of results.

KALJA does not modify Python's process-global `random` state.

## Command-line interface

KALJA includes a command-line interface.

Mutate text directly:

```bash
kalja "Missä te olette?"
```

Control mutation intensity:

```bash
kalja --intensity 0.7 "Missä te olette?"
```

Use a seed for reproducible output:

```bash
kalja --intensity 0.7 --seed 42 "Missä te olette?"
```

Generate multiple variants:

```bash
kalja --count 5 --intensity 0.7 --seed 42 "Missä te olette?"
```

Select the US keyboard layout:

```bash
kalja --layout us "Where are you?"
```

The Finnish layout is the default:

```bash
kalja --layout fi "Missä te olette?"
```

KALJA can also read text from standard input:

```bash
echo "Missä te olette?" | kalja --intensity 0.7 --seed 42
```

Run the built-in help for all options:

```bash
kalja --help
```

## Use cases

KALJA can be used to generate imperfect inputs for testing:

- search and autocomplete
- fuzzy matching
- typo-tolerant systems
- form handling
- text normalization
- parsers
- chat applications
- NLP pipelines
- validation logic
- test fixtures and fuzz tests

For example, a search system can be tested against several mutated versions of a query:

```python
import kalja

queries = kalja.variants(
    "ravintola oulu",
    count=20,
    intensity=0.6,
    seed=42,
)

for query in queries:
    test_search(query)
```

## Unicode and Finnish text

KALJA works with Python Unicode strings and supports Finnish characters such as:

```text
ä ö å Ä Ö Å
```

The Finnish desktop layout includes these characters when generating neighboring-key substitutions.

KALJA currently operates on Python string characters rather than Unicode grapheme clusters. Combining character sequences may therefore be treated as multiple mutation units.

## Limitations

KALJA is a mechanical text mutation and fuzzing library. It is not a linguistic model of how people make mistakes.

In particular:

- keyboard geometry is approximate
- Finnish and US desktop layouts are currently included
- AltGr combinations are not modeled
- dead-key composition is not modeled
- mobile keyboard geometry is not modeled
- Unicode grapheme clusters are not treated as atomic units
- generated mutations are not guaranteed to represent realistic human errors
- generated variants are not guaranteed to be unique

These constraints are intentional: KALJA aims to provide small, deterministic, understandable mutation primitives suitable for testing.

## Development

Install the development environment with `uv`:

```bash
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Check formatting:

```bash
uv run ruff format --check .
```

Run type checking:

```bash
uv run mypy src
```

Run coverage:

```bash
uv run pytest --cov=kalja --cov-report=term-missing
```

## License

KALJA is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later). See the LICENSE file for details.