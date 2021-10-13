from cursor import Cursor
import pstree
from pstree import Tree

import psutil
from psutil import Process

from typing import Optional


def build_process_tree(process: Process) -> Tree:
    child_processes = filter(lambda x: x != process, process.children())
    # to interleave the processing, make this a generator instead?
    # so there will be no need to build the tree till it is printed.
    sub_trees = [build_process_tree(p) for p in child_processes]
    try:
        process_name = process.name()
    except psutil.ZombieProcess:
        process_name = "**Zombie**"
    process_label = f"{process_name} : {process.pid}"
    # above idea is constrained by this interface, you are spreading the argument
    # so the generator will iterative over the subtrees here
    return Tree(process_label, *sub_trees)


def _direct_print_tree(process: Process, cursor: Cursor):
    process_id_str = str(process.pid)
    try:
        cursor = cursor.print(process.name(), " : ", process_id_str)
    except psutil.ZombieProcess:
        cursor = cursor.print("**Zombie** : ", process_id_str)
    child_processes = list(filter(lambda p: p != process, process.children()))
    for index, child in enumerate(child_processes):
        child_cursor = pstree.print_child_prefix(cursor, index, len(child_processes))
        _direct_print_tree(child, child_cursor)


def direct_print_tree(process: Process, cursor: Optional[Cursor] = None):
    if cursor is None:
        cursor = Cursor()
    _direct_print_tree(process, cursor)


import argparse

if __name__ == "__main__":
    import argparse

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
    args = parser.parse_args()

    root_process = Process(args.root_pid)

    if args.mode == "direct":
        direct_print_tree(root_process)
    elif args.mode == "indirect":
        process_tree = build_process_tree(root_process)
        pstree.print_tree(process_tree)

    print()
