import kalja


def test_public_api() -> None:
    assert callable(kalja.mutate)
    assert callable(kalja.keyboard_error)
    assert callable(kalja.transpose_chars)
    assert callable(kalja.drop_chars)
    assert callable(kalja.repeat_chars)
    assert callable(kalja.mutate_spacing)
    assert callable(kalja.mutate_casing)
    assert callable(kalja.mutate_punctuation)

    assert kalja.Mutator is not None
