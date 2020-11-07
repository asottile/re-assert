[![Build Status](https://dev.azure.com/asottile/asottile/_apis/build/status/asottile.re-assert?branchName=master)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=31&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/31/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=31&branchName=master)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/asottile/re-assert/master.svg)](https://results.pre-commit.ci/latest/github/asottile/re-assert/master)

re-assert
=========

show where your regex match assertion failed!

## installation

`pip install re-assert`

## usage

`re-assert` provides a helper class to make assertions of regexes simpler.

### `re_assert.Matches(pattern: str, *args, **kwargs)`

construct a `Matches` object.

_note_: under the hood, `re-assert` uses the [`regex`] library for matching,
any `*args` / `**kwargs` that `regex.compile` supports will work.  in general,
 the `regex` library is 100% compatible with the `re` library (and will even
accept its flags, etc.)

[`regex`]: https://pypi.org/project/regex/

### `re_assert.Matches.from_pattern(pattern: Pattern[str]) -> Matches`

construct a `Matches` object from an already-compiled regex.

this is useful (for instance) if you're testing an existing compiled regex.

```pycon
>>> import re
>>> reg = re.compile('foo')
>>> Matches.from_pattern(reg) == 'fork'
False
>>> Matches.from_pattern(reg) == 'food'
True
```

### `Matches.__eq__(other)` (`==`)

the equality operator is overridden for use with assertion frameworks such
as pytest

```pycon
>>> pat = Matches('foo')
>>> pat == 'bar'
False
>>> pat == 'food'
True
```

### `Matches.__repr__()` (`repr(...)`)

a side-effect of an equality failure changes the `repr(...)` of a `Matches`
object.  this allows for useful pytest assertion messages:

```pytest
>       assert Matches('foo') == 'fork'
E       AssertionError: assert Matches('foo'...ork\n    #    ^ == 'fork'
E         -Matches('foo')\n
E         -    # regex failed to match at:\n
E         -    #\n
E         -    #> fork\n
E         -    #    ^
E         +'fork'
```

### `Matches.assert_matches(s: str)`

if you're using some other test framework, this method is useful for producing
a readable traceback

```pycon
>>> Matches('foo').assert_matches('food')
>>> Matches('foo').assert_matches('fork')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/asottile/workspace/re-assert/re_assert.py", line 63, in assert_matches
    assert self == s, self._fail
AssertionError:  regex failed to match at:

> fork
    ^
```
