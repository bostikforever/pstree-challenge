from __future__ import annotations
import copy

from typing import List, Optional


class _Marker:
    def __init__(self, offset: int, character: str):
        assert len(character) == 1
        self.offset = offset
        self.character = character


class Cursor:
    """
    Mechanism encoding the position to print from and the persistent markings to
    print when starting a new line.

    Usage
    -----

    Example 1: Basic usage, no markers
    - - - - - - - - - - - - - - - - - -
    ..
    c = Cursor()
    d = c.print("Hello")
    d.advance_line()
    d.print("World")
    d.advance_line()
    d.print("Hello")
    c.advance_line()
    c.print("World")
    print()
    ..

    This should output:
    ..
    Hello
         World
         Hello
    World
    ..

    Example 2: Basic usage, with markers
    - - - - - - - - - - - - - - - - - - -
    ..
    c = Cursor()
    d = c.print("Hello ").add_marker("*").print(" ")
    d.advance_line()
    d.print("World")
    d.advance_line()
    e = d.print("Hello ").add_marker("*").print(" ")
    e.advance_line()
    e.print("World")
    print()
    ..

    This should output:
    ..
    Hello *
          * World
          * Hello *
          *       * World
    ..
    """

    def __init__(
        self, offset: Optional[int] = None, markers: Optional[List[_Marker]] = None
    ):
        if offset is None:
            offset = 0
        # assumes markers is sorted
        if markers:
            last_marker = markers[-1]
            assert last_marker.offset < offset
        self._offset = offset
        # can use a node-based structure instead to save memory
        self._markers = copy.copy(markers) if markers is not None else []

    def print(self, *strings) -> Cursor:
        accum_len = 0
        for string in strings:
            print(string, end="")
            accum_len += len(string)
        return Cursor(self._offset + accum_len, self._markers)

    def add_marker(self, character) -> Cursor:
        assert not self._markers or self._markers[-1].offset < self._offset
        print(character, end="")
        marker = _Marker(self._offset, character)
        return Cursor(marker.offset + 1, self._markers + [marker])

    def advance_line(self):
        position = 0
        print()
        for marker in self._markers:
            print(" " * (marker.offset - position), marker.character, sep="", end="")
            position = marker.offset + 1
        print(" " * (self._offset - position), end="")
