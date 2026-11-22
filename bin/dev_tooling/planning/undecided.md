# Planned work: `UNDECIDED`

Brought up to date: 2026-11-22.

The items of planned work that stand at `UNDECIDED`: described, and the
author has not decided. `Next` holds the question.

The items are written by `item_template.md`, beside this file, and
`planned_items.md` lists the files of the other statuses. An item that
changes its status is moved, whole, to the file of the new one, under
the heading of its area.

## Warnings, deprecations and the next major version

---

### Confirm the other spellings of `index` as deprecated

`int(member)`, a member as a list index and `Kee.index` were deprecated
along with `index`, and were never confirmed one by one.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none
- Next: the author says yes or no to each of the three
- History:
  - 2026-11-11 UNDECIDED. Built as deprecated, in 1.2.0.

---

### Settle the names `RiskWarning` and `AlternativeWarning`

The two general warnings of the family carry names chosen while the
family was built.

- Status: UNDECIDED
- Level: unset
- Scale: small
- Release: none
- Next: the author keeps the names or gives others
- History:
  - 2026-11-11 UNDECIDED. Built with these names, in 1.2.0.

---

### Refuse a test class's own `doCleanups` or `debug` in 2.0

A proposal of the report on what 1.2.0 broke: refuse it at the line of
the class body in the next major version, and warn at most in 1.x.

- Status: UNDECIDED
- Level: major
- Scale: small
- Release: 2.0.0
- Next: the author says whether it is wanted
- History:
  - 2026-11-12 UNDECIDED. Proposed in the report.

## Overloads

---

### Settle what a subclass hides by declaring another kind of method

A subclass that declares an inherited overloaded name only as kinds of
method none of the nearer classes declares there hides what its base
declares, as a plain definition does. A subclass declaring only a
fallback of another kind therefore hides the overloads of its base.

- Status: UNDECIDED
- Level: unset
- Scale: small
- Release: none
- Next: the author says whether the rule stays, or a subclass keeps
  what its bases declare whatever kinds it declares itself
- History:
  - 2026-11-22 UNDECIDED. Seen while the two fallbacks were built.

## keenum

---

### Settle the default value of a combination of valued flags

A flags member defaults to its name. What a combination defaults to
when its flags declare values of their own, as `Kee[int](4)`, is not
settled.

- Status: UNDECIDED
- Level: unset
- Scale: small
- Release: none
- Next: the author says what the value is
- History:
  - 2026-11-11 UNDECIDED. The one open line of the plan of the rebuild.

---

### Confirm four choices of the keenum rebuild

Made while building, and never confirmed: a diamond of bases is one
member, and two objects under one name are refused; the name `owners`;
`KeeFlag` deprecated; `Kee[str]()` holds its name.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none; all four are in 1.2.0
- Next: the author says yes or no to each
- History:
  - 2026-11-11 UNDECIDED. Built as picked.

---

### Look over five consequences of the keenum rebuild

A `_getValue` of a subclass values only the members that subclass
builds. `NULL` is valued the text `NULL` in every class. `valueType` is
the type of the value of the first flag. A member of a subclass handed
to the call of the class is answered as it is. `&` of two unrelated
flags classes gives `NULL`, while `|` and `^` raise.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none; all five are in 1.2.0
- Next: the author says which, if any, is wrong
- History:
  - 2026-11-11 UNDECIDED. Found while building, and listed for him.

## ezdata

---

### Settle the receiver name `__ez_self__` of generated methods

The generated `__init__` and `replace` name their receiver
`__ez_self__`, so that a field may be named `self`.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none; the name is in 1.2.0
- Next: the author keeps the name or gives another
- History:
  - 2026-11-12 UNDECIDED. Chosen while the repair was built.

---

### Settle how a namespace class records its acting hook

A subclass of `EZHook` declared in a subclass of `EZSpace` acts in
place of the inherited hook, and the namespace class records which
hook acts. The shape of that record was chosen while building.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none; the record is in the builds of 1.2.1
- Next: the author keeps the shape or gives another
- History:
  - 2026-11-12 UNDECIDED. Chosen while building.

---

### Choose "attribute" or "field" for the prose of `ezdata`

Three lines say "attribute" on the author's word, to avoid confusion
with the class `Field`. The rest of the package says "field", as its
names do.

- Status: UNDECIDED
- Level: micro
- Scale: medium
- Release: none
- Next: the author says whether the rest follows
- History:
  - 2026-11-12 UNDECIDED. Three lines changed, the rest left.

---

### Unify the two rules for a default not of the field type

`AttriBox[int]('3')` gives 3, since a box builds its default through
the constructor. `EZField[int]('7')` is refused, since a field casts.

- Status: UNDECIDED
- Level: major
- Scale: small
- Release: none
- Next: the author says whether the two stay apart
- History:
  - 2026-11-10 UNDECIDED. A question of a newcomer reading the
    promises.

---

### Unify how the options of an `EZData` class inherit

`order` is inherited, `kwOnly` is not, and `frozen` must be declared
again by a subclass.

- Status: UNDECIDED
- Level: unset
- Scale: unsized
- Release: none
- Next: the author says whether the three stay as they are
- History:
  - 2026-11-10 UNDECIDED. A question of a newcomer reading the
    promises.

## work_test

---

### Decide whether `TestMeta` and `TestSpace` are deprecated

Since the repair of 1.2.1 `BaseTest` is not built by them. They stay
exported for a test base that chooses them.

- Status: UNDECIDED
- Level: minor
- Scale: small
- Release: none
- Next: the author says whether they are deprecated
- History:
  - 2026-11-12 UNDECIDED. Left open by the repair.

---

### Promise the three usages that 1.2.0 broke

A test base with a metaclass of its own, and a test class writing its
own `doCleanups` or its own `debug`, are tested and promised nowhere.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none
- Next: the author says whether they are promised
- History:
  - 2026-11-12 UNDECIDED. Left open by the repair.

## The promises and the manual

---

### Refuse or redirect `Parent.x.onSet` in the body of a subclass

Written in the body of a subclass, it registers on the box of the
base, so a write on an instance of the base fails for want of the
method. `THIS[Parent].x.onSet` is the way that works.

- Status: UNDECIDED
- Level: unset
- Scale: unsized
- Release: none
- Next: the author says whether it is refused or left
- History:
  - 2026-11-10 UNDECIDED. A question of a newcomer reading the
    promises.

---

### Notice a misspelled class keyword

A keyword in a class statement that nothing reads is dropped without a
word. A forwarded keyword and a misspelled one cannot be told apart,
and a guard around `__init_subclass__` is ruled out.

- Status: UNDECIDED
- Level: unset
- Scale: unsized
- Release: none
- Next: the author; it is his standing question
- History:
  - 2026-10-19 UNDECIDED. Listed as the author's open question.

---

### Promise the fallback for each way of reaching a name

1.2.3 lets a name hold an instance bound fallback and a class bound
one, and the changelog says so. Nothing in `design` promises it, and
the manual does not show it. The promise of several kinds at one name
says a staticmethod is not considered through an instance where the
name has a bound method, which is loose for a name whose only bound
method is its fallback.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none
- Next: the author says whether it is promised, and from which version
- History:
  - 2026-11-22 UNDECIDED. Left out of the promises when it was built.

---

### Rewrite the package parts of the manual in the voice of the README

The manual opens with the README and goes on from its class. The ten
parts after that opening, one for each package, read as the chapters
did before they were joined: written to state what is promised, not to
answer what a curious reader would ask.

- Status: UNDECIDED
- Level: micro
- Scale: large
- Release: none
- Next: the author says whether, and with which package to begin
- History:
  - 2026-11-22 UNDECIDED. The opening was rewritten on his word; the
    parts were left as they were.

---

### Point the README to the manual, and settle what the manual repeats

The README does not say that the manual exists. The manual begins with
the README whole, so it repeats the sections on contributing and the
license, with two links that do not resolve from inside `design`.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none
- Next: the author says whether the README points to the manual, and
  whether the copy ends before the section on contributing
- History:
  - 2026-11-22 UNDECIDED. Noted when the README was placed at the top
    of the manual.

## Testing and mutation testing

---

### Add contract, property and differential tests

A plan of 2026-06-08: one invariant run across the family of boxes,
property tests with `hypothesis` for the dispatcher, and tests against
CPython for `resolveMRO`, slices and `isinstance`. The suite went
another way in November 2026, to full branch coverage and Cosmic Ray,
and holds none of the three.

- Status: UNDECIDED
- Level: none
- Scale: large
- Release: none
- Next: the author says whether they are wanted beside the sweeps
- History:
  - 2026-06-08 UNDECIDED. Proposed in a hand-off, and never taken up.

---

### Narrow the `except TypeError` of the exact-match lookup

`src/worktoy/dispatch/_dispatcher.py`, line 801. It is written for an
argument whose class cannot be hashed, and would also hide a defect
inside the lookup.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none
- Next: the author says whether it is narrowed
- History:
  - 2026-11-06 UNDECIDED. Left to the author when the tests were
    written anew.

---

### Remove five small redundancies from the source

`True` and `False` beside `1` and `0` in the cast to `bool`, the
shortcut for a single base in `resolveMRO`, the two-word branch of
`joinWords`, the early check for an empty slot in `bipartiteMatching`,
and the filler value of `Arrangement.inverse`.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none
- Next: the author says which go
- History:
  - 2026-11-06 UNDECIDED. Pointed at by the mutation sweeps.

---

### Sweep `dispatch` and `mcls` whole

The sweeps of 1.2.3 ran over the files whose code changed, each whole.
The two packages as a whole were last swept on 2026-11-06, before
several kinds of method and the two fallbacks changed how their files
work together.

- Status: UNDECIDED
- Level: none
- Scale: medium
- Release: none
- Next: the author says whether both are swept whole before 1.3.0
- History:
  - 2026-11-22 UNDECIDED. Left undone in each sweep of 1.2.3.

## Reviews of the source

---

### Add a root `CLAUDE.md` with the rule on reading the core

The rule that `core`, `dispatch`, `desc` and `mcls` are read whole in
every session is kept in notes outside the repository. A file at the
root would put it into the repository.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none
- Next: the author says whether he wants it
- History:
  - 2026-11-12 UNDECIDED. Offered, and not answered.

## The documentation

---

### Build the docs against markwork pre-releases at dev and rc presses

`docs/requirements.txt` asks for `markwork>=0.1.0`, a floor and no
pin, and neither the lts workflows nor Read the Docs install
pre-releases. A dev or rc build of markwork therefore never reaches
the docs of worktoy, and the first time a new markwork meets them is a
release. A step in the dev and rc workflows would install the
requirements, then `pip install --pre --upgrade markwork`, markwork
alone so that no pre-release of Sphinx or furo comes along, build the
pages and throw them away. Nothing is published and neither site is
touched. It costs one build of about a minute at each press, and it
fails a press when a markwork pre-release breaks the pages, which is
the warning it is for. The pages could also be kept as an artifact of
the run, to be opened by hand.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none
- Next: the author decides, once it is clearer where markwork goes;
  the workflow files are his to edit
- History:
  - 2026-11-13 CONCEPTION. The author asked whether the dev and rc
    workflows could install markwork with `--pre`.
  - 2026-11-13 UNDECIDED. Described; the author has not decided what
    to do in markwork.

---

### Publish a nightly view of the docs from dev and rc builds

A view of the docs as they stand on `main`, beside the released ones,
built with the newest markwork. Each of the two sites has a way, and
each way runs against a decision that stands. Read the Docs has the
version `latest`, which follows the default branch and rebuilds at
every push; it is switched off on purpose, and its builds do not see a
workflow flag, so `--pre` for that view alone would go into
`.readthedocs.yaml` behind a test of the version being built. GitHub
Pages knows no versions: the lts job builds one folder for each
release, and a `nightly` folder would be one more, but the deploy
replaces the whole site, so a dev press would have to build every
version again, more than ten minutes at seven of them, or the deploy
would have to change to one that replaces a single folder.

- Status: UNDECIDED
- Level: none
- Scale: medium
- Release: none
- Next: the author decides whether a nightly view is wanted at all;
  it would take back one of the three decisions above
- History:
  - 2026-11-13 CONCEPTION. The author asked whether the two sites
    support a nightly view.
  - 2026-11-13 UNDECIDED. Described, with what each way would undo.

---

### Put the docs of dev and rc builds on `latest` at Read the Docs

Read the Docs already has a place for docs that are ahead of the
release: its version `latest`, beside `stable` and the versions of the
tags. The docs of the dev and rc builds would go there, built with the
newest markwork, pre-releases included, while `stable` and the tags
stay as they are. How that is brought about is left open.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none
- Next: the author decides; `latest` is switched off there today, on
  purpose
- History:
  - 2026-11-13 CONCEPTION. The author's idea, from the talk about a
    nightly view.
  - 2026-11-13 UNDECIDED. Named, without the how.

---

### Bound the markwork version the docs install

With the floor alone, the next lts press and every rebuild at Read the
Docs take the newest stable markwork of that day. A stable markwork
that changes what it asks of its host would then break the docs of
worktoy at a release, or at Read the Docs with no press at all. An
upper bound in `docs/requirements.txt`, as `markwork>=0.1.0,<0.2`,
keeps the docs on the line they were built with until the bound is
raised by hand. The cost is that a fix in a newer line of markwork no
longer arrives by itself.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none
- Next: the author decides, with the plans for markwork; it matters
  only once a stable markwork breaks its contract with the host
- History:
  - 2026-11-13 CONCEPTION. Noticed while checking what the docs job
    of the first `micro-lts` run installed: `0.1.1`, the newest
    stable.
  - 2026-11-13 UNDECIDED. Described.
