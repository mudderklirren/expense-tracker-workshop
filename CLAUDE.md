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

## General principles

- Always write clean, maintainable, well-structured, idiomatic code.
- Follow SOLID principles at all times. Prefer composition over inheritance.
- Follow the DRY principle. Do not repeat yourself. But also follow KISS and
  do not over-engineer. Use your best judgment to balance these.
- Write self-documenting code. Add comments where the intent is not obvious.
- Leave the codebase better than you found it (the Boy Scout Rule).
- Think step by step. Take your time. Quality over speed.
- Be consistent with the surrounding code.
- Prefer readability over cleverness.
- Smaller functions are usually better. If a function does not fit on a screen,
  consider splitting it.

## Conventions

### Python style

- Follow PEP 8. Use type hints on all public functions.
- Maximum line length is 79 characters (from our 2023 Python style guide).
- Use `snake_case` for functions and variables, `PascalCase` for classes.
- Prefer f-strings over `.format()` and `%` formatting.
- Docstrings on all modules and public functions, in Google style.
- Prefer `pathlib` over `os.path`.
- Sort imports: standard library, third party, local; alphabetised within each
  group. (We used to use isort; ruff now does this.)
- Avoid mutable default arguments. Use `None` and assign inside.

### Testing

- We use pytest. Tests live in `tests/`, mirroring the package layout.
- Every new behaviour needs a test that fails without the change.
- Use `tmp_path` for anything that touches the filesystem. Never write test
  artifacts into the repo.
- Aim for meaningful coverage, not a coverage percentage. Test behaviour, not
  implementation details.
- Frontend tests use Jest and React Testing Library. Test what the user sees.
- End-to-end tests use Playwright and live in `e2e/`. Keep them stable; a flaky
  test is worse than no test.
- Mark slow tests with `@pytest.mark.slow` so they can be skipped locally.

### Git and pull requests

- Branch names: `type/short-description` (`feat/add-tags`, `fix/date-parse`).
- We use Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`).
- Keep PRs small and focused. One logical change per PR.
- PR descriptions must state what changed, why, and how it was verified.
- At least one approving review before merge. Squash-merge to main.
- Never force-push to a shared branch.

### Code review checklist

- Does the change do what the description says, and nothing more?
- Are there tests, and do they fail without the change?
- Any security, privacy, or money-handling concern?
- Is the naming clear? Will someone understand this in six months?
- Is anything here better solved by deleting code than adding it?

### Security

- No secrets in code, logs, or prompts. Use environment variables.
- Validate and sanitise all external input.
- Keep dependencies current; do not pin to abandoned packages.
- Report anything suspicious to the security channel; do not sit on it.

### Performance

- Do not optimise prematurely. Measure first.
- Be mindful of N+1 queries in any data-access path.
- Cache deliberately, and always with an invalidation story.

### Documentation

- Update the README when you change how something is run or configured.
- Architecture decisions of any weight get an ADR in `docs/adr/`.
- Keep this file up to date. (In practice, nobody does, so be skeptical of
  anything here that the code contradicts.)

### Data and money handling

- Dates use ISO 8601 (`YYYY-MM-DD`). Parse and validate; never trust a raw
  string. Reject malformed dates with a clear error.
- All monetary amounts are represented as an integer number of minor units
  (cents). Never use floating-point numbers for money. This applies to storage,
  arithmetic, and any intermediate calculation. Formatting for display is the
  only place cents are converted back, and even then with integer math.
- Categories are free-text lowercase strings for now. A controlled vocabulary
  is on the roadmap; do not build it yet.
- Never log full request bodies or anything that could contain personal or
  financial data.

## Notes

I prefer dark mode and I usually work in VS Code. Don't be too verbose in your
responses. Use the latest Python features where you can.

The team is discussing whether to migrate to a database. There was a bug in the
summary command last March but I think Dave fixed it.