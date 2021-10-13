from cursor import Cursor

from typing import Optional
from cursor import Cursor


def _is_first(index: int, size: int):
    return index == 0


def _is_last(index: int, size: int):
    return index == size - 1


def print_child_prefix(cursor: Cursor, index: int, size: int) -> Cursor:
    """
    Use the specified 'cursor' to print the decorative prefix for the relative
    position determined using the specified 'index' and 'size'.  Return a new
    'Cursor' encoding the new postion to print from as well as any branch
    markings added.
    """
    if not _is_first(index, size):
        cursor.advance_line()
    if _is_first(index, size) and _is_last(index, size):
        cursor = cursor.print("--")
    elif _is_first(index, size):
        cursor = cursor.print("-")
        cursor = cursor.add_marker("|")
        cursor = cursor.print("+")
    elif _is_last(index, size):
        cursor = cursor.print(" `")
    else:
        cursor = cursor.print(" ")
        cursor = cursor.add_marker("|")
        cursor = cursor.print("|")
    cursor = cursor.print("-")
    return cursor


class Tree:
    def __init__(self, data, *children):
        self.data = data
        self.children = children


def _print_tree(tree: Tree, cursor: Cursor):
    cursor = cursor.print(tree.data)
    for index, child in enumerate(tree.children):
        child_cursor = print_child_prefix(cursor, index, len(tree.children))
        _print_tree(child, child_cursor)


def print_tree(tree: Tree, cursor: Optional[Cursor] = None):
    if cursor is None:
        cursor = Cursor()
    _print_tree(tree, cursor)
