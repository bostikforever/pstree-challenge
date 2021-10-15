import pstree
from pstree import Tree


EXAMPLE_TREE = (
Tree("init", Tree("amd")
           , Tree("2*[strsd]")
           , Tree("atd")
           , Tree("crond")
           , Tree("deskguide_apple")
           , Tree("eth0")
           , Tree("gdm", Tree("gdm", Tree("X")
                                   , Tree("gnome-session", Tree("Gnome")
                                                         , Tree("ssh-agent")
                                                         , Tree("true"))))
           , Tree("geyes_applet")
           , Tree("gkb_applet")
           , Tree("gnome-name-serv")
           , Tree("gnome-terminal", Tree("bash", Tree("vim"))
                                  , Tree("bash")
                                  , Tree("bash", Tree("pstree"))
                                  , Tree("bash", Tree("ssh"))
                                  , Tree("bash", Tree("mozilla-bin", Tree("mozilla-bin", Tree("3*[mozilla-bin]"))))
                                  , Tree("gnome-pty-helper"))
           , Tree("gpm")
           , Tree("gweather")
           , Tree("kapm-idled"))
)


def pstree_demo():
    pstree.print_tree(EXAMPLE_TREE)
    print()


def ps_tree_demo_vertical():
    import io

    stream = io.StringIO()
    pstree.print_tree(EXAMPLE_TREE, stream=stream)
    import transpose

    vertical_lines = transpose.transpose(
        stream.getvalue(), char_map=pstree.BASIC_CHAR_MAP
    )
    print(*vertical_lines, sep="\n")


if __name__ == "__main__":
    # pstree_demo()
    ps_tree_demo_vertical()
