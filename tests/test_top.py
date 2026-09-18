from expense_tracker.commands import add, top
from tests.conftest import args, make_store


def _seed(store):
    add.handle(
        args(amount="12.50", category="groceries", date="2026-01-15", note="weekly shop"),
        store,
    )
    add.handle(args(amount="40.00", category="transport", date="2026-01-16", note=""), store)
    add.handle(
        args(amount="4.20", category="food", date="2026-01-08", note="morning coffee"), store
    )


def test_top_defaults_to_three_largest_first(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()  # discard output from seeding

    code = top.handle(args(limit=3), store)
    out = capsys.readouterr().out.splitlines()

    assert code == 0
    assert out == [
        "#2  2026-01-16      $40.00  transport",
        "#1  2026-01-15      $12.50  groceries  (weekly shop)",
        "#3  2026-01-08       $4.20  food  (morning coffee)",
    ]


def test_top_respects_limit(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    code = top.handle(args(limit=2), store)
    out = capsys.readouterr().out.splitlines()

    assert code == 0
    assert out == [
        "#2  2026-01-16      $40.00  transport",
        "#1  2026-01-15      $12.50  groceries  (weekly shop)",
    ]


def test_top_limit_larger_than_available_prints_all_still_sorted(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    code = top.handle(args(limit=10), store)
    out = capsys.readouterr().out.splitlines()

    assert code == 0
    assert len(out) == 3
    assert out[0].endswith("transport")
    assert out[-1].endswith("(morning coffee)")


def test_top_keeps_insertion_order_for_equal_amounts(tmp_path, capsys):
    store = make_store(tmp_path)
    add.handle(args(amount="5.00", category="first", date="2026-01-01", note=""), store)
    add.handle(args(amount="5.00", category="second", date="2026-01-02", note=""), store)
    capsys.readouterr()

    top.handle(args(limit=2), store)
    out = capsys.readouterr().out.splitlines()

    assert out == [
        "#1  2026-01-01       $5.00  first",
        "#2  2026-01-02       $5.00  second",
    ]


def test_top_empty(tmp_path, capsys):
    store = make_store(tmp_path)

    code = top.handle(args(limit=3), store)
    out = capsys.readouterr().out

    assert code == 0
    assert "No expenses found." in out


def test_top_rejects_limit_below_one(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    code = top.handle(args(limit=0), store)
    out = capsys.readouterr().out

    assert code == 1
    assert "error: --limit must be at least 1" in out
