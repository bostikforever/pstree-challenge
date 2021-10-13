from __future__ import annotations

from typing import Iterable, Optional


class _Marker:
    def __init__(self, offset: int, character: str, prev: Optional[_Marker] = None):
        # ensure markers is sorted
        assert prev is None or offset > prev.offset
        assert len(character) == 1
        self.offset: int = offset
        self.character = character
        self.prev = prev


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

    def __init__(self, offset: Optional[int] = None, markers: Optional[_Marker] = None):
        if offset is None:
            offset = 0
        assert markers is None or markers.offset < offset
        self._offset = offset
        self._markers = markers

    def print(self, *strings) -> Cursor:
        accum_len = 0
        for string in strings:
            print(string, end="")
            accum_len += len(string)
        return Cursor(self._offset + accum_len, self._markers)

    def add_marker(self, character) -> Cursor:
        assert not self._markers or self._markers.offset < self._offset
        print(character, end="")
        new_markers = _Marker(self._offset, character, self._markers)
        return Cursor(new_markers.offset + 1, new_markers)

    def _accumulate_markers_and_offset(self) -> Iterable[str]:
        reversed_segments = []
        marker = self._markers
        position = self._offset
        while marker is not None:
            reversed_segments.append(" " * (position - marker.offset - 1))
            reversed_segments.append(marker.character)
            position = marker.offset
            marker = marker.prev
        reversed_segments.append(" " * position)
        return reversed(reversed_segments)

    def advance_line(self):
        print("\n", *self._accumulate_markers_and_offset(), sep="", end="")
