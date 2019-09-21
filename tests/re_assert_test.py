import re

import pytest

from re_assert import Matches


def test_typeerror_equality_different_type():
    with pytest.raises(TypeError):
        Matches('foo') == b'foo'


def test_matches_repr_plain():
    assert repr(Matches('^foo')) == "Matches('^foo')"


def test_matches_repr_with_flags():
    ret = repr(Matches('^foo', re.I))
    assert ret == "Matches('^foo', flags=regex.I | regex.V0)"


def test_repr_with_failure():
    obj = Matches('^foo')
    assert obj != 'fa'
    assert repr(obj) == (
        "Matches('^foo')\n"
        '    # regex failed to match at:\n'
        '    #\n'
        '    #> fa\n'
        '    #   ^'
    )


def test_assert_success():
    obj = Matches('foo')
    assert obj == 'food'
    obj.assert_matches('food')


def test_fail_at_beginning():
    with pytest.raises(AssertionError) as excinfo:
        Matches('foo').assert_matches('bar')
    msg, = excinfo.value.args
    assert msg == (
        ' regex failed to match at:\n'
        '\n'
        '> bar\n'
        '  ^'
    )


def test_fail_at_end_of_line():
    with pytest.raises(AssertionError) as excinfo:
        Matches('foo').assert_matches('fo')
    msg, = excinfo.value.args
    assert msg == (
        ' regex failed to match at:\n'
        '\n'
        '> fo\n'
        '    ^'
    )


def test_fail_multiple_lines():
    with pytest.raises(AssertionError) as excinfo:
        Matches('foo.bar', re.DOTALL).assert_matches('foo\nbr')
    msg, = excinfo.value.args
    assert msg == (
        ' regex failed to match at:\n'
        '\n'
        '> foo\n'
        '> br\n'
        '   ^'
    )


def test_fail_end_of_line_with_newline():
    with pytest.raises(AssertionError) as excinfo:
        Matches('foo.bar', re.DOTALL).assert_matches('foo\n')
    msg, = excinfo.value.args
    assert msg == (
        ' regex failed to match at:\n'
        '\n'
        '> foo\n'
        '>\n'
        '  ^'
    )


def test_fail_at_end_of_line_mismatching_newline():
    with pytest.raises(AssertionError) as excinfo:
        Matches('foo.', re.DOTALL).assert_matches('foo')
    msg, = excinfo.value.args
    assert msg == (
        ' regex failed to match at:\n'
        '\n'
        '> foo\n'
        '     ^'
    )


def test_match_with_tabs():
    with pytest.raises(AssertionError) as excinfo:
        Matches('f.o.o').assert_matches('f\to\tx\n')
    msg, = excinfo.value.args
    assert msg == (
        ' regex failed to match at:\n'
        '\n'
        '> f\to\tx\n'
        '   \t \t^'
    )


def test_from_pattern():
    pattern = re.compile('^foo', flags=re.I)
    assert Matches.from_pattern(pattern) == 'FOO'
