import pytest

def test_phrase_length():
    phrase = input("Set a phrase: ")

    assert len(phrase) < 15, f"The phrase entered is longer than 15 characters: '{phrase}'"
    print(f"The length of the phrase entered is {len(phrase)}")
