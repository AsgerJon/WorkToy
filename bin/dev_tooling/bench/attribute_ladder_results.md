# Attribute ladder, 2026-11-07

Measured with `attribute_ladder.py` on worktoy 1.1.0, nanoseconds per
access, best of three runs of 600000, on one idle machine.

| access                          | 3.7 read | 3.7 write | 3.14 read | 3.14 write | 3.15 read | 3.15 write |
| ------------------------------- | -------: | --------: | --------: | ---------: | --------: | ---------: |
| plain attribute, instance dict  |       25 |        28 |        12 |         12 |        14 |         14 |
| plain attribute, `__slots__`    |       24 |        28 |        11 |         12 |        14 |         13 |
| `FastBox[int]`                  |      139 |       227 |       101 |        136 |       104 |        138 |
| `AttriBox[int]` on `BaseObject` |     4084 |      2998 |      2226 |       1656 |      2189 |       1569 |
| `property`, reads `_x + 1`      |       81 |           |        31 |            |        33 |            |
| `Field` with `GET`, reads `x + 1` |   9533 |           |      5171 |            |      5159 |            |

The ratios hold across the three interpreters: a `FastBox` costs seven
to ten plain attributes, an `AttriBox` about 150, a `Field` about 370.
The absolute numbers halve from 3.7 to 3.14, which is the interpreter's
work, not the library's. Slots buy no speed on any of them.

Where an `AttriBox` read goes, from a profile on 3.15: about half in the
two read-hook phases, run through the recursion guard even when no
callback is registered; a sixth in `__get__` itself; an eighth in the
frame push and pop; a tenth in the lookup. Skipping a hook phase that
has nothing to run, and answering a settled box with no hooks the way a
`FastBox` does, are the two planned changes for the 1.2 line.
