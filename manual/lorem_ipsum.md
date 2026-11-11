# worktoy manual: lorem_ipsum

`worktoy.lorem_ipsum` makes placeholder text of an exact number of
characters, for mock-ups, fixed-width fields and layout tests. It is
also a small worked example of worktoy itself: the generators are
`BaseObject` classes with boxes and overloads.

Everything shown here is promised. The examples are checked against
every release, so they keep working in every update. Anything this
chapter does not show may change.

Contents:

1. Text of an exact length
2. Clause, sentence, paragraph
3. Repeatable text
4. Words of your own
5. The distributions underneath


## 1. Text of an exact length

Every generator takes a character count and gives text of exactly that
many characters:

```
>>> from worktoy.lorem_ipsum import Clause, Sentence, Paragraph
>>> paragraph = Paragraph(200)
>>> len(str(paragraph)), len(paragraph)
(200, 200)
>>> str(paragraph).startswith('Lorem ipsum')
True

```

A draw of `str(Sentence(60))` might read `Ingenium ordo sensus numerus
aura mare lorem pontus fortuna.`: Latin-looking words from the three
lists the package exports, `COMMON_WORDS`, `UNCOMMON_WORDS` and
`RARE_WORDS`, drawn mostly from the first.

The count is given by position, as `charCount`, or not at all for 40.
A negative count raises `ValueError` at once, and any other keyword
raises `TypeError`. The text is made at the first read and kept, so two
reads give the same text, and `reset()` makes a new one of the same
count:

```
>>> clause = Clause(40)
>>> str(clause) == str(clause)
True
>>> clause.reset()
>>> len(str(clause))
40

```

Assigning `charCount` makes a text of the new count, and so does
assigning `isFirst` of the next section. A generator given another of
its kind copies it, the text it has realized included.


## 2. Clause, sentence, paragraph

- A `Clause` is words joined by single spaces, without punctuation.
  Iterating it gives its words, and `len` gives its characters.
- A `Sentence` is clauses joined by `', '`, its first letter capital and
  its last character a period.
- A `Paragraph` is sentences joined by single spaces.

A paragraph, the usual block of a mock-up, opens with `Lorem ipsum`. A
clause or a sentence, which usually sits mid-text, opens with it only
when made by `first`:

```
>>> str(Clause.first(40)).startswith('Lorem ipsum')
True
>>> str(Clause.first(15))
'Lorem ipsum....'

```

The lead-in is set by `isFirst`: `first` sets it on a clause or a
sentence, and a paragraph starts with it set. Set `paragraph.isFirst =
False` for a paragraph without it; the next read makes the new text.
A first clause too short for the lead-in and one word, as fifteen
characters, comes out as the lead-in cut short and filled with dots, so
the count still holds.

The smallest count differs: a clause that is not first needs room for
its shortest word, and below that `str()` raises `ValueError`; a
sentence or paragraph too short for its usual parts comes out as a
placeholder of the same count.


## 3. Repeatable text

The words and lengths are drawn from Python's `random`, so seeding it
repeats a text:

```
>>> import random
>>> random.seed(7)
>>> first = str(Paragraph(200))
>>> random.seed(7)
>>> str(Paragraph(200)) == first
True

```

That is the global generator your own code may use too, so seeding it
for a snapshot test seeds both.


## 4. Words of your own

A themed mock-up wants words of its own. A subclass of `StochasticWord`
lists them in `__category_weights__`, as pairs of a tuple of words and
the weight of each word in it; a clause takes them when its `stochWord`
box is declared over that subclass:

```
>>> from worktoy.desc import AttriBox
>>> from worktoy.lorem_ipsum import StochasticWord
>>> class Fruit(StochasticWord):
...   __category_weights__ = ((('fig', 'kiwi', 'apple', 'banana'), 1.0),)
>>> class FruitClause(Clause):
...   stochWord = AttriBox[Fruit]()
>>> text = str(FruitClause(20))
>>> len(text)
20
>>> set(text.split()) <= {'fig', 'kiwi', 'apple', 'banana'}
True

```

- The weight belongs to each word, so a longer list weighs more in
  total.
- The lengths must leave no gap between the shortest and the longest
  word, since any length in that range may be drawn; a gap raises
  `ValueError` at the class statement.
- `Fruit()[4]` and `Fruit().realizeLength(4)` give a word of length
  four, and `realize()` a word of any length.
- A subclass of `Clause` rebinding `__lead_in__`, as `('Hello',
  'world')`, opens its first clauses with words of its own.

Words of your own reach a clause. A sentence and a paragraph build their
clauses from `Clause` itself.


## 5. The distributions underneath

The lengths of clauses and sentences come from a `GaussianLengths`,
four numbers: a mean, a variance, and two bounds, both included. A
draw is a rounded Gaussian, clamped into the bounds:

```
>>> from worktoy.lorem_ipsum import GaussianLengths
>>> lengths = GaussianLengths(40, 15, 12, 70)
>>> 12 <= lengths.sampleInteger() <= 70
True
>>> parts = lengths.partition(300)
>>> sum(parts)
300
>>> all(12 <= part <= 70 for part in parts)
True

```

`partition(total)` cuts a total into values within the bounds;
`partitionSpaced(total, spacing)` cuts it so the values plus `spacing`
for each add up to it, which is how a clause pays for the spaces after
its words: it asks for its count plus one, since the last word has no
space after it. A total no number of values can reach raises
`ValueError`. A mean outside the bounds, or a negative variance, raises
`ValueError` too. `var` is the variance, not the standard deviation.

Each sentence holds its own `clauseDist`, and each paragraph its own
`sentenceDist`, so a project may retune the one it holds.
