"""The ``summary`` command: show spending totals by category."""

from __future__ import annotations

from datetime import date as date_cls

from ..money import format_amount

NAME = "summary"
HELP = "Summarize spending by category"


def add_parser(subparsers) -> None:
    parser = subparsers.add_parser(NAME, help=HELP)
    parser.add_argument(
        "--month",
        default=None,
        help="Only summarize expenses from this month, in YYYY-MM format",
    )


def _validate_month(value: str) -> str:
    if len(value) != 7 or value[4] != "-":
        raise ValueError(f"invalid month: {value!r}")

    year, month = value.split("-", maxsplit=1)
    if not year.isdigit() or not month.isdigit():
        raise ValueError(f"invalid month: {value!r}")

    try:
        date_cls.fromisoformat(f"{value}-01")
    except ValueError as exc:
        raise ValueError(f"invalid month: {value!r}") from exc
    return value


def handle(args, store) -> int:
    try:
        month = _validate_month(args.month) if args.month is not None else None
    except ValueError as exc:
        print(f"error: {exc}")
        return 1

    expenses = store.load()
    if month is not None:
        expenses = [e for e in expenses if e.date.startswith(month)]

    if not expenses:
        print("No expenses found.")
        return 0

    totals_by_category: dict[str, int] = {}
    for expense in expenses:
        totals_by_category[expense.category] = (
            totals_by_category.get(expense.category, 0) + expense.amount_cents
        )

    for category in sorted(totals_by_category):
        print(f"{format_amount(totals_by_category[category]):>10}  {category}")

    total_cents = sum(totals_by_category.values())
    print(f"{format_amount(total_cents):>10}  Total")
    return 0
