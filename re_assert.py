from typing import Any
from typing import Optional
from typing import Pattern

import regex


class Matches:  # TODO: Generic[AnyStr] (binary pattern support)
    def __init__(self, pattern: str, *args: Any, **kwargs: Any) -> None:
        self._pattern = regex.compile(pattern, *args, **kwargs)
        self._fail: Optional[str] = None
        self._type = type(pattern)

    def _fail_message(self, fail: str) -> str:
        # binary search to find the longest substring match
        pos, bound = 0, len(fail)
        while pos < bound:
            pivot = pos + (bound - pos + 1) // 2
            match = self._pattern.match(fail[:pivot], partial=True)
            if match:
                pos = pivot
            else:
                bound = pivot - 1

        retv = [' regex failed to match at:', '']
        for line in fail.splitlines(True):
            line_noeol = line.rstrip('\r\n')
            retv.append(f'> {line_noeol}')
            if 0 <= pos <= len(line_noeol):
                indent = ''.join(c if c.isspace() else ' ' for c in line[:pos])
                retv.append(f'  {indent}^')
                pos = -1
            else:
                pos -= len(line)
        if pos >= 0:
            retv.append('>')
            retv.append('  ^')
        return '\n'.join(retv)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self._type):
            raise TypeError(f'expected {self._type}, got {type(other)}')
        if not self._pattern.match(other):
            self._fail = self._fail_message(other)
            return False
        else:
            self._fail = None
            return True

    def __repr__(self) -> str:
        pattern_repr = repr(self._pattern)
        params = pattern_repr[pattern_repr.index('(') + 1:-1]
        boring_flag = ', flags=regex.V0'
        if params.endswith(boring_flag):
            params = params[:-1 * len(boring_flag)]
        if self._fail is not None:
            fail_msg = '    #'.join(['\n'] + self._fail.splitlines(True))
        else:
            fail_msg = ''
        return f'{type(self).__name__}({params}){fail_msg}'

    def assert_matches(self, s: str) -> None:
        assert self == s, self._fail

    @classmethod
    def from_pattern(cls, pattern: Pattern[str]) -> 'Matches':
        return cls(pattern.pattern, pattern.flags)
