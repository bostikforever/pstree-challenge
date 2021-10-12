from cursor import Cursor


def hello_world_cursor_test_1():
    c = Cursor()
    d = c.print("Hello")
    d.advance_line()
    d.print("World")
    d.advance_line()
    d.print("Hello")
    c.advance_line()
    c.print("World")
    print()


def hello_world_cursor_test_2():
    c = Cursor()
    d = c.print("Hello ").add_marker("*").print(" ")
    d.advance_line()
    d.print("World")
    d.advance_line()
    e = d.print("Hello ").add_marker("*").print(" ")
    e.advance_line()
    e.print("World")
    print()


from pstree import print_child_prefix


def print_child(cursor: Cursor, index: int, size: int, data: str) -> Cursor:
    """
    Use the specified 'cursor' to print the specified 'data' using the
    spcified, 'index' and 'size' to determine 'data's relative position
    among its siblings.  Return a Cursor that encodes the new position
    as well as any branch markings added.
    """
    cursor = print_child_prefix(cursor, index, size)
    cursor = cursor.print(data)
    return cursor


def tree_cursor_test():
    root = Cursor()
    cursor = root.print("init")

    print_child(cursor, 0, 16, "amd")

    print_child(cursor, 1, 16, "apmd")

    print_child(cursor, 2, 16, "2*[artsd]")

    print_child(cursor, 3, 16, "atd")

    print_child(cursor, 4, 16, "crond")

    print_child(cursor, 5, 16, "deskguide_apple")

    print_child(cursor, 6, 16, "eth0")

    gdm_cursor = print_child(cursor, 7, 16, "gdm")

    gdm_gdm_cursor = print_child(gdm_cursor, 0, 1, "gdm")

    print_child(gdm_gdm_cursor, 0, 2, "X")

    gnome_session_cursor = print_child(gdm_gdm_cursor, 1, 2, "gnome-session")

    print_child(gnome_session_cursor, 0, 3, "Gnome")

    print_child(gnome_session_cursor, 1, 3, "ssh-agent")

    print_child(gnome_session_cursor, 2, 3, "true")

    print_child(cursor, 8, 16, "geyes-applet")

    print_child(cursor, 9, 16, "gtk-applet")

    print_child(cursor, 10, 16, "gnome-name-serv")

    print_child(cursor, 11, 16, "gnome-smproxy")

    gnome_terminal_cursor = print_child(cursor, 12, 16, "gnome-terminal")
    bash_0 = print_child(gnome_terminal_cursor, 0, 6, "bash")
    print_child(bash_0, 0, 1, "vim")
    print_child(gnome_terminal_cursor, 1, 6, "bash")
    bash_2 = print_child(gnome_terminal_cursor, 2, 6, "bash")
    print_child(bash_2, 0, 1, "pstree")
    bash_3 = print_child(gnome_terminal_cursor, 3, 6, "bash")
    print_child(bash_3, 0, 1, "ssh")
    bash_4 = print_child(gnome_terminal_cursor, 4, 6, "bash")
    moz_0 = print_child(bash_4, 0, 1, "mozilla-bin")
    moz_1 = print_child(moz_0, 0, 1, "mozilla-bin")
    print_child(moz_1, 0, 1, "3*[mozilla-bin]")
    print_child(gnome_terminal_cursor, 5, 6, "gnome-pty-helper")

    print_child(cursor, 13, 16, "gpm")

    print_child(cursor, 14, 16, "gweather")

    print_child(cursor, 15, 16, "kapm-idled")

    print()


if __name__ == "__main__":
    hello_world_cursor_test_1()
    hello_world_cursor_test_2()
    tree_cursor_test()
