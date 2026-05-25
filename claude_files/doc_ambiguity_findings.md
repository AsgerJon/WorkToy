# Documentation Ambiguity Findings — worktoy

Working tracker for the documentation-only ambiguity review. Goal: every
promise/claim the docs make is precise, terms are used consistently, and
checkable claims match the code. We take these ONE AT A TIME.

## How to read an entry

- **ID** — stable handle (C/H/M/L = Critical/High/Medium/Low tier).
- **Status** — `TODO` / `IN PROGRESS` / `DONE` / `WONTFIX`.
- **Kind** — what the fix touches:
  - `docstring` — pure triple-quoted text in src/ or tests/ (safe; within
    the hard constraints, no code lines change).
  - `readme` — README.md / top-level prose.
  - `code-bug` — the doc is wrong because the CODE is wrong; REPORT ONLY,
    do not change code this pass. The docstring fix (describe actual
    behavior) is still a `docstring` edit.
  - `pipeline` — docs build machinery (docs/_gen.py, conf.py, index.rst);
    release-critical, get approval before changing.
  - `decision` — needs a call from Asger before touching.
- **Confidence** — `[verified]` (I read the code / ran it) or `[agent]`
  (sub-agent reported against cited lines; not independently re-run).
- **CODE DELIVERS** — does the code currently back the (corrected) claim?

## Hard constraints (do not violate while fixing)

- src/ and tests/: ONLY triple-quoted docstring text may change. Never
  touch imports, annotations, signatures, logic. When deleting a
  docstring, don't let the edit run onto the next code line.
- If a promise is wrong because the code is wrong: report it, fix the
  docstring to match reality, do NOT fix the code this pass.
- docs/ machinery + README are editable, but propose pipeline changes
  before making them.
- Style on every rewrite: NumPy style, <=77-char lines, 2-space indent,
  no em-dashes, no double-backtick markup, plain vocabulary, expand
  TypeAlias types. Clarity first, style second.

---

## Progress checklist

Critical
- [x] C1  THIS sentinel: contradictory meaning (class vs instance)
- [x] C2  KeeFlags "any order" + dangling __getattr__ + nonexistent FULL
          (+ found/fixed: flags-vs-highs conflation)
- [x] C3  KeeNum cls[int] is positional index, not value lookup
- [x] C4  Kee: non-uppercase keys "treated as ordinary attrs" is false
- [x] C5  DescriptorException: nonexistent routing; siblings don't inherit
- [x] C6  mcls __prepare__ "removes nothing from bases" but strips Generic
- [x] C7  mcls LoadSpaceHook references nonexistent DescLoad
- [x] C8  mcls _notifySubclassHook overstates contract
- [x] M21 mcls __init__ docstring "metaclass validates the 'dict' object"
          before type.__new__ -- no such validation step (NEW, found in C8)
- [x] C9  textFmt documented example is wrong
- [x] C10 work_test SubTest claims to subclass BaseTest (it's TestCase)

High
- [x] H1  dispatch Dispatcher "three tiers" but code runs five
- [x] H2  dispatch Dispatcher.flex "any type signature" / fallback
- [x] H3  dispatch overload.flex attributes permutation to dispatcher
- [x] H4  dispatch flexCall ignores keyword-only requirements
- [x] H5  desc AttriBox class docstring omits cast-vs-raise contract
- [x] H6  desc FixBox "only change" hides that delete is disabled
- [x] H7  desc Field @SET/@DELETE copied getter wording (wrong)
- [x] H8  core ExceptionInfo "each outcome" misses two outcomes
- [x] H9  work_io PathSyntaxException missing from Raises; strict= undoc
- [x] H10 work_io FidGen.__get__ docstring copied from Dispatcher
- [x] H11 lorem_ipsum scaleSum direction inverted + maxIndex off-by-one
- [x] H12 work_test samplers: stale gen, wrong cardinality, wrong attrs
- [x] H13 tests: docstrings name nonexistent modules / invert assertions

Medium
- [x] M1  KeeFlag "is itself an enumeration" vs "instances are not members"
- [x] M20 KeeFlag "Attributes" section frames flag attrs as member attrs;
          lists a 'value' attr KeeFlag does not implement (NEW, found in C2)

NOTE: Medium tier all DONE 2026-05-25 (docstring-only; verified against
code; full worktoy import OK). Per-item "## Mn" detail blocks keep the
original finding text; their Status lines were not individually flipped
to save churn -- this checklist is authoritative.

CODE BUGS FOUND:
- tests/test_keenum/test_kee_meta_resolve.py nameContract: built case
  variants (lowerCase/shuffleCase/upperCase) but the inner loop used
  'names' not the variant, so case-insensitive resolution was never
  actually tested. FIXED (per Asger): inner loop now iterates the
  variant; loop var renamed 'case'->'variant' and 'cases'->'variants'
  to avoid the match/case soft-keyword. Verified the corrected logic
  passes across all 18 example enums (672 assertions); docstring now
  describes the case-insensitive testing. (Asger to run full pytest.)
- work_io/_fid_gen.py next(): raises 'RecursionError' when all candidate
  filename slots are taken (odd exception choice). REPORT-ONLY, not
  fixed; noted under H10.
- [x] M2  dispatch addVariadicSigFunc silent on duplicates / ARGS
- [x] M3  dispatch fallback/finalize edge cases
- [x] M4  desc BaseDescriptor callback order/duplicates
- [x] M5  desc Field @GET "decorate one method"
- [x] M6  core parseKwargs omits wrong-type raise
- [x] M7  core hookPreSet/hookOnSet identical "just set" wording
- [x] M8  mcls pre/postCompilePhase lifecycle reversed in time
- [x] M9  mcls __init__ claims type.__init__ triggers __set_name__ etc.
- [x] M10 mcls AbstractSpaceHook.__get__ sets spaceClass (it doesn't)
- [x] M11 mcls getItemPhase -> bool / "returns False"
- [x] M12 mcls setItemHook named method does not exist
- [x] M13 mcls BaseMeta says hooks "defined in BaseSpace"
- [x] M14 mcls __getitem__ fallback doesn't exist
- [x] M15 ezdata mutable defaults "fresh copy" is shallow
- [x] M16 ezdata MRO "later-MRO wins" inverted
- [x] M17 keenum exceptions: vague trigger + missing attribute docs
- [x] M18 work_io newDirectory NotADirectoryError trigger wrong
- [x] M19 tests: docstrings undersell/mislabel what is asserted

Low / cosmetic
- [x] L1  README grammar + inline triple-backticks (incl. version header)
- [x] L2  desc __init__ "descriptor-context" announced, never defined
- [x] L3  core DELETED "should raise" imperative phrasing
- [x] L4  core Object self-referential "See 'Object'"
- [x] L5  core MetaType "base on this class" non-standard
- [x] L6  waitaminute MissingVariable expectedTypes documented singular
- [x] L7  waitaminute ControlClassError "only __str__/__repr__"
- [x] L8  utilities ValidSlice "defines __index__" (not invoked)
- [x] L9  utilities Directory "owner class" vs concrete class module
- [x] L10 waitaminute DuplicateSignature NumPy heading "Arguments"
- [x] L11 mcls __bool__ Dante excerpt -- KEPT as deliberate flair
          (Asger confirmed: keep it). Fallback behavior is documented
          in the class hook table, so the poem costs nothing. Do NOT
          remove it in future doc cleanups.

Low tier DONE 2026-05-25 (docstring/README prose; full import OK), except
L11 left as flair by decision. Backticks are allowed in markdown (README)
per Asger; L1 inline ```triple``` -> `single` and grammar fixed.

Decisions / pipeline (need Asger)
- [x] D1  setAnnotationPhase documented but never dispatched (PEP work)
- [x] D2  index.rst "Every source file" false (option a; _kee_num.py
          still not rendered -- option b deferred)

---

# CRITICAL

## C1 — THIS sentinel: contradictory meaning
- Status: DONE (sentinel docstrings + README overload comment fixed)
  | Kind: docstring (+readme) | Confidence: [verified]
- RESOLVED with Asger's authoritative explanation + this_box_example.py
  (100% branch coverage): THIS = placeholder for the 'instance' arg of
  '__get__' (and the enclosing class in '@overload' signatures, matching
  instances of it); OWNER = placeholder for the 'owner' arg of '__get__',
  used by AttriBox, no role in overloading. Backing code:
  'core/_object.py:147-185' getContextualSentinels maps THIS->instance,
  OWNER->owner, DESC->self.
- EDITS: `_this.py` module + class docstrings rewritten;
  `sentinels/__init__.py` THIS/OWNER bullets aligned (also fixed
  '@Overload' -> '@overload'); `_owner.py` already correct, untouched.
- README: both '@overload(THIS)' comments now read "THIS = the enclosing
  class (matches an instance of it)". Rationale (per Asger): OWNER is
  pointless in overloads since you can name the metaclass directly to
  match the class object, so overload docs mention THIS only.
- AttriBox side (per Asger): the AttriBox class docstring
  (`_attri_box.py:25`) now documents that a deferred default may contain
  THIS / OWNER / DESC, substituted when the field is built with the
  active '__get__' instance / owner / descriptor. DESC sentinel
  (`_desc.py`) and FastBox's "sacrificed" list (`_fast_box.py:11`) were
  already consistent.
- Files: `src/worktoy/core/sentinels/_this.py:19-21`
  vs `src/worktoy/core/sentinels/__init__.py:16-18`
  (README echoes the wrong one at README.md:145, 216)
- CLAIM (`_this.py`): "THIS is the sentinel object representing the class
  currently under construction. Similar to the 'self' keyword, it is used
  to refer to the class being defined."
- CLAIM (`__init__.py`): "THIS: ... to specify an instance of the class.
  Similar to 'typing.Self'." and "OWNER: Similar to THIS, but specifying
  the class itself, rather than an instance of it."
- WHY: The two disagree on whether THIS is the class or an instance of the
  class. `_this.py` likens it to `self` (an instance) while calling it
  "the class," which is incoherent; and if THIS meant "the class itself"
  it would be redundant with OWNER.
- REWRITE (`_this.py` docstring):
  ```
  THIS is a placeholder for the enclosing class, used inside a
  class body before that class exists. In '@overload(THIS, ...)'
  and 'AttriBox[THIS](...)' it stands for an instance of the
  class being defined, analogous to 'typing.Self'. Use 'OWNER'
  when you mean the class object itself. THIS is replaced by the
  real class once the class body has compiled.
  ```
- CODE DELIVERS: `__init__.py`/OWNER wording is correct; `_this.py` wrong.
  unsure on exact "instance vs class-as-type" phrasing; contradiction is
  definite.

## C2 — KeeFlags "any order" + dangling __getattr__ + nonexistent FULL
- Status: DONE | Kind: docstring (code-bug adjacent) | Confidence: [verified]
- EDITS (all docstring-only, re-verified by running FileAccess):
  - `_kee_flags.py` intro: grammar + "members" (not "enumerations").
  - `_kee_flags.py` "Flags and Names" -> "Flags, Highs, Lows, and Names":
    FIXED a conflation found during this pass: 'flags' returns ALL
    class flags (mirrors class-level 'flags'), the HIGH ones are
    'highs', LOW are 'lows', HIGH names are 'names'. The old text
    wrongly said 'flags' returns only the HIGH flags.
  - `_kee_flags.py` "Flexibility" -> "Resolution and naming": attribute
    access = canonical name only (reordered name raises; no
    '__getattr__'); subscript/call = order- and case-insensitive,
    duplicates collapse, unknown raises 'KeyError'.
  - `_kee_flags.py` class "Important attributes" -> "Member attributes":
    accurate flags/highs/lows/names/index/value/name list.
  - `_kee_flag.py` module + class openings: dropped the nonexistent
    'FULL' member and the "is itself an enumeration" claim (also M1).
- CODE NOTE (unchanged, for Asger): reordered ATTRIBUTE access does not
  resolve because KeeFlagsMeta has no '__getattr__'. Docs now match the
  code; if order-insensitive attribute access is wanted, that is a code
  change, out of scope.
- Files: `src/worktoy/keenum/_kee_flags.py:37-45` (module),
  `_kee_flags.py:1-6, 42-46` and `_kee_flag.py:5, 45` (the FULL claim)
- CLAIM: "member resolution via 'KeeFlagsMeta.__getitem__' and
  'KeeFlagsMeta.__getattr__' accepts any order: passing a string like
  'EXECUTE_READ', a tuple/frozenset like ('READ', 'EXECUTE'), or a
  sequence of separate names all resolve to the same member." ... "the
  'KeeFlags' populate the enumeration with the 'NULL' enumeration, the
  'FULL' enumeration and all possible combinations".
- WHY (all confirmed by running):
  - `KeeFlagsMeta` has NO `__getattr__`; it inherits
    `AbstractMetaclass.__getattr__`, which raises `MissingVariable` when
    `__class_getattr__` is unset (it is). `FileAccess.EXECUTE_READ`
    (reversed) raises `MissingVariable`. Only the canonical
    declaration-order name resolves by attribute.
  - Subscript/call DO accept any order, ARE case-insensitive
    (`cls['execute_read']` works), and collapse duplicates
    (`cls['READ','READ']` -> READ). Unknown names raise `KeyError`. None
    of this is stated.
  - There is NO member named `FULL` (`FileAccess.FULL` raises
    `MissingVariable`); the all-high member is named by joined flags. Only
    `NULL` is auto-named.
- REWRITE (module docstring "Flexibility" section):
  ```
  The canonical attribute name is built in declaration order, so
  attribute access resolves only that exact name
  ('FileAccess.READ_EXECUTE', not 'FileAccess.EXECUTE_READ').
  Subscripting and calling are order-insensitive and
  case-insensitive: 'cls["EXECUTE_READ"]', 'cls["execute_read"]',
  'cls[("READ", "EXECUTE")]', and 'cls["READ", "EXECUTE"]' all
  resolve to the same member, and a repeated name collapses
  ('cls["READ", "READ"]' resolves to READ). An unknown name
  raises 'KeyError'.
  ```
  In `_kee_flags.py` / `_kee_flag.py`: drop "the 'FULL' enumeration"; the
  only auto-named member is `NULL`.
- CODE DELIVERS: subscript-any-order yes; `__getattr__` any-order NO
  (`_kee_flags_meta.py` has no `__getattr__`;
  `_abstract_metaclass.py:299-307`); `FULL` member NO (`_kee_flags.py:203`).
- NOTE: if order-insensitive ATTRIBUTE access is actually desired, that is
  a code change (out of scope this pass); flag to Asger.

## C3 — KeeNum cls[int] is positional index, not value lookup
- Status: DONE | Kind: docstring + code (authorized) | Confidence: [verified]
- RESOLVED: KeeMeta "Member resolution" docstring now states the real
  contract (verified by running Weekday + a collision fixture Coll):
  'cls(i)' = value-only resolution; 'cls[i]' for a non-bool int first
  does positional indexing into the member sequence (negatives allowed)
  and falls back to value resolution when out of range; the index path
  wins on collision, so 'cls[2]' and 'cls(2)' can differ. bool excluded;
  name lookup case-insensitive. Matches Asger's "index with value
  fallback" recollection; this is the tested (100% branch) behavior, so
  documented as-is. Pure-value subscript would be a code change (not
  this pass).
- Other catalogued-confidence lines in the old block were unconditional
  (name/value steps) and are now gated by their type conditions.
- CODE FIX (per Asger; authorized exception to the doc-only rule):
  final order in 'KeeMeta._resolveMember' is identity -> name ->
  __class_resolve__ -> index (when 'allowIndex=True') -> value ->
  raise. Identity and name resolution bypass the hook; the hook
  precedes index and value. '__getitem__' is now just
  'return cls._resolveMember(identifier, allowIndex=True)'. Class
  docstring "Member resolution" rewritten to match. (Asger revised the
  order twice; original code was identity -> name -> hook -> value with
  the index shortcut in '__getitem__' ahead of the hook.)
- Risk: low. Enums without a hook and 'cls(...)' calls behave as before
  (identity/name still first); the hook only changes resolution for
  enums that DEFINE it, and only for identifiers that are neither a
  member nor a name match.
- Verified (PYTHONPATH=src): with a hook that claims everything,
  identity and name still win (IdTest(IdTest.A)=A, IdTest['A']=A) while
  the hook beats index/value (IdTest[0]=C, IdTest[5]=C); the three
  existing __class_resolve__ scenarios hold (Sus[0..2]=A,B,C; Cardinal
  tuple/raise; Polar bool); no-hook Coll[2]=C vs Coll(2)=A, identity
  Coll(Coll.B)=B, name Coll['A']=A.
- Saved design intent: memory project_keenum_class_resolve_precedence.
- PENDING: full 'pytest' in worktoy_env (Asger to run, outside sandbox).
- File: `src/worktoy/keenum/_kee_meta.py:96-108` (KeeMeta class docstring)
- CLAIM: "'cls(identifier)' and 'cls[identifier]' both call
  '_resolveMember', which tries in order: 1. identity 2. case-insensitive
  name lookup 3. ... 4. value lookup".
- WHY: `__getitem__` (`_kee_meta.py:339-349`) shortcuts a non-bool `int`
  to `cls.members[i]` (positional index) BEFORE `_resolveMember`.
  Verified with values 10/20/30: `Weekday[1]` -> TUE (position 1),
  `Weekday[20]` -> TUE (by value), and `Weekday(1)` raises KeeResolveError
  (no member with value 1). So `cls(i)` and `cls[i]` are NOT equivalent,
  and `cls[int]` is not "value lookup."
- REWRITE:
  ```
  'cls(identifier)' resolves via '_resolveMember', trying in
  order: identity, case-insensitive name (str only), a
  '__class_resolve__' hook if present, then value lookup for an
  identifier of the member value type; failing all of these
  raises 'KeeResolveError'. 'cls[identifier]' behaves the same
  EXCEPT that a non-bool 'int' is first treated as a positional
  index into the member sequence ('cls[0]' is the first member);
  an out-of-range int falls through to '_resolveMember'.
  ```
- CODE DELIVERS: NO for the subscript claim (`_kee_meta.py:341-348`).

## C4 — Kee: non-uppercase keys "treated as ordinary attrs" is false
  (renumbered from C5 to match Asger's notebook)
- Status: DONE | Kind: docstring | Confidence: [verified]
- RESOLVED: `_kee_member.py` name bullet now states the rule is
  enforced (a lowercase OR mixed-case 'Kee' raises 'KeeCaseException'
  at class creation; only non-'Kee' entries stay ordinary attributes).
  Verified by running Bad / Mixed / Good fixtures.
- File: `src/worktoy/keenum/_kee_member.py:7-12`
- CLAIM: "Names ... must be uppercase. The uppercase requirement is
  enforced (not merely convention). Class-body entries whose key is not
  uppercase are treated as ordinary class attributes rather than
  enumeration members."
- WHY: `KeeSpaceHook.setItemPhase` routes EVERY `Kee` to `addNum`
  regardless of key case (`_kee_space_hook.py:48-50`); `addNum` sets
  `member.name`, whose setter raises `KeeCaseException` for any
  non-uppercase name (`_kee_member.py:113-116`). A lowercase-keyed `Kee`
  RAISES at class creation; it is not silently demoted. The two sentences
  contradict each other.
- REWRITE:
  ```
  Names must be unique within an enumeration and must be
  uppercase. The uppercase rule is enforced: assigning a 'Kee'
  to a non-uppercase name raises 'KeeCaseException' when the
  class is created. (Non-'Kee' class-body entries are unaffected
  and remain ordinary class attributes.)
  ```
- CODE DELIVERS: NO (`_kee_space_hook.py:48`, `_kee_space.py:51`,
  `_kee_member.py:115-116`).

## C5 — DescriptorException: nonexistent routing; siblings don't inherit
  (renumbered from C4 to match Asger's notebook)
- Status: DONE | Kind: docstring | Confidence: [verified]
- RESOLVED (docstring-only): removed the fictional "Object recognises a
  descriptor exception and propagates it rather than routing to a
  fallback accessor" claim (no 'except DescriptorException' and no
  fallback mechanism exist anywhere in src; only 'except's in
  '_object.py' are TypeError/SkipSet/AttributeError). Replaced the
  "catches every descriptor failure" / "every exception here subclasses
  DescriptorException" overclaims with the truth: AccessError /
  ProtectedError / ReadOnlyError share the base; WriteOnceError
  (TypeError) and WithoutException (RuntimeError) do NOT. Fixed in
  '_descriptor_exception.py' (module + class), '__init__.py', and the
  related overclaim in '_read_only_error.py' ("the shared base for
  descriptor failures" -> "a shared base for several of the descriptor
  exceptions"). Inheritance verified by import.
- Files: `src/worktoy/waitaminute/desc/_descriptor_exception.py:17-24`
  and `src/worktoy/waitaminute/desc/__init__.py:4-7`
- CLAIM: "Catching this one type catches every descriptor failure. The
  shared base also lets 'Object' tell a deliberate descriptor exception
  apart from an incidental one: a 'DescriptorException' propagates to the
  caller rather than being routed to a fallback accessor."
- WHY: grep finds ZERO `except DescriptorException` anywhere; no
  "fallback accessor" routing exists. `WriteOnceError(TypeError)` and
  `WithoutException(RuntimeError)` are exported from this same package but
  do NOT subclass `DescriptorException`, so "catches every descriptor
  failure" is false.
- REWRITE (`_descriptor_exception.py`):
  ```
  Base class for the descriptor write/delete exceptions
  'AccessError', 'ProtectedError', and 'ReadOnlyError'. Note that
  'WriteOnceError' (a 'TypeError') and 'WithoutException' (a
  'RuntimeError') are related descriptor errors that do NOT
  inherit from this class, so a bare 'except DescriptorException'
  does not catch them.
  ```
  Apply the same correction to `desc/__init__.py:4-7`.
- CODE DELIVERS: NO (`_write_once_error.py:15`, `_without_exception.py:17`;
  no `except DescriptorException` in core/, desc/).

## C6 — mcls __prepare__ "removes nothing from bases" but strips Generic
- Status: DONE | Kind: code (authorized) | Confidence: [verified]
- CORRECTION to the original finding: my cataloged rewrite ("strips
  Generic so it does not appear in the resulting class's bases") was
  ITSELF wrong. Investigation showed the strip was vestigial:
    * '__new__' builds the class from the ORIGINAL bases, so the class
      keeps Generic regardless (Foo.__bases__ has Generic; Foo[int]
      works). The strip only ever touched the namespace object.
    * every concrete metaclass (BaseMeta, KeeMeta, KeeFlagsMeta, EZMeta)
      overrides '__prepare__' WITHOUT the strip, so it never ran for any
      real worktoy class.
    * not version-gated; not a Python 3.7 concern (pre-3.7 Generic had
      GenericMeta, but worktoy is 3.7+ where Generic is metaclass-free).
    * no test passes 'Generic' (grep: zero 'Generic' in tests/).
- RESOLUTION (Asger chose "remove the strip"): deleted the
  'bases = [b for b in bases if b is not Generic]' line and dropped the
  now-unused 'Generic' import from '_abstract_metaclass.py'. The
  existing docstring ("removes nothing ... subclasses should also remove
  nothing") is now TRUE, so it was left unchanged.
- Verified (PYTHONPATH=src): full import OK; BaseObject+Generic[T] and
  direct AbstractMetaclass+Generic[T] both construct; namespace now
  consistent with class bases.
- PENDING: full 'pytest' in worktoy_env (Asger to run, outside sandbox).

## C7 — mcls LoadSpaceHook references nonexistent DescLoad
- Status: DONE | Kind: docstring | Confidence: [verified]
- RESOLVED (docstring-only): module, class, and 'postCompilePhase'
  docstrings rewritten to describe the real behavior, verified against
  the code: 'setItemPhase' collects 'overload' instances (routing
  signatures, variadics, fallback, finalizer onto the namespace) and
  'postCompilePhase' assembles one 'Dispatcher' per overloaded name
  into the compiled namespace. 'DescLoad' gone everywhere (grep); import
  OK.
- File: `src/worktoy/mcls/space_hooks/_load_space_hook.py:2, 24, 55`
- CLAIM: "LoadSpaceHook collects DescLoad instances encountered in the
  class body ..." (module + class + method docstrings)
- WHY: `DescLoad` exists nowhere; the hook collects `overload` instances
  and assembles `Dispatcher` objects. Stale name.
- REWRITE: "LoadSpaceHook collects the 'overload' instances declared in
  the class body and assembles one 'Dispatcher' per overloaded name in the
  compiled namespace."
- CODE DELIVERS: NO (hook uses overload/Dispatcher).

## C8 — mcls _notifySubclassHook overstates the contract
- Status: DONE | Kind: docstring | Confidence: [verified]
- RESOLVED (docstring-only): the 'mcls/__init__.py' sentence now says the
  metaclass CALLS '__subclasshook__' on each base (not "checks for
  presence"), the return value is ignored (so a base cannot modify the
  class), and a base can only reject by raising. Import OK.
- SPOTTED nearby (logged as M21, not fixed here): the same docstring
  still claims the metaclass "validates the 'dict' object" before
  'type.__new__'; there is no such step.
- File: `src/worktoy/mcls/__init__.py:14-18`
- CLAIM: "the metaclass checks each baseclass for the presence of a method
  called '__subclasshook__'. If it exists, the method is called ...
  allowing the baseclass to modify or even reject the class."
- WHY: `_notifySubclassHook` calls `base.__subclasshook__(cls)`
  unconditionally (every object inherits one) and DISCARDS the return
  value (`_abstract_metaclass.py:327-329`). It cannot "modify" the class;
  rejection only by raising.
- REWRITE:
  ```
  Before returning the class, the metaclass calls
  '__subclasshook__(cls)' on each base. This is notification
  only: the return value is ignored, and every class inherits
  '__subclasshook__' from 'object' so the call always happens. A
  base can reject the new class by raising from that method.
  ```
- CODE DELIVERS: NO (`_abstract_metaclass.py:324-329`).

## C9 — textFmt documented example is wrong
- Status: DONE | Kind: docstring | Confidence: [verified — ran it]
- RESOLVED (docstring-only): replaced the single wrong example
  (claimed 'first line,\\nsecond line\\n  indented', actually
  'first line, \\nsecond line   indented') with two certified examples:
  textFmt('many    spaces   here') -> 'many spaces here' (collapse) and
  textFmt('paragraph<br><tab>indented line') -> 'paragraph\\n  indented
  line'. Both asserted against live output; kept the original '\\n'
  source escaping. Avoided a literal newline in the example input to
  keep the verbatim-rendered page unambiguous.
- File: `src/worktoy/utilities/_text_fmt.py:53-54`
- CLAIM: `textFmt('first line, <br>second line', '<tab>indented')` ->
  `'first line,\nsecond line\n  indented'`
- WHY: actual output is `'first line, \nsecond line   indented'` — the
  space before `<br>` is preserved, and `<tab>` in a separate argument
  inserts two spaces inline (args are space-joined first), not a
  newline+indent.
- REWRITE:
  ```
  Examples
  --------
  >>> textFmt('line one<br>line two')
  'line one\nline two'
  >>> textFmt('first<br><tab>indented')
  'first\n  indented'
  ```
- CODE DELIVERS: NO (ran all three; corrected examples verified).

## C10 — work_test SubTest claims to subclass BaseTest (it's TestCase)
- Status: DONE | Kind: docstring | Confidence: [verified]
- RESOLVED (docstring-only): module + class docstrings corrected.
  SubTest subclasses 'unittest.TestCase' (for assert methods), NOT
  'BaseTest' -- deliberately: it is the per-instance accumulator /
  context manager that 'BaseTest' hosts as the 'subTest' descriptor
  ('_base_test.py:105'), built lazily in '__get__', records pass/fail
  (AssertionError)/error per context block, and 'BaseTest.tearDown'
  fails the test if any sub-test failed. Subclassing BaseTest would be
  circular (BaseTest embeds a SubTest) and wrongly make it a
  discovered/runnable test. Verified: issubclass(SubTest, TestCase)
  and not issubclass(SubTest, BaseTest).
- File: `src/worktoy/work_test/_sub_test.py:2, 23`
- CLAIM: "SubTest subclasses BaseTest and provides a locally instantiated
  sub test."
- WHY: `class SubTest(TestCase)` — `issubclass(SubTest, BaseTest)` is
  False.
- REWRITE: "SubTest subclasses 'unittest.TestCase' directly and acts as a
  locally instantiated sub-test accumulator used by 'BaseTest'."
- CODE DELIVERS: NO (`_sub_test.py:22`).

---

# HIGH

## H1 — dispatch Dispatcher "three tiers" but code runs five
- Status: DONE | Kind: docstring | Confidence: [verified]
- VERIFIED by reading the compiled 'dispatch' fn (_dispatcher.py:158-249):
  FASTEST, FAST-concrete, FAST-variadic, SLOW-concrete, SLOW-variadic,
  then fallback. RESOLVED: Dispatcher "Dispatch tiers" section rewritten
  to "five ordered passes" grouped as three kinds (FASTEST/FAST/SLOW,
  FAST and SLOW each concrete-then-variadic), with the full order and
  the "behaves as three tiers when no variadic overloads" note. Aligned
  '_overload.py' summary vocabulary ("three kinds of pass", dropped
  "tier"). Import OK.
- Files: `src/worktoy/dispatch/_dispatcher.py:39` (and `_overload.py:60`)
- CLAIM: "Calls go through up to three resolution tiers" (FASTEST/FAST/SLOW).
- WHY: two extra variadic passes exist (FAST-variadic
  `_dispatcher.py:175-193`, SLOW-variadic `:214-245`); that is how an
  overlong call still matches.
- REWRITE: enumerate five passes (FASTEST, FAST-concrete, FAST-variadic,
  SLOW-concrete, SLOW-variadic); note the variadic passes are empty unless
  an 'ARGS'-terminated overload is registered, so with none it behaves as
  three tiers.
- CODE DELIVERS: NO (`_dispatcher.py:162-245`).

## H2 — dispatch Dispatcher.flex "any type signature" / fallback
- Status: DONE | Kind: docstring | Confidence: [verified]
- VERIFIED: flex registers one concrete sig per Arrangements(*types)
  permutation ('_dispatcher.py:468-475'), __allow_flex__=False, wrapped
  in PermuterMethod; confirmed Arrangements(int,str) -> (int,str) and
  (str,int). RESOLVED: docstring now says it registers func under every
  ORDERING of the given types (order-insensitive calls), coercion
  disabled, not a catch-all/fallback. Import OK.
- File: `src/worktoy/dispatch/_dispatcher.py:456`
- CLAIM: "register a function that can handle any type signature. This
  function will be called if no other signature matches."
- WHY: registers only permutations of the given types
  (`Arrangements(*types)`, `:462-468`); not a catch-all, not the fallback.
- REWRITE: "Register 'func' under every ordering of the given types so
  callers may pass them in any order; coercion is disabled per ordering.
  This is not a catch-all and not the fallback (see 'fallback')."
- CODE DELIVERS: NO.

## H3 — dispatch overload.flex attributes permutation to the dispatcher
- Status: DONE | Kind: docstring | Confidence: [verified]
- VERIFIED: restoreFrom is called in 'PermuterMethod.invoke'
  ('_permuter_method.py:30'), not in the dispatcher's dispatch fn.
  RESOLVED: 'overload.flex' docstring now attributes the permutation to
  the 'PermuterMethod' ("not the dispatcher"). Import OK.
- File: `src/worktoy/dispatch/_overload.py:210`
- CLAIM: "the dispatcher uses 'arrangement.restoreFrom(*args)' to permute
  the user's args back into canonical order before forwarding to 'func'."
- WHY: the dispatcher calls the registered `PermuterMethod`;
  `PermuterMethod.invoke` (`_permuter_method.py:30`) calls `restoreFrom`.
- REWRITE: attribute the permutation to the selected `PermuterMethod`, not
  "the dispatcher."
- CODE DELIVERS: NO.

## H4 — dispatch flexCall ignores keyword-only requirements
- Status: DONE | Kind: docstring | Confidence: [verified]
- VERIFIED by running: 'def f(a, *, b)' wrapped -> w(1) raises
  'f() missing 1 required keyword-only argument: b' (from func, not the
  wrapper's check); w(1, b=2) passes kwargs through. RESOLVED: bullet
  now scopes the check to positional-or-keyword args and notes a missing
  required keyword-only arg surfaces as the wrapped function's own
  TypeError. Import OK.
- File: `src/worktoy/dispatch/_flex_call.py:42`
- CLAIM: "raises TypeError when fewer than the required number of
  positional args is supplied (defaults are honoured)".
- WHY: `minPos = co_argcount - len(__defaults__)` (`:90-96`) counts only
  positional-or-keyword params; required keyword-only args aren't checked
  and surface as the wrapped function's own TypeError.
- REWRITE: scope the claim to positional-or-keyword args; note a missing
  required keyword-only arg surfaces as the wrapped function's TypeError.
- CODE DELIVERS: NO.

## H5 — desc AttriBox class docstring omits cast-vs-raise contract
- Status: DONE | Kind: docstring | Confidence: [verified]
- RESOLVED: added a "Get and set contract" section to the AttriBox
  class docstring. Verified by running each path: int->complex lossless
  cast; (3,4)->complex(3,4) tuple-splat construct; int('zero') build
  failure -> TypeException; delete then read -> raises MissingVariable
  (raises, not returns). Contract: already-typed stored as-is; else
  lossless typeCast (no construction); else T(value)/T(*value); else
  TypeException chained from the cast failure.
- File: `src/worktoy/desc/_attri_box.py:25-28`
- CLAIM: "AttriBox implements a lazily instantiated and strongly typed
  descriptor class." (only restates the name)
- WHY: the set/get/cast/raise contract is documented nowhere on the public
  class: a value already of type T is stored as-is; else lossless
  `typeCast` with allowInstantiation=False; else construct `T(value)`
  (tuple splatted); else `TypeException` chained from the cast failure;
  deleted field reads back as `MissingVariable`.
- REWRITE: state the lazy-default + set contract on the class docstring
  (model on `_attri_box.py:189-216`).
- CODE DELIVERS: behavior yes (`_attri_box.py:189-216`); doc gap.

## H6 — desc FixBox "only change" hides that delete is disabled
- Status: DONE | Kind: docstring | Confidence: [verified]
- RESOLVED: module + class docstrings now state two methods change
  (write-once -> WriteOnceError; delete disabled -> ProtectedError).
  Verified by running: 2nd write raises WriteOnceError, del raises
  ProtectedError.
- File: `src/worktoy/desc/_fix_box.py:1-5, 21-25`
- CLAIM: "The only change reimplemented is that setting is only allowed
  when no value has been set before."
- WHY: `__instance_delete__` is also overridden so deletion raises
  `ProtectedError` (`_fix_box.py:45-48`).
- REWRITE: "Two methods change: a second write raises 'WriteOnceError';
  deletion is disabled and raises 'ProtectedError'."
- CODE DELIVERS: NO.

## H7 — desc Field @SET/@DELETE copied getter wording (wrong)
- Status: DONE | Kind: docstring | Confidence: [verified]
- VERIFIED: setter invoked 'setterFunc(instance, value)' (_field.py:134),
  deleter 'deleterFunc(instance)' (:150); multiple may register (fire in
  order); no setter -> ReadOnlyError, no deleter -> ProtectedError.
  RESOLVED: SET/DELETE docstrings rewritten accordingly (SET takes value;
  both note registration order + the no-handler raise). GET left as-is
  (its "no other arguments" wording is correct; second @GET / AccessError
  is tracked under M5).
- File: `src/worktoy/desc/_field.py:89-105`
- CLAIM: "Decorator for the setter method. The method should be a normal
  instance method that can be run without any other arguments."
- WHY: a setter is called `method(self, value)` (`_field.py:132-134`), so
  "without any other arguments" is wrong.
- REWRITE: SET -> "called as 'method(self, value)' on every assignment";
  DELETE -> "called as 'method(self)' on 'del'."
- CODE DELIVERS: NO (docstring contradicts code).

## H8 — core ExceptionInfo "each outcome" misses two outcomes
- Status: DONE | Kind: docstring | Confidence: [verified]
- VERIFIED by running: no-expected-type + exception -> propagates,
  report stays ''; wrong-type -> suppressed (no escape), report set.
  RESOLVED: class docstring (_exception_info.py, in utilities) now
  enumerates all outcomes, marks which suppress the exception, and notes
  the empty-report propagation case.
- File: `src/worktoy/utilities/_exception_info.py:27-51`
- CLAIM: "a human-readable 'report' string is produced for each possible
  outcome: clean exit, missing exception, exact match, subclass match, or
  wrong type."
- WHY: when no expected type is set and an exception is raised, it
  propagates and `report` stays `''`; a wrong-type exception is
  SUPPRESSED (returns True) without that being stated.
- REWRITE: enumerate all branches, including "no expected type + exception
  raised -> propagates, report empty" and "wrong type -> suppressed."
- CODE DELIVERS: NO.

## H9 — work_io PathSyntaxException missing from Raises; strict= undoc
- Status: DONE | Kind: docstring | Confidence: [verified]
- RESOLVED: validateExistingFile / validateExistingDirectory /
  scrapDirectory docstrings rewritten (Google->NumPy style) to document
  PathSyntaxException (non-absolute, always), the 'strict=False' kwarg
  (returns '' / silent), and for scrapDirectory the NotADirectoryError
  (always) and OSError (non-empty, from os.rmdir). Verified by reading
  each function body; work_io import OK.
- Files: `src/worktoy/work_io/_validate_existing_file.py:26-28`,
  `_validate_existing_directory.py:27-29`, `_scrap_directory.py:17-19`
- CLAIM: Raises sections list only `FileNotFoundError` / `IsADirectoryError`
  etc.
- WHY: each unconditionally raises `PathSyntaxException` for a non-absolute
  path; the `strict=False` kwarg (silences failures, returns '') is
  undocumented; `scrapDirectory` doesn't mention the non-empty-directory
  `OSError`.
- REWRITE: add `PathSyntaxException` (non-absolute) and the `strict`
  kwarg to each; for scrapDirectory add `OSError` (not empty) and
  `NotADirectoryError`.
- CODE DELIVERS: NO.

## H10 — work_io FidGen.__get__ docstring copied from Dispatcher
- Status: DONE | Kind: docstring | Confidence: [verified]
- RESOLVED: '__get__' docstring (which talked about type signatures and
  the THIS token, and class-creation) replaced with the actual behavior:
  records 'instance' as the context caller and delegates to
  '__instance_get__'. (The RecursionError-on-slot-exhaustion in next()
  remains a separate CODE smell, not addressed here.)
- File: `src/worktoy/work_io/_fid_gen.py:196-201`
- CLAIM: "Python calls this method to allow the type signatures to be
  updated with the owner class ... using the 'THIS' token ..."
- WHY: FidGen has no type signatures, overloads, or THIS. `__get__`
  records `instance` and delegates to `__instance_get__` (`:203-204`).
- REWRITE: describe the actual behavior (bind to instance, set
  `__context_caller__`, return self / class).
- CODE DELIVERS: NO.
- NOTE: related code smell — when all 101 candidate names are taken,
  `_fid_gen.py:124` raises `RecursionError` (odd choice). REPORT ONLY;
  do not change code. The docstring fix should at least state the failure
  mode (see M-side note).

## H11 — lorem_ipsum scaleSum direction inverted + maxIndex off-by-one
- Status: DONE | Kind: docstring | Confidence: [verified]
- VERIFIED in code: miss = sum-targetSum, loop converges sum TO
  targetSum (may rise or fall); randint(minIndex, maxIndex) is
  inclusive. RESOLVED: description now says "until their sum equals
  targetSum"; maxIndex doc says "up to and including this value"
  (default last index). minIndex doc ("greater than or equal") was
  already correct.
- File: `src/worktoy/lorem_ipsum/_base_generator.py:54-56` (direction),
  `:70-72` (off-by-one)
- CLAIM: "incrementing or decrementing the integers until the sum ... is
  reduced by the given amount"; "maxIndex ... only entries less than this
  index will be adjusted."
- WHY: it adjusts the sum TOWARD `targetSum` (may increase it), and
  `randint(minIndex, maxIndex)` is inclusive of `maxIndex`.
- REWRITE: "adjusts entries up or down until the sum equals 'targetSum'";
  "maxIndex ... entries up to and including this index."
- CODE DELIVERS: NO.

## H12 — work_test samplers: stale gen, wrong cardinality, wrong attrs
- Status: DONE | Kind: docstring | Confidence: [verified]
- VERIFIED in code (_base_sampler.py): _getRow uses self.colCount
  (:193) not self.count; __call__ calls _getItem (:228); __iter__ is
  finite (yields rowCount rows via _getRow). RESOLVED: docstrings fixed
  (colCount; '_getItem'; "yields exactly rowCount rows", each a row
  tuple). work_test import OK.
- File: `src/worktoy/work_test/samplers/_base_sampler.py:226, 232-233, 182`
- CLAIM: "calling the 'gen' method"; "infinite stream of sample values";
  "n specified by 'self.count'".
- WHY: no `gen` method (calls `_getItem`/`_getRow`); the iterator is
  FINITE (yields `rowCount` rows); the count attribute is `colCount`.
- REWRITE: name `_getItem`/`_getRow`; "yields exactly 'rowCount' rows"; "n
  given by 'self.colCount'."
- CODE DELIVERS: NO.

## H13 — tests: docstrings name nonexistent modules / invert assertions
- Status: DONE | Kind: docstring | Confidence: [verified]
- RESOLVED (test docstrings only; all 7 files byte-compile):
  - test_type_cast.py: worktoy.static -> worktoy.utilities (module +
    class); EVERY "raises TypeError" -> "raises 'TypeCastException'"
    (the whole file asserts TypeCastException); the "only when <type>"
    claims replaced with the real accepted/rejected inputs. Fixed all
    such methods, not just the agent-listed lines.
  - test_maybe.py: worktoy.parse -> worktoy.utilities (module + class).
  - test_string_list.py: "StringList class" -> "'stringList' function".
  - test_text_fmt.py: inverted "raises TypeError" -> "converts
    non-string args and joins with spaces (does not raise)".
  - test_kee_meta_sub_class.py: dropped nonexistent 'FontMeta' (fixture
    is 'KeeMetaSub') in all 3 docstrings; fixed "Becaues" typo.
  - test_kee_meta.py: removed the truncated "These tes" fragment
    (module + class).
  - test_class_resolve.py: hook "raises KeeResolveError" -> returns
    'NotImplemented'; KeeMeta falls through and raises KeeResolveError
    only when no resolver succeeds.
- Items (each MATCHES TEST: NO):
  - `tests/test_utilities/test_type_cast.py:1, 23` — "worktoy.static"
    module (it's `worktoy.utilities`).
  - `tests/test_utilities/test_maybe.py:1, 22` — "worktoy.parse" module
    (it's `worktoy.utilities`).
  - `tests/test_utilities/test_string_list.py:12` — "the StringList class"
    (`stringList` is a function; no such class).
  - `tests/test_utilities/test_text_fmt.py:52` — "raises a TypeError when
    given a non-string input," but the test asserts it CONVERTS
    (`'69 420 1337'`). Inverted contract.
  - `tests/test_utilities/test_type_cast.py:86,96,130,142,163,176` — say
    "TypeError" / "only when ... float"; tests assert `TypeCastException`
    and include str/complex/bool cases.
  - `tests/test_keenum/test_class_resolve.py:26` — says
    `__class_resolve__` "raises 'KeeResolveError'"; fixture returns
    `NotImplemented`.
  - `tests/test_keenum/test_kee_meta_sub_class.py:1,22,44` — repeatedly
    names `FontMeta`; the fixture is `KeeMetaSub`.
  - `tests/test_keenum/test_kee_meta.py:1,21` — truncated mid-word
    ("These tes").
- REWRITE: point each at the real module/exception/fixture; for the
  inverted ones describe what is actually asserted (see review for exact
  rewrites).

---

# MEDIUM

## M1 — KeeFlag "is itself an enumeration" vs "instances are not members"
- Status: DONE (resolved alongside C2) | Kind: docstring
  | Confidence: [verified]
- File: `src/worktoy/keenum/_kee_flag.py` module + class openings
  rewritten ("declares one single-bit flag ... not itself an
  enumeration"); `'kw'` bullet renamed to `'kwargs'`.
- CODE DELIVERS: docs now match.

## M20 — KeeFlag "Attributes" section frames flag attrs as member attrs
- Status: TODO  | Kind: docstring | Confidence: [verified]
- File: `src/worktoy/keenum/_kee_flag.py` class docstring "Attributes
  (becomes attributes of the instances of the owning 'KeeFlags'
  class)" list.
- WHY: the bullets describe a KeeFlag's own attributes (the single
  flag's name, the bit index) but call them "the member"'s. It also
  lists a 'value' attribute; KeeFlag has no 'value' Field ('value',
  'lows', 'highs', 'names' at `_kee_flag.py:78-81` are linter-only
  annotations, not implemented), so 'keeFlag.value' raises
  AttributeError.
- NEEDS: decide what KeeFlag actually exposes vs what KeeFlags members
  expose, then rewrite the section. Deferred from C2 to avoid guessing.
- CODE DELIVERS: NO (lists attributes KeeFlag does not implement).

## M21 — mcls __init__ docstring claims a 'dict' validation step
- Status: TODO  | Kind: docstring | Confidence: [verified] (found during C8)
- File: `src/worktoy/mcls/__init__.py` module docstring (~line 12).
- CLAIM: "Next the metaclass validates the 'dict' object and finally
  passes it to the '__new__' method on type."
- WHY: 'AbstractMetaclass.__new__' does no validation between
  'compile()' and 'MetaType.__new__'. Name validation (reserved names,
  near-miss dunders, '__del__') happens earlier, during class-body
  execution, via the namespace hooks.
- REWRITE: "The namespace 'compile()' returns the final 'dict', which is
  passed to 'type.__new__'. Per-name validation happens earlier, during
  class-body execution, through the hooks on the namespace class."
- CODE DELIVERS: NO (no validation step in '__new__').

## M2 — dispatch addVariadicSigFunc silent on duplicates / ARGS
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/dispatch/_dispatcher.py:293`
- WHY: unlike `addSigFunc` (raises `DuplicateSignature`), it appends and
  does not validate the `ARGS` terminator.
- REWRITE: state first-registered-wins and that the `ARGS` terminator is
  not validated here.
- CODE DELIVERS: NO.

## M3 — dispatch fallback/finalize edge cases
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/dispatch/_dispatcher.py:447, 439`
- WHY: fallback also fires on length mismatch / coercion-disabled sigs /
  kwargs-only; a throwing finalizer replaces the return and chains the
  in-flight exception (`:250-258`).
- REWRITE: state both.
- CODE DELIVERS: yes, underspecified.

## M4 — desc BaseDescriptor callback order/duplicates
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/desc/_base_descriptor.py:26-30`
- WHY: "as many methods as desired" omits that callbacks fire in
  registration order and a re-registered name fires twice.
- CODE DELIVERS: yes, underspecified.

## M5 — desc Field @GET "decorate one method"
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/desc/_field.py:41-42, 81-87`
- WHY: a second `@GET` silently replaces the first; a Field with no getter
  raises `AccessError` on read.
- CODE DELIVERS: yes, underspecified.

## M6 — core parseKwargs omits wrong-type raise
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/core/_object.py:466-503`
- WHY: "If no value is found" covers only key-absent; a present key with a
  wrong-typed value raises `TypeException` (`:501`).
- CODE DELIVERS: yes, underspecified.

## M7 — core hookPreSet/hookOnSet identical "just set" wording
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/core/_object.py:399-426`
- WHY: `hookPreSet` fires BEFORE the write; both say "the value just set,"
  making them indistinguishable.
- CODE DELIVERS: hookPreSet NO (fires before); hookOnSet yes.

## M8 — mcls pre/postCompilePhase lifecycle reversed in time
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/mcls/space_hooks/_abstract_space_hook.py:140-150`
- WHY: described as "before/after the '__init__' of the namespace," but
  they run during `compile()`, long after `__init__`.
- REWRITE: restate relative to `compile()` (after the class body executes).
- CODE DELIVERS: NO.

## M9 — mcls __init__ claims type.__init__ triggers __set_name__ etc.
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/mcls/_abstract_metaclass.py:169-173`
- WHY: `__set_name__`/`__init_subclass__` run inside `type.__new__`,
  already complete before `__init__`.
- CODE DELIVERS: NO (ordering claim).

## M10 — mcls AbstractSpaceHook.__get__ sets spaceClass (it doesn't)
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/mcls/space_hooks/_abstract_space_hook.py:172-179`
- WHY: only `__space_object__` is set; `spaceClass` is never assigned.
  (Also uses double-backtick markup — drop it.)
- CODE DELIVERS: NO.

## M11 — mcls getItemPhase -> bool / "returns False"
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/mcls/space_hooks/_abstract_space_hook.py:130-133`
- WHY: base returns `None`, the caller ignores the return
  (`_abstract_namespace.py:223`); no blocking semantics (unlike
  setItemPhase).
- REWRITE: "return value ignored."
- CODE DELIVERS: NO.

## M12 — mcls setItemHook named method does not exist
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/mcls/space_hooks/_reserved_namespace_hook.py:68-75`
- WHY: the method is `setItemPhase`; the docstring says `setItemHook`.
- CODE DELIVERS: NO (name).

## M13 — mcls BaseMeta says hooks "defined in BaseSpace"
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/mcls/_base_meta.py:20-22`
- WHY: NamespaceHook/ReservedNamespaceHook/FlexCallHook are on
  `AbstractNamespace`; only `LoadSpaceHook` is added by `BaseSpace`.
- CODE DELIVERS: NO.

## M14 — mcls __getitem__ fallback doesn't exist
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/mcls/_abstract_metaclass.py:113-116`
- WHY: "falls through to the metaclass '__getitem__'" — `__getitem__` is
  commented out (`:274-283`); subscripting a class with no
  `__class_getitem__` raises `TypeError`.
- CODE DELIVERS: NO.

## M15 — ezdata mutable defaults "fresh copy" is shallow
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/ezdata/_ez_field.py:240-243`
- WHY: `fieldType(*posArgs, **keyArgs)` is shallow; nested mutables are
  shared.
- CODE DELIVERS: NO (overpromises isolation). (Same file `:237-240` has
  the "idempotent / without any cost" overclaim — fold in.)

## M16 — ezdata MRO "later-MRO wins" inverted
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/ezdata/_ez_space.py:168-169, 197-199`
- WHY: behavior is correct (higher-priority/earlier-MRO base wins) but both
  docstrings label it "later-MRO wins" and call `reversed(bases)` "reverse
  MRO order."
- CODE DELIVERS: behavior yes, terminology NO.

## M17 — keenum exceptions: vague trigger + missing attribute docs
- Status: TODO  | Kind: docstring | Confidence: [agent]
- Files: `src/worktoy/waitaminute/keenum/_kee_type_exception.py:15-19`,
  `_kee_case_exception.py:15-19`, `_kee_duplicate.py:17-21`
- WHY: one-line restatements; none documents the precise condition or the
  stored attributes (`name`/`value`/`expectedTypes`; "duplicate" = name vs
  value; "not with upper case" grammar).
- REWRITE: add `Attributes` and a precise trigger to each.
- CODE DELIVERS: yes (attributes set), docs vague.

## M18 — work_io newDirectory NotADirectoryError trigger wrong
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/work_io/_new_directory.py:29-30`
- WHY: the trigger is "an intermediate path component is a file," not "the
  path is not a directory."
- CODE DELIVERS: unsure (raised under a different condition than stated).

## M19 — tests: docstrings undersell/mislabel what is asserted
- Status: TODO  | Kind: docstring | Confidence: [agent]
- Items:
  - `tests/test_dispatcher.py:1,115` — "tests TypeSig" but also tests
    Dispatcher/overload.
  - `tests/test_keenum/test_kee_flags.py:37` — "availability" but actually
    asserts memberList vs iteration-order identity.
  - `tests/test_keenum/test_kee_meta_resolve.py:42` — loops over case
    variants but the body ignores `case`, so case-insensitivity is never
    exercised.
  - `tests/test_keenum/test_num.py:306` — "every KeeNum member" but only
    `Compass` is tested.

---

# LOW / COSMETIC

## L1 — README grammar + inline triple-backticks
- Status: PARTIAL (version header DONE; grammar/backticks TODO)
  | Kind: readme | Confidence: [verified]
- README.md:8 "The **worktoy** provides utilities"; README.md:71 inline
  triple-backticks around AttriBox.  <-- still TODO
- DONE: README.md:6 version header "worktoy v0.99.xx" replaced with
  "worktoy v1.0.0 (release candidate)" plus a one-line RC-window status
  note. Header intentionally carries no rcN so it will not drift; the
  live PyPI badge shows the exact published version.

## L2 — desc __init__ "descriptor-context" announced, never defined
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/desc/__init__.py:1-10` (definition lives in
  core/_object.py; also hedges with "usually").

## L3 — core DELETED "should raise" imperative phrasing
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/core/sentinels/_deleted.py:35`

## L4 — core Object self-referential "See 'Object'"
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/core/_object.py:295-305, 265-269`

## L5 — core MetaType "base on this class" non-standard
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/core/_meta_type.py:22`

## L6 — waitaminute MissingVariable expectedTypes documented singular
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/waitaminute/_missing_variable.py:32` (variadic,
  plural slot).

## L7 — waitaminute ControlClassError "only __str__/__repr__"
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/waitaminute/control_flow/_control_class_error.py:19`
  (omits whitelisted interpreter dunders).

## L8 — utilities ValidSlice "defines __index__" (not invoked)
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/utilities/_valid_slice.py:67-70` (checks for a
  callable attribute without invoking it).

## L9 — utilities Directory "owner class" vs concrete class module
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/utilities/_directory.py:22` (resolves
  `instance.__class__.__module__`).

## L10 — waitaminute DuplicateSignature NumPy heading "Arguments"
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/waitaminute/dispatch/_duplicate_signature.py:29`
  (should be "Attributes").

## L11 — mcls __bool__ docstring is a Dante excerpt, no behavior
- Status: TODO  | Kind: docstring | Confidence: [agent]
- File: `src/worktoy/mcls/_abstract_metaclass.py:218-226` (actual fallback
  chain `__class_bool__` -> `__class_len__` -> `__class_iter__` -> True is
  documented only in the class table).

---

# DECISIONS / PIPELINE (need Asger)

## D1 — setAnnotationPhase documented but never dispatched
- Status: DONE (removed, per Asger) | Kind: code (authorized)
  | Confidence: [verified]
- RESOLVED: Asger said get rid of it. Removed the dead
  'setAnnotationPhase' lifecycle-table entry AND the no-op method from
  '_abstract_space_hook.py' (no callers, no overrides anywhere; entirely
  dead pending the annotation PEP). Verified: grep finds none, mcls
  imports, hasattr(AbstractSpaceHook,'setAnnotationPhase') is False. The
  real '__annotations__' storage / reserved name were left untouched.
  If the PEP lands, the hook gets re-added and actually wired up.
- File: `src/worktoy/mcls/space_hooks/_abstract_space_hook.py:62, 124`
- WHY: documented as a lifecycle phase; grep finds NO caller. Looks tied to
  the in-progress namespace-annotation / PEP work (pep_annotations.txt).
- OPTIONS: (a) add one line noting it is a reserved phase not currently
  dispatched, or (b) leave as-is. Do NOT re-engineer annotation handling
  without Asger's say-so.

## D2 — index.rst "Every source file" false; _kee_num.py omitted from site
- Status: DONE (option a) | Kind: docs prose | Confidence: [verified]
- RESOLVED (option a, per Asger): index.rst no longer claims "Every
  source file"; now "Every source file reachable from a package's
  public API ... private helper modules that are not re-exported do not
  appear." Avoided the literal '__all__' token in rST prose.
- STILL OPEN (option b, NOT done): the canonical KeeNum contract in
  '_kee_num.py' (_KeeBase docstring) is still not rendered on the site;
  the KeeNum page shows '_kee_meta.py' (the TYPE_CHECKING joke). Making
  it visible needs either a '_gen.py' change (release-critical pipeline)
  or moving the contract docstring into '_kee_meta.py'. Left for a
  deliberate decision.
- Files: `docs/index.rst:19`; generator `docs/_gen.py` (driven by __all__)
- WHY: index.rst claims "Every source file in the package, shown verbatim,"
  but `_gen.py` only emits files reachable through `__all__`. The clearest
  casualty is `src/worktoy/keenum/_kee_num.py`: the `_KeeBase` docstring
  there is the CANONICAL KeeNum equality/identity + hashability contract,
  and it appears on NO site page (the `KeeNum` page renders `_kee_meta.py`,
  whose only KeeNum docstring is the `if TYPE_CHECKING` "samizdat" joke).
- OPTIONS: (a) one-word honesty fix to index.rst ("Every public source
  file ..."), or (b) generator change to also emit private modules
  (touches release-critical pipeline — approval required).
