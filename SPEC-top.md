# Spec: `top` command (Variant C)

## The task
The CLI can `add`, `list`, `summary` and `delete`, but there is no way to ask
"what did I spend the most on?" — you have to `list` everything and scan it.

Add a read-only `top` command that prints the N largest expenses, biggest
first, with an optional `--limit N` (default 3). Nothing about how expenses
are stored changes.

Done means: `top --limit 2` prints exactly the two largest expenses in
descending order, and `--limit` larger than the number of expenses prints all
of them, still sorted.

## Density

**Dense on one line: `--limit` below 1.** argparse with `type=int` accepts
`--limit -1` without complaint, and `expenses[:-1]` then drops the *last*
item and prints the rest. That is not a crash and not an empty result — it is
a plausible-looking answer that is quietly wrong, and nothing downstream can
tell. Specify it: anything below 1 is an error, exit code 1, no output rows.

**Medium on the output format.** It must match `list` byte for byte, because
the two will be read side by side. The spec carries one worked example
(below) so there is something to assert against rather than a description to
interpret.

**Loose on everything else.** Module name, help text, whether the default
lives in a constant, how the sort is expressed — all free. Follow the shape
of the existing command modules and it will be right.

## First test
1. Seed three expenses; `top --limit 2` prints exactly:

       #2  2026-01-16      $40.00  transport
       #1  2026-01-15      $12.50  groceries  (weekly shop)

2. `top --limit 0` prints an error and returns exit code 1, with two
   expenses in the store.

## Open question
Two expenses of the same amount have no defined order. Stable sort (equal
amounts keep id order) is free and reproducible, but it means the "top 3" of
four equal expenses silently depends on insertion order. Reject that as
arbitrary and sort by date as a tie-break, or accept it and document it?
