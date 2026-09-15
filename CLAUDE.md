# CLAUDE.md

This is the expense tracker project. It is a Python application that tracks
expenses. Please write clean, readable, maintainable code and follow Python
best practices at all times. Use good variable names and add comments where
appropriate. Make sure the code is well tested and handles errors gracefully.

## Project structure

expense_tracker/
__init__.py
__main__.py
cli.py
models.py
money.py
storage.py
commands/
add.py
delete.py
list_cmd.py
summary.py
tests/
conftest.py
test_add.py
test_delete.py
test_money.py
test_summary.py

## Dependencies

- pytest
- ruff

## Notes

I prefer dark mode and I usually work in VS Code. Don't be too verbose in your
responses. Use the latest Python features where you can.

The team is discussing whether to migrate to a database. There was a bug in the
summary command last March but I think Dave fixed it.