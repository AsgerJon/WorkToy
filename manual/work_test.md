# worktoy manual: work_test

`worktoy.work_test` is the testing support worktoy's own suite runs on,
offered to projects as well: a `unittest.TestCase` base with a
sub-test that checks every case, seeded random data, and a pattern for
running one bank of tests against several implementations.

Everything shown here is promised. The examples are checked against
every release, so they keep working in every update. Anything this
chapter does not show may change.

Contents:

1. `BaseTest` and its `subTest`
2. Random data: the samplers
3. One bank of tests, many implementations


## 1. `BaseTest` and its `subTest`

Base a test class on `BaseTest` as on `unittest.TestCase`. Its
`subTest` runs every block of a loop, even after one fails, and the test
then fails once, with every failed block named:

```
>>> import unittest
>>> from worktoy.work_test import BaseTest
>>> class TestSquares(BaseTest):
...   def test_squares(self):
...     for value in (1, 2, 3, 4):
...       with self.subTest(value=value):
...         self.assertNotIn(value, (2, 3))
>>> result = unittest.TestResult()
>>> _ = unittest.TestLoader().loadTestsFromTestCase(TestSquares).run(result)
>>> result.testsRun, len(result.failures)
(1, 1)
>>> report = result.failures[0][1]
>>> 'value=2' in report, 'value=3' in report
(True, True)

```

What it adds over the `subTest` of `unittest`: that one reports each
failed block to the runner on its own, which some runners show poorly.
This one collects every block and fails the test once, at its end, with
the label and the traceback of each block that failed, so any runner
shows them all. A block raising an error, not only a failed assertion,
is recorded the same way and the loop goes on. Nested blocks join their
labels, as `outer=1 -> inner=2`.

A `setUp` of your own needs no call of the base's. `BaseTest` also has
`assertIsNotInstance` and `assertIsNotSubclass`, the negative
assertions under worktoy's names, on every Python worktoy supports.
`unittest` spells the first `assertNotIsInstance`, and gained its own
subclass pair only in Python 3.14.


## 2. Random data: the samplers

Each test has samplers of its own: `randomInteger`, `randomFloat`,
`randomGaussian`, `randomSymbolicName`, `randomWord` and `randomLorem`.
`seedSamplers(seed)` seeds them all, so the test repeats its data;
seed in `setUp` to make every run alike.

A sampler draws one value with `item`, a row with `row` and a table
with `table`, each anew at every read:

```
>>> from worktoy.work_test.samplers import IntSampler
>>> dice = IntSampler(1, 6, width=4, height=3, seed=7)
>>> len(dice.row), [len(row) for row in dice.table]
(4, [4, 4, 4])
>>> dice.item in range(1, 7)
True
>>> IntSampler(1, 6, seed=7).row == IntSampler(1, 6, seed=7).row
True

```

- The bounds are both included, and a swapped pair is put right:
  `IntSampler(6, 1)` draws from 1 to 6.
- A row is `width` or `size` values long, a table `height` or `count`
  rows; a size below one raises `ValueError`, and a keyword naming no
  setting raises `TypeError`.
- Each sampler draws from a generator of its own, `random`, which
  `seed=` seeds, so other code drawing in between changes nothing.

A sampler of your own subclasses `BaseSampler` with two methods, the
type of its values and a recipe for one:

```
>>> from worktoy.desc import AttriBox
>>> from worktoy.work_test.samplers import BaseSampler
>>> class DieSampler(BaseSampler):
...   sides = AttriBox[int](6)
...   def _getValueType(self, **kwargs):
...     return int
...   def _getItem(self, *args, **kwargs):
...     return self.random.randint(1, self.sides)
>>> die = DieSampler(seed=3)
>>> die.sides = 20
>>> die.item in range(1, 21)
True

```

Its settings are boxes, set after construction. A sampler leaving out
either method cannot be instantiated, and raises `TypeError`.

For text, `loremSentence(n)` gives a sentence of exactly `n`
characters, capitalized and closed by a period, and `randomWord()` a
word of `LOREM_WORDS`. These two draw from Python's own `random`, so
`random.seed` repeats them.


## 3. One bank of tests, many implementations

Several classes implementing one interface should pass one set of
tests, written once. `ComplexTest` shows the pattern: a bank of tests
for complex-number arithmetic, run against every class a test lists in
`targets`. `ComplexMixin` is the implementation it comes with, a class
getting the whole arithmetic of `complex` from two parts, `REAL` and
`IMAG`:

```
>>> from worktoy.work_test import ComplexMixin, ComplexTest
>>> class Simple(ComplexMixin):
...   pass
>>> z = Simple(1, 2)
>>> complex(z + Simple(3, 4)), z == 1 + 2j, abs(Simple(3, 4))
((4+6j), True, 5.0)
>>> class TestSimple(ComplexTest, BaseTest):
...   targets = (Simple,)
>>> result = unittest.TestResult()
>>> _ = unittest.TestLoader().loadTestsFromTestCase(TestSimple).run(result)
>>> result.wasSuccessful(), result.testsRun > 0
(True, True)

```

- The bank goes first among the bases and a test case after it,
  `BaseTest` or any other. A class listing the bank without a test case
  raises `TypeError`, so its tests cannot vanish from a run unnoticed.
- The bank has no base of its own, so it is never collected and run by
  itself. A test class without `targets` skips every test.
- A `ComplexMixin` is built from nothing, one number, a `complex`, a
  string `complex` parses, or two parts. It equals and hashes as
  `complex` does, and iterates its two parts.

A bank of your own follows the same shape: a class with no base,
holding test methods that loop over `self.targets` in blocks of
`subTest`, listed first beside a test case.
