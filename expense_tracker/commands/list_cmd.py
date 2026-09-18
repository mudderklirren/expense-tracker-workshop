"""The ``list`` command: show recorded expenses."""

from __future__ import annotations

from ..formatting import format_expense_line

NAME = "list"
HELP = "List expenses, optionally filtered by category"


def add_parser(subparsers) -> None:
    parser = subparsers.add_parser(NAME, help=HELP)
    parser.add_argument(
        "--category",
        default=None,
        help="Only show expenses in this category",
    )


def handle(args, store) -> int:
    expenses = store.load()
    if args.category is not None:
        expenses = [e for e in expenses if e.category == args.category]

    if not expenses:
        print("No expenses found.")
        return 0

    for e in expenses:
        print(format_expense_line(e))
    return 0
