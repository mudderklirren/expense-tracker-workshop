from expense_tracker.commands import add, summary
from tests.conftest import args, make_store


def _seed(store):
    add.handle(args(amount="10.00", category="food", date="2026-01-01", note=""), store)
    add.handle(args(amount="20.00", category="travel", date="2026-01-02", note=""), store)
    add.handle(args(amount="5.00", category="food", date="2026-02-03", note=""), store)
    add.handle(args(amount="3.25", category="books", date="2026-01-15", note=""), store)


def test_summary_groups_by_category_with_total(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    code = summary.handle(args(month=None), store)
    out = capsys.readouterr().out.splitlines()

    assert code == 0
    assert out == [
        "     $3.25  books",
        "    $15.00  food",
        "    $20.00  travel",
        "    $38.25  Total",
    ]


def test_summary_filters_by_month(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    code = summary.handle(args(month="2026-01"), store)
    out = capsys.readouterr().out

    assert code == 0
    assert "$10.00  food" in out
    assert "$20.00  travel" in out
    assert "$3.25  books" in out
    assert "$33.25  Total" in out
    assert "$15.00  food" not in out


def test_summary_empty(tmp_path, capsys):
    store = make_store(tmp_path)

    code = summary.handle(args(month=None), store)
    out = capsys.readouterr().out

    assert code == 0
    assert "No expenses found." in out


def test_summary_empty_month(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    code = summary.handle(args(month="2027-01"), store)
    out = capsys.readouterr().out

    assert code == 0
    assert "No expenses found." in out


def test_summary_rejects_bad_month(tmp_path, capsys):
    store = make_store(tmp_path)

    code = summary.handle(args(month="2026-13"), store)
    out = capsys.readouterr().out

    assert code == 1
    assert "error: invalid month: '2026-13'" in out
    assert store.load() == []
