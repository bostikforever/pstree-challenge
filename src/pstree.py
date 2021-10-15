from cursor import Cursor

import io
from typing import Optional


def _is_first(index: int, size: int):
    return index == 0


def _is_last(index: int, size: int):
    return index == size - 1


def print_child_prefix(
    cursor: Cursor, index: int, size: int, *, stream: Optional[io.TextIOBase] = None
) -> Cursor:
    """
    Use the specified 'cursor' to print the decorative prefix for the relative
    position determined using the specified 'index' and 'size' to the specified 'stream'
    if provided, or stdandard output otherwise.  Return a new 'Cursor' encoding the new
    postion to print from as well as any branch markings added.
    """
    if not _is_first(index, size):
        cursor.advance_line(stream=stream)
    if _is_first(index, size) and _is_last(index, size):
        cursor = cursor.print("--", stream=stream)
    elif _is_first(index, size):
        cursor = cursor.print("-", stream=stream)
        cursor = cursor.add_marker("|")
        cursor = cursor.print("+", stream=stream)
    elif _is_last(index, size):
        cursor = cursor.print(" `", stream=stream)
    else:
        cursor = cursor.print(" ", stream=stream)
        cursor = cursor.add_marker("|")
        cursor = cursor.print("|", stream=stream)
    cursor = cursor.print("-", stream=stream)
    return cursor


class Tree:
    def __init__(self, data, *children):
        self.data = data
        self.children = children


def _print_tree(tree: Tree, cursor: Cursor, *, stream: Optional[io.TextIOBase] = None):
    cursor = cursor.print(tree.data, stream=stream)
    for index, child in enumerate(tree.children):
        child_cursor = print_child_prefix(
            cursor, index, len(tree.children), stream=stream
        )
        _print_tree(child, child_cursor, stream=stream)


def print_tree(
    tree: Tree,
    *,
    stream: Optional[io.TextIOBase] = None,
    cursor: Optional[Cursor] = None
):
    if cursor is None:
        cursor = Cursor()
    _print_tree(tree, cursor, stream=stream)
