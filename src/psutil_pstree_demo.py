from cursor import Cursor
import pstree
from pstree import Tree

import psutil
from psutil import Process

from typing import Optional


def build_process_tree(process: Process) -> Tree:
    child_processes = filter(lambda x: x != process, process.children())
    sub_trees = [build_process_tree(p) for p in child_processes]
    try:
        process_name = process.name()
    except psutil.ZombieProcess:
        process_name = "**Zombie**"
    process_label = f"{process_name} : {process.pid}"
    return Tree(process_label, *sub_trees)


def _direct_print_tree(process: Process, cursor: Cursor, *, stream=None):
    process_id_str = str(process.pid)
    try:
        cursor = cursor.print(process.name(), " : ", process_id_str, file=stream)
    except psutil.ZombieProcess:
        cursor = cursor.print("**Zombie** : ", process_id_str, file=stream)
    child_processes = list(filter(lambda p: p != process, process.children()))
    for index, child in enumerate(child_processes):
        child_cursor = pstree.print_child_prefix(
            cursor, index, len(child_processes), file=stream
        )
        _direct_print_tree(child, child_cursor, stream=stream)


def direct_print_tree(
    process: Process, *, stream=None, cursor: Optional[Cursor] = None
):
    if cursor is None:
        cursor = Cursor()
    _direct_print_tree(process, cursor, stream=stream)


def indirect_print_tree(process: Process, stream=None):
    process_tree = build_process_tree(process)
    pstree.print_tree(process_tree, stream=stream)


import argparse
import io
import transpose

CHAR_MAP = {"-": "|", "|": "-", "`": "\\"}


def main(args: argparse.Namespace):
    root_process = Process(args.root_pid)
    stream = None  # default to stdout
    if args.orient == "vertical":
        stream = io.StringIO()

    if args.mode == "direct":
        direct_print_tree(root_process, stream)
    elif args.mode == "indirect":
        indirect_print_tree(root_process, stream)

    if stream is not None:
        vertical_lines = transpose.transpose(stream.getvalue())  # CHAR_MAP)
        print(*vertical_lines, sep="\n")
    else:
        # already printed, only add new line
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print process tree.")
    parser.add_argument(
        "--root-pid",
        dest="root_pid",
        metavar="N",
        type=int,
        default=0,
        help="pid for process to start tree from",
    )
    parser.add_argument(
        "--mode",
        dest="mode",
        choices=["direct", "indirect"],
        default="indirect",
        help="specify the whether to print the tree directly or convert to an intermediate representation",
    )
    parser.add_argument(
        "--orient",
        dest="orient",
        choices=["horizontal", "vertical"],
        default="horizontal",
        help="specify the whether to print the tree directly or convert to an intermediate representation",
    )
    args = parser.parse_args()
    main(args)
