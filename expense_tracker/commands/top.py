"""The ``top`` command: show the largest expenses."""

from __future__ import annotations

from ..formatting import format_expense_line

NAME = "top"
HELP = "Show the largest expenses, biggest first"

DEFAULT_LIMIT = 3


def add_parser(subparsers) -> None:
    parser = subparsers.add_parser(NAME, help=HELP)
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"How many expenses to show (default: {DEFAULT_LIMIT})",
    )


def handle(args, store) -> int:
    # argparse accepts any int, including 0 and negatives. Slicing with a
    # negative limit would quietly drop items instead of failing, so reject it.
    if args.limit < 1:
        print("error: --limit must be at least 1")
        return 1

    expenses = store.load()
    if not expenses:
        print("No expenses found.")
        return 0

    # sorted() is stable, so expenses of equal size keep their insertion order.
    largest = sorted(expenses, key=lambda e: e.amount_cents, reverse=True)[: args.limit]

    for expense in largest:
        print(format_expense_line(expense))
    return 0
