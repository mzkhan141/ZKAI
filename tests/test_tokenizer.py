"""Unit tests for Tokenizer subsystem."""

import pytest
from zkai.tokenizer import (
    BytePairTokenizer,
    CharacterTokenizer,
    FastTokenizer,
    RegexTokenizer,
    SentencePieceTokenizer,
    StreamingTokenizer,
    UnicodeNormalizer,
    UnigramTokenizer,
    Vocabulary,
    WhitespaceTokenizer,
    WordPieceTokenizer,
)


def test_bpe_tokenizer():
    tok = BytePairTokenizer(vocab_size=100)
    tok.train(["hello world hello zkai", "natural language processing"])
    enc = tok.encode("hello zkai")
    assert len(enc.ids) > 0
    dec = tok.decode(enc.ids)
    assert isinstance(dec, str)


def test_character_tokenizer():
    tok = CharacterTokenizer()
    tok.train(["abc def"])
    enc = tok.encode("abc")
    assert len(enc.ids) == 5  # bos + a + b + c + eos


def test_whitespace_tokenizer():
    tok = WhitespaceTokenizer()
    tok.train(["one two three"])
    enc = tok.encode("one two")
    assert len(enc.tokens) == 4  # bos + one + two + eos


def test_regex_tokenizer():
    tok = RegexTokenizer()
    tok.train(["word1 word2 123"])
    enc = tok.encode("word1")
    assert len(enc.ids) > 0


def test_streaming_tokenizer():
    st = StreamingTokenizer()
    res1 = st.feed("hello ")
    res2 = st.feed("world ")
    res3 = st.flush()
    assert isinstance(res1, list)
    assert isinstance(res2, list)
    assert isinstance(res3, list)
