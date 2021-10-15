from __future__ import annotations
from typing import Dict, Iterable, Optional
import itertools


class Line:
    class LineIter:
        def __init__(self, line: Line):
            self._line = line
            self._offset = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self._offset == self._line._length:
                raise StopIteration()
            ret = self._line[self._offset]
            self._offset += 1
            return ret

    def __init__(self, base: str, begin: int, end: int):
        assert end <= len(base)
        assert begin <= end
        self._base = base
        self._begin = begin
        self._length = end - begin

    def __iter__(self):
        return self.LineIter(self)

    def __getitem__(self, index: int):
        if index > self._length:
            raise IndexError(
                f"Specified index '{index}' exceeds length '{self._length}'"
            )
        base_index = self._begin + index
        return self._base[base_index]

    def __len__(self):
        return self._length

    def __str__(self) -> str:
        return _join(iter(self), 0)

    def __repr__(self) -> str:
        return str(self)


def split_lines(string: str, *, delimiter="\n") -> Iterable[Iterable[str]]:
    """
    Split the specified 'string' into multiple lines determined by the specified
    'delimiter', returning an iterable of string iterables with each inner iterable
    representing a line.  Note that the delimiters are not included in any of the lines.
    """
    lines = []
    start = -1
    while start < len(string):
        start += 1
        end = string.find(delimiter, start)
        if end == -1:
            end = len(string)
        # itertools.islice, while able to achieve similar cannot "jump" to 'start' so
        # would need to traverse from the begining for each slice.
        lines.append(Line(string, start, end))
        start = end
    return lines


def _join(string_iter: Iterable[str], interspace: int) -> str:
    return (" " * interspace).join(string_iter)


def _join_with_translate(char_map: Dict[str, str], interspace: int):
    def inner_join(string_iter: Iterable[str]):
        def _get_default(character: str):
            return char_map.get(character, character)

        return _join(map(_get_default, string_iter), interspace)

    return inner_join


def transpose(
    screen: str, *, interspace=2, char_map: Optional[Dict[str, str]] = None
) -> Iterable[str]:
    """
    Transpose the specified 'screen' so that rows becomes columns, applying the
    specified 'interspace' spacing between columns in the new transposed screen and
    using the specified 'char_map' if provided to select alternate orientation.  Note
    that if 'char_map' is not provided, or if a character is not in 'char_map', then the
    character is rendered as it originally is.
    """
    lines = split_lines(screen)
    transpose_lines_iter = itertools.zip_longest(*lines, fillvalue=" ")
    if char_map:
        return map(_join_with_translate(char_map, interspace), transpose_lines_iter)
    return map(lambda x: _join(x, interspace), transpose_lines_iter)
