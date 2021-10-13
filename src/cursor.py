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
    d = c.print("Hello ").add_marker("*").print("  ")
    d.advance_line()
    d.print("World")
    d.advance_line()
    e = d.print("Hello ").add_marker("*").print("* ")
    e.advance_line()
    e.print("World")
    print()
    ..

    This should output:
    ..
    Hello   
        * World
        * Hello * 
        *       * World
    ..
    """

    def __init__(self):
        self._init_cursor(0, None)

    def _init_cursor(self, offset: int, markers: Optional[_Marker]):
        assert markers is None or markers.offset <= offset
        self._offset = offset
        self._markers = markers

    @classmethod
    def _create_cursor(cls, offset: int, markers: Optional[_Marker]) -> Cursor:
        new_cursor = cls()
        new_cursor._init_cursor(offset, markers)
        return new_cursor

    def print(self, *strings) -> Cursor:
        """
        Print the specified 'strings' to screen, returning a new 'Cursor' object that
        repesents the current object after advancement by the total length of 'strings'.
        """
        accum_len = 0
        for string in strings:
            print(string, end="")
            accum_len += len(string)
        return Cursor._create_cursor(self._offset + accum_len, self._markers)

    def add_marker(self, character) -> Cursor:
        """
        Return a new 'Cursor' object with the marker specified by 'character' added at
        the current offset.  Note that this call does not print 'character' to screen
        and the returned 'Cursor' is not advanced.  The behaviour is undefined unless
        character is a single character string.
        """
        assert not self._markers or self._markers.offset <= self._offset
        new_markers = _Marker(self._offset, character, self._markers)
        return Cursor._create_cursor(new_markers.offset, new_markers)

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
        """
        Print a new line followed by whitespace and any markers in the current object,
        up until the position represented by this 'Cursor' object.  This method provides
        a way to "initiailze" a new line to begin printing at the position represented
        by this object while printing any stored line markings that should occur before
        the position.
        """
        print("\n", *self._accumulate_markers_and_offset(), sep="", end="")
