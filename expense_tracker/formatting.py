"""Shared rendering of an expense as a single display line.

Both ``list`` and ``top`` print expenses in the same format. Keeping that
format in one place means the two commands cannot drift apart.
"""

from __future__ import annotations

from .models import Expense
from .money import format_amount


def format_expense_line(expense: Expense) -> str:
    """Render one expense as the CLI's standard single-line summary.

    Args:
        expense: The expense to render.

    Returns:
        A line such as ``#1  2026-01-15      $12.50  groceries  (weekly shop)``.
    """
    note = f"  ({expense.note})" if expense.note else ""
    return (
        f"#{expense.id}  {expense.date}  "
        f"{format_amount(expense.amount_cents):>10}  {expense.category}{note}"
    )
