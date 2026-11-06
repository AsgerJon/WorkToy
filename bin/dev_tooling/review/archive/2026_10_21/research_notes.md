# worktoy research notes: central non-leaf packages

Started 2026-10-20. Read order follows research_prompt.txt: core,
dispatch, desc, mcls, each in the import order of its own __init__.py.
utilities and waitaminute are inspected ad hoc as they are referenced.
Every entry below was written immediately after reading every line of
the item it describes. Line references are to the file as it stood on
2026-10-20. To resume: continue with the first item in the package
order that has no entry here.

Legend for each entry:
- Item: path and symbol(s) it defines, with line count.
- What it is: the job of the item in its own words.
- Symbols: every public and private name defined, with path:line.
- Interactions: how the item touches core, dispatch, desc, mcls.
- Support: which utilities / waitaminute names it uses, and what they do.
- Notes: anything observed that a later reader should know.

# Package: core

Import order from core/__init__.py:15-19: MetaType, sentinels,
control_flow, ContextInstance and ContextOwner, Object. The sibling
_annotations_descriptor.py is not exported and is pulled in by
_meta_type.py, so it is covered first.

## utilities/_maybe.py : maybe (support, read ad hoc from core/_annotations_descriptor.py)

- Item: src/worktoy/utilities/_maybe.py, 39 lines, defines the function
  maybe at utilities/_maybe.py:14.
- What it is: returns the first positional argument that is not None, or
  None when every argument is None or no argument was given
  (utilities/_maybe.py:36-39). Falsy values such as 0 or '' are returned;
  only None is skipped (docstring example at :31-32).
- Symbols: maybe(*args) -> Any, utilities/_maybe.py:14.
- Interactions: a pure leaf. First reference found at
  core/_annotations_descriptor.py:53, where it prefers the owner passed to
  __get__ over type(cls). Expect it throughout core, dispatch, desc and
  mcls wherever an optional argument gets a fallback.
- Support: none beyond typing.
- Notes: because only None is skipped, maybe cannot supply a default for
  a falsy value; that is the documented contract.

## core/_annotations_descriptor.py : _AnnotationsDescriptor, HAS_TYPE_ANNOTATIONS

- Item: src/worktoy/core/_annotations_descriptor.py, 70 lines. Not
  exported by core/__init__.py; imported directly as a sibling by
  core/_meta_type.py:10-11.
- What it is: a private data descriptor that MetaType.__new__ installs in a
  metaclass body under '__annotations__' whenever that body carries
  annotations, on Python 3.10 and later. It restores for the classes of
  that metaclass the behaviour of the getset descriptor
  type.__dict__['__annotations__'], which the metaclass's own eager
  annotations dict would otherwise shadow.
- Symbols:
  - typeAnnDesc, core/_annotations_descriptor.py:25: the getset descriptor
    'type' carries for '__annotations__' from 3.10 on, None before that.
  - HAS_TYPE_ANNOTATIONS, :26: True when typeAnnDesc exists. MetaType
    installs the descriptor only when this is True.
  - _AnnotationsDescriptor, :29. Stores the metaclass's own annotations in
    __meta_annotations__ (:41, set at :43-44).
    - __get__(cls, owner), :46-54. cls is None means 'type' itself is
      reading the attribute off the metaclass (type's getset calls the
      stored value's __get__ with no instance), so the metaclass's own
      dict is returned. Otherwise cls is a class of the metaclass and the
      call is forwarded to the getset with mcls = maybe(owner, type(cls)),
      so the class answers with its own annotations, and on 3.10+ 'type'
      creates an empty dict on a class that has none.
    - __set__, :56-61, and __delete__, :63-68: forwarded to the getset so
      assignment and deletion on a class behave as stock.
    - __objclass__ = type, :70: presents the descriptor as belonging to
      'type' for introspection tools.
- Interactions: explains why cls.__annotations__ on a class built by any
  worktoy metaclass (mcls.AbstractMetaclass and BaseMeta, SentinelMeta,
  MetaFlow, the keenum and ezdata metaclasses) answers for the class
  alone. Anything in desc or mcls that reads '__annotations__' off a
  class relies on this. The only construction site is
  core/_meta_type.py:80-82.
- Support: utilities.maybe (imported :14, used :53).
- Notes:
  - The problem it solves is created by 'from __future__ import
    annotations' making every annotated class body produce an eager
    '__annotations__' dict (comment at core/_meta_type.py:71-77). Only a
    metaclass (a base that subclasses type) receives the descriptor;
    ordinary classes keep their plain dict. Before 3.10 nothing is
    installed and the fall-through to a base is accepted.
  - Derived from CPython's type_getattro, not executed: a metaclass
    whose body has no annotations gets no descriptor, and the first read
    of __annotations__ on that metaclass makes 'type' store an empty
    plain dict in the metaclass's own __dict__. That plain dict then
    sits ahead of both a parent metaclass's _AnnotationsDescriptor and
    type's getset in the lookup for its classes, reviving the
    fall-through. Worth checking which worktoy metaclass bodies carry
    annotations when mcls is read.

## core/_meta_type.py : MetaType, _Chill

- Item: src/worktoy/core/_meta_type.py, 92 lines. First import of
  core/__init__.py:15. Exports MetaType; _Chill stays private.
- What it is: the meta-metaclass of the library. Every worktoy metaclass
  (mcls.AbstractMetaclass and everything based on it, SentinelMeta,
  MetaFlow, KeeMetaMeta, the ezdata metaclass) derives from MetaType, so
  combining them never raises a metaclass conflict (docstring :37-45).
  Its __new__ does two jobs: it ends every class's __init_subclass__
  chain at _Chill, and it installs _AnnotationsDescriptor on annotated
  metaclass bodies.
- Symbols:
  - _Chill, core/_meta_type.py:21-32. Carries __skip_hash__ = True (:22)
    and a classmethod __init_subclass__(cls, **kwargs) (:24-32) that
    accepts and drops any keyword, sets __skip_hash__ False on the new
    subclass through type.__setattr__, and deliberately does not call
    super().__init_subclass__. The comment at :30-32 gives the contract:
    _Chill is last in the resolution order of every class it is a base
    of, only object follows it, so the chain ends here. This is the
    author's suppression of object.__init_subclass__ refusing keywords.
  - MetaType(type), :35.
    - __str__ and __repr__, :59-62: 'Name[metaclass=MetaName]'.
    - __new__(mmcls, name, bases, space, **kw), :66-89:
      - :67-69 if the last base is not an instance of MetaType (so does
        not already end in _Chill), append _Chill to bases.
      - :70 drop an explicit 'object' from bases, which would otherwise
        sit before _Chill and break the linearisation.
      - :78-82 when HAS_TYPE_ANNOTATIONS, the body has '__annotations__'
        and any base subclasses type (a metaclass is being made), wrap
        the dict in _AnnotationsDescriptor.
      - :83-88 if the namespace has no '__namespace__' key, put the
        namespace itself under that key for the duration of
        type.__new__, then remove the key from the caller's dict.
      - :86 creation itself goes through super().__new__ with **kw.
    - __init__(cls, name, bases, space, **kw), :91-92: sets __skip_hash__
      False on the created class via type.__setattr__ and does not
      forward to type.__init__, so the keywords never reach
      type.__init__ (which would refuse them).
- Interactions:
  - mcls: AbstractMetaclass both subclasses and derives from MetaType
    (docstring :38-40), so every class statement under a worktoy
    metaclass passes through this __new__. Class keywords travel in
    **kw to type.__new__ (:86), which hands them to the new class's
    __init_subclass__, and that chain ends at _Chill. That is the only
    route a class keyword takes and the only place it stops.
  - core.sentinels and core.control_flow: SentinelMeta and MetaFlow are
    built the same way (:41-44), so a sentinel or signal declared with a
    class keyword behaves like any other worktoy class.
  - utilities: _MetaSlice subclasses type directly and is the stated
    exception (:44-45), because utilities loads before core.
  - desc: no direct contact; desc classes become MetaType-made only by
    being based on mcls.BaseObject.
  - The '__namespace__' key (:83-88) is a bridge to mcls: a namespace
    compiled by AbstractNamespace is expected to carry '__namespace__'
    already (spaceState True, nothing inserted), while a plain dict
    namespace gets a temporary self reference.
- Support: core/_annotations_descriptor.py (sibling import :10-11, not
  through the package since it is unexported). Nothing from utilities
  or waitaminute directly.
- Notes:
  - __skip_hash__ is True only on _Chill itself; _Chill.__init_subclass__
    (:29) and MetaType.__init__ (:92) both set it False. No consumer seen
    yet; expect a __hash__ somewhere that honours it. Track.
  - The temporary '__namespace__' key is removed from the caller's dict
    only. type.__new__ copies the namespace into the class __dict__, so
    the created class keeps '__namespace__' pointing at the original
    namespace dict (derived from CPython behaviour, not executed). If
    relied on, cls.__namespace__ is a stable feature of every
    MetaType-made class; if not, it is a reference that keeps the whole
    namespace alive.
  - The test at :67-68 looks at the last base only. For bases
    (WorktoyClass, PlainClass) _Chill is appended again, harmless since
    _Chill is already last in WorktoyClass's MRO and C3 keeps it last.
    For bases (PlainClass, WorktoyClass) nothing is appended and _Chill
    still precedes object in the C3 result.
  - A class with no bases gets bases (_Chill,) (:67 falls back to object,
    :69 appends, :70 would strip object anyway).
  - MetaType's own body has no annotations, so MetaType.__dict__ has no
    '__annotations__' and the descriptor machinery starts one level
    down, at the first annotated metaclass body.

## waitaminute/_work_toy_exception.py : WorkToyException, _rebuild, _travels (support, read ad hoc from core/sentinels/_sentinel.py)

- Item: src/worktoy/waitaminute/_work_toy_exception.py, 105 lines. Second
  import of waitaminute/__init__.py:25, after Detached.
- What it is: the common base of every library exception apart from the
  control-flow signals. It adds pickle and copy support in one place by
  recording the constructor call as made and replaying it.
- Symbols:
  - _rebuild(cls, args, kwargs), :19-25: module-level callable that
    pickle stores by reference; calls cls(*args, **kwargs).
  - _travels(arg), :28-37: True when pickle.dumps(arg) succeeds; the only
    test is to try.
  - WorkToyException(Exception), :40. __slots__ = () (:75) so it adds no
    layout and can sit beside SyntaxError.
    - __new__(cls, *args, **kwargs), :77-81: BaseException.__new__ with
      the positional args only, then stores __init_args__ and
      __init_kwargs__ in the instance dict (every exception has one).
    - __reduce__, :83-95: returns _rebuild with the class and the
      captured call, each argument that does not travel replaced by a
      Detached stand-in.
    - __copy__, :97-98 and __deepcopy__, :100-105: rebuild from the
      captured call, the deep variant deep-copying the captured args
      first (the copy import is local to that method).
- Interactions: every exception raised by core, dispatch, desc and mcls
  is a WorkToyException, listed first and then the builtin. Exceptions
  call the builtin's __init__ with no arguments (see
  IllegalInstantiation below), so self.args is empty and the stock
  BaseException.__reduce__ would rebuild them with nothing; this base
  is what makes a worktoy exception survive a process pool.
- Support: Detached (waitaminute/_detached.py) and pickle.
- Notes: the constructor replay means an exception's __init__ runs again
  on unpickle and on copy, with Detached stand-ins where real objects
  were. Any __init__ that validates argument types would then see a
  Detached; none of the two read so far does.

## waitaminute/_detached.py : Detached (support)

- Item: src/worktoy/waitaminute/_detached.py, 69 lines. First import of
  waitaminute/__init__.py:24.
- What it is: the stand-in that WorkToyException.__reduce__ substitutes
  for an argument that cannot be pickled (a lambda, a class defined in
  a function, a namespace object). It carries the type name and repr of
  the original so the rebuilt exception still renders its message.
- Symbols:
  - Detached, :15, __slots__ = ('typeName', 'text') (:35).
  - __init__(arg), :37-39: stores type(arg).__name__ and repr(arg).
  - _fromParts(typeName, text), :41-50: classmethod rebuilding a
    stand-in from its two parts; __reduce__ (:52-53) points pickle at it.
  - __getattr__(name), :55-64: any plain attribute answers with the
    stand-in itself; a dunder name raises AttributeError so pickle and
    copy do not mistake the stand-in for an object implementing their
    protocols.
  - __str__ and __repr__, :66-69: '<detached TypeName: repr>'.
- Interactions: only WorkToyException constructs it. Its attribute
  passthrough exists for exception messages in desc and mcls that read
  through an argument.
- Notes: derived, not executed: the docstring example at :24 is
  'self.desc.__field_name__', but __field_name__ is a dunder and the
  refusal at :62-63 raises AttributeError for every dunder, so a message
  that reads a dunder straight through a Detached argument would fail
  inside __str__ rather than show the stand-in. Whether any exception
  message in waitaminute.desc does that is something to check when
  those exceptions are read ad hoc.

## waitaminute/meta/__init__.py : index of the metaclass exceptions (support)

- Item: src/worktoy/waitaminute/meta/__init__.py, 40 lines.
- What it is: the exceptions raised during class creation by mcls and by
  the primitive metaclasses in core. Import order (:14-25):
  IllegalInstantiation, HookException, DuplicateHook, DelException,
  QuestionableSyntax, ReservedName, UnboundClassHook, OverloadConflict,
  ClaimedName, ShadowedClassHook, DuplicateSentinel, ControlClassError.
- Interactions: core.sentinels uses IllegalInstantiation and
  DuplicateSentinel; core.control_flow is expected to use
  ControlClassError; the hook and name exceptions belong to mcls.
  Each is read ad hoc when first referenced.

## waitaminute/meta/_illegal_instantiation.py : IllegalInstantiation (support)

- Item: src/worktoy/waitaminute/meta/_illegal_instantiation.py, 38 lines.
- What it is: raised when a class is called that must never be
  instantiated; the sentinel classes are the stated case (:15-18).
  Based on WorkToyException then TypeError (:13).
- Symbols: __slots__ = ('cls',) (:26); __init__(cls_) stores self.cls and
  calls TypeError.__init__ with nothing (:28-30); __str__ (:32-36)
  formats "Illegal instantiation of class 'Name'" through textFmt;
  __repr__ = __str__ (:38).
- Interactions: raised by SentinelMeta.__call__
  (core/sentinels/_sentinel.py:96-100). Expect it again wherever mcls
  or desc forbids instantiation.
- Support: utilities.textFmt (:9, used :36).

## waitaminute/meta/_duplicate_sentinel.py : DuplicateSentinel (support)

- Item: src/worktoy/waitaminute/meta/_duplicate_sentinel.py, 71 lines.
- What it is: raised when a class statement declares a sentinel at a
  name the process-wide registry already holds. The docstring (:20-30)
  records the history: the second statement used to silently receive
  the existing sentinel, so two unrelated modules declaring PENDING
  shared one object. Based on WorkToyException then TypeError (:18).
- Symbols: __slots__ = ('sentinelName', 'existing', 'module') (:45);
  __init__(sentinelName, existing, module=None) (:47-56) stores the
  three and calls TypeError.__init__ with nothing; __str__ (:58-69)
  names the existing sentinel's __module__ and the refusing module, or
  'a class statement' when the namespace carried no __module__ (a plain
  dict handed to SentinelMeta by hand); __repr__ = __str__ (:71).
- Interactions: raised by SentinelMeta.__new__
  (core/sentinels/_sentinel.py:86-91) with space.get('__module__').
- Support: utilities.textFmt (:11, used :69).

## core/sentinels/_sentinel.py : SentinelMeta, Sentinel

- Item: src/worktoy/core/sentinels/_sentinel.py, 123 lines. First import
  of core/sentinels/__init__.py:38.
- What it is: the metaclass and base class of every sentinel. A
  sentinel is a class, never an instance: the class object itself is
  the unique stateless marker, equal only to itself. SentinelMeta
  registers each sentinel by name for the whole process, refuses a
  second class statement at a registered name, and forbids calling a
  sentinel class.
- Symbols:
  - SentinelMeta(MetaType, metaclass=MetaType), :21. Both subclasses and
    derives from MetaType, as AbstractMetaclass does (:28-31), so a
    sentinel declared with a class keyword has it absorbed by _Chill.
    - __registered_sentinels__ = None, :39: the registry, always read
      and written on SentinelMeta itself whichever subclass asks.
    - _getRegisteredSentinels, :45-51: maybe(registry, []).
    - _getNamedSentinel(name), :53-63: linear search by __name__,
      KeyError when absent.
    - _registerSentinel(sentinel), :69-75: rebinds the registry to a
      new list with the sentinel appended.
    - __prepare__, :77-79: a plain dict, stated explicitly.
    - __new__(mcls, name, bases, space, **kwargs), :81-94: KeyError from
      the lookup means the name is free; otherwise DuplicateSentinel
      with the existing sentinel and space.get('__module__'). Creation
      goes through super().__new__ (MetaType.__new__) and the result is
      registered.
    - __call__, :96-100: raises IllegalInstantiation(cls) for every
      sentinel class.
    - __hash__, :102-108: hash of (metaclass module, metaclass name,
      class module, class name), replacing type's identity hash with a
      name-based one. No __eq__ is defined, so equality stays identity.
    - __str__ and __repr__, :110-113: "<Sentinel: 'NAME'>".
  - Sentinel(metaclass=SentinelMeta), :116-123: the base sentinel. It
    has no bases, so MetaType.__new__ gives it (_Chill,) and its MRO is
    Sentinel, _Chill, object. The name 'Sentinel' is itself registered.
- Interactions:
  - core: the first class statement through MetaType.__new__ after
    MetaType itself. SentinelMeta's own bases become (MetaType, _Chill)
    (MetaType is an instance of type, not of MetaType), so _Chill sits
    in a metaclass MRO: SentinelMeta, MetaType, type, _Chill, object.
    A subclass of Sentinel such as DELETED has last base Sentinel, an
    instance of SentinelMeta and so of MetaType, and nothing is
    appended.
  - dispatch: the sentinels THIS and ARGS appear in overload signatures
    (per the package docstring), so TypeSig must recognise sentinel
    classes; the name-based __hash__ is likely what lets a signature
    hash deterministically. Confirm when dispatch is read.
  - desc: THIS, OWNER, DESC are placeholders in deferred AttriBox
    arguments; DELETED is the stored value meaning 'deleted'.
  - mcls: METACALL marks dunder hooks the metaclass dispatches.
  - The registry is process-global by design (one concept per
    process), never per module.
- Support: utilities.maybe (:11, used :51); waitaminute.meta
  IllegalInstantiation and DuplicateSentinel (:12). MetaType is imported
  from the parent package (:13), which works because core/__init__.py
  binds MetaType before importing sentinels.
- Notes:
  - ARGS is documented as instantiable (sentinels/__init__.py:30-32), so
    its own metaclass must override __call__; see _args.py.
  - The registry is a list rebound on every registration, so a
    sentinel can never be unregistered through this API; a test that
    builds a sentinel with a fresh name leaves it registered for the
    rest of the process.
  - The typing names Self and Never (:16) are 3.11 names, imported only
    under TYPE_CHECKING, which is the sanctioned place for them.

## utilities/_text_fmt.py : textFmt (support, read ad hoc from the waitaminute.meta exceptions)

- Item: src/worktoy/utilities/_text_fmt.py, 78 lines, defines textFmt at
  utilities/_text_fmt.py:11.
- What it is: the formatter every exception message goes through. It
  joins its arguments with single spaces, collapses every run of
  whitespace (so a triple-quoted literal with embedded newlines and
  indentation becomes one line), and then honours two explicit tokens:
  '<br>' becomes os.linesep and '<tab>' becomes two spaces. The space on
  either side of a '<br>' is dropped (:74-76).
- Symbols: textFmt(*args, **kwargs) -> str, :11. Keywords newLineToken,
  tabToken, newLineSymbol, indentSymbol (:62-67). No args or only empty
  strings gives '' (:50-51, :59-60). Non-string arguments are converted
  with str() (:57-58); an empty string argument is dropped (:55-56).
- Interactions: used by every waitaminute exception __str__ seen so far
  (IllegalInstantiation :36, DuplicateSentinel :69). Nothing in core,
  dispatch, desc or mcls formats a message without it, so a message
  written across lines in source is always one line at the user.
- Support: none beyond os.
- Notes: the newline symbol is os.linesep, so a '<br>' renders as CRLF
  on Windows while the docstring example (:47-48) shows '\n'. The str()
  at :71 is redundant since words are already strings. No regex is
  used, in keeping with the author's preference.

## core/sentinels/_deleted.py : DELETED

- Item: src/worktoy/core/sentinels/_deleted.py, 25 lines. Second import
  of core/sentinels/__init__.py:39.
- What it is: class DELETED(Sentinel) with an empty body (:12-25). The
  value a descriptor stores in an instance's backing slot to mark the
  attribute as deleted.
- Interactions (from its docstring, to be confirmed in core/_object.py):
  a descriptor resolves a value through up to three lookups, the value
  on the instance, a default on the descriptor object, and a fallback on
  the descriptor class (:19-21). Deletion sets the first slot to
  DELETED, and Object.__get__ then raises MissingVariable (an
  AttributeError subclass from waitaminute) instead of returning it
  (:14-17, :22-23). desc's descriptors therefore implement __delete__ by
  storing DELETED rather than removing the slot.
- Support: imports Sentinel from the sentinels package (:9).

## core/sentinels/_owner.py : OWNER

- Item: src/worktoy/core/sentinels/_owner.py, 20 lines. Third import of
  core/sentinels/__init__.py:40.
- What it is: class OWNER(Sentinel), docstring-only body (:13-20). The
  placeholder for the 'owner' argument of __get__.
- Interactions: in a deferred AttriBox constructor argument it is
  replaced at access time by the owner class (:16-18). It has no role in
  overload signatures (:18-19), unlike THIS. So desc reads it, dispatch
  does not.
- Support: Sentinel from the package (:10).

## core/sentinels/_this.py : THIS

- Item: src/worktoy/core/sentinels/_this.py, 25 lines. Fourth import of
  core/sentinels/__init__.py:41.
- What it is: class THIS(Sentinel), docstring-only body (:12-25). The
  placeholder for the enclosing class, used inside a class body before
  that class exists.
- Interactions: two different resolutions, one per consumer. desc: in a
  deferred AttriBox argument it is replaced at access time by the
  instance passed to __get__ (:17-19). dispatch: in an @overload
  signature it stands for the enclosing class, matching instances of
  it, like typing.Self (:19-21). The two meanings share one sentinel,
  so TypeSig and AttriBox each own their own substitution.
- Support: Sentinel from the package (:9).

## core/sentinels/_desc.py : DESC

- Item: src/worktoy/core/sentinels/_desc.py, 18 lines. Fifth import of
  core/sentinels/__init__.py:42.
- What it is: class DESC(Sentinel), docstring-only body (:12-18). The
  placeholder for the descriptor object itself.
- Interactions: desc only. In a deferred AttriBox constructor argument
  it is replaced at access time by the descriptor mediating the access
  (:14-17). Together THIS, OWNER and DESC are the three values __get__
  knows (instance, owner, self), which is the full context a deferred
  argument can be resolved against.
- Support: Sentinel from the package (:9).

## core/sentinels/_meta_call.py : METACALL

- Item: src/worktoy/core/sentinels/_meta_call.py, 18 lines. Sixth import
  of core/sentinels/__init__.py:43.
- What it is: class METACALL(Sentinel), docstring-only body (:12-18). A
  marker value for a class-level dunder hook.
- Interactions: mcls only. When AbstractMetaclass finds METACALL as the
  value of a hook such as __class_str__ or __class_iter__ it uses its
  own implementation instead of calling the hook on the class (:14-17).
  So the __class_*__ names are routed protocols, dispatched by the
  metaclass, and METACALL is the opt-out that says 'use the metaclass
  default'. Confirm the exact routing when mcls is read.
- Support: Sentinel from the package (:9).

## core/sentinels/_args.py : ARGS, _MetaARGS

- Item: src/worktoy/core/sentinels/_args.py, 77 lines. Last import of
  core/sentinels/__init__.py:44.
- What it is: the one sentinel that is instantiated. ARGS[int] builds an
  instance whose __inner_type__ is int, marking the variadic tail of an
  overload signature.
- Symbols:
  - _MetaARGS(SentinelMeta), :17-33. A private single-purpose
    metaclass (kept private deliberately). Class variable
    __inner_type__: Optional[type] = None (:25). __call__(cls, type_)
    (:27-33) overrides the refusal in SentinelMeta.__call__: it builds
    an instance through type.__call__(cls) and sets __inner_type__ on
    the instance. Registration with SentinelMeta is unchanged, so a
    second class statement named ARGS is refused.
  - ARGS(metaclass=_MetaARGS), :36-77.
    - __iter__, :47-51: yields the instance itself, so an ARGS
      instance can be star-expanded or iterated as a one-element
      sequence.
    - __eq__, :53-56: equal only to another ARGS whose inner type is
      the identical object; NotImplemented otherwise. The explicit
      'True if ... else False' form is the author's chosen style.
    - __hash__, :58-59: hash of (class name, inner type).
    - __str__ and __repr__, :61-70: 'ARGS[int]', falling back to
      str(innerType) when it has no __name__.
    - __class_getitem__, :72-77: ARGS[T] is cls(T).
- Interactions:
  - dispatch: each subscript builds a new instance (:41-42), so the
    value-based __eq__ and __hash__ are what let a variadic signature
    in a subclass be recognised as equal to the one it overrides
    (:42-44). TypeSig is the consumer; expect it to test
    isinstance(part, ARGS) and read __inner_type__.
  - core: _MetaARGS is the first metaclass body in the library with an
    annotation (:25), so on 3.10+ MetaType.__new__ replaces its
    __annotations__ with _AnnotationsDescriptor. ARGS itself has no
    body annotation, so ARGS.__annotations__ goes through the
    descriptor to type's getset and answers an empty dict of its own,
    while _MetaARGS.__annotations__ answers {'__inner_type__': ...}.
    This is the first concrete exercise of the descriptor.
  - Its bases are () so MetaType.__new__ gives it (_Chill,), and
    SentinelMeta.__new__ registers the name 'ARGS'.
- Support: SentinelMeta from the package (:11). Typing names Self,
  Iterator, Optional under TYPE_CHECKING only.
- Notes:
  - __inner_type__ lives both as a metaclass class variable (:25, read
    as None through ARGS.__inner_type__ on the class) and as an
    instance attribute set at :32. The class-level None is the
    fallback a bare ARGS would show if ever used unsubscripted.
  - __eq__ compares inner types by identity, so ARGS[list[int]] built
    twice from two distinct generic alias objects would not compare
    equal; only plain classes and shared alias objects do.

## core/sentinels package summary

- Order read: SentinelMeta and Sentinel, DELETED, OWNER, THIS, DESC,
  METACALL, ARGS. Seven sentinels are registered at import, including
  Sentinel itself.
- Consumers by package: core.Object reads DELETED; desc reads THIS,
  OWNER, DESC and DELETED; dispatch reads THIS and ARGS; mcls reads
  METACALL. Any new sentinel anywhere in the process must pick a name
  not in the registry.

# core/control_flow package

Import order from core/control_flow/__init__.py:27-30: ControlSpace,
MetaFlow, ControlFlow, SkipSet. The package docstring (:2-21) states the
design: a signal is an exception raised to steer a protocol, used by its
type alone, so it sits beside the sentinels; MetaFlow refuses every
attribute in a signal body except __str__ and __repr__ through
ControlSpace and keeps one root class; SkipSet is the only signal the
library raises itself, from a descriptor's hookPreSet, telling
Object.__set__ to skip the write. ControlClassError lives in
waitaminute.meta; waitaminute.control_flow is a 1.x re-export.

## core/control_flow/_control_space.py : ControlSpace

- Item: src/worktoy/core/control_flow/_control_space.py, 69 lines. First
  import of core/control_flow/__init__.py:27.
- What it is: the dict subclass MetaFlow.__prepare__ returns as the
  namespace of a signal class. It refuses nearly every assignment in a
  non-root signal body at the moment the body executes.
- Symbols:
  - __white_list__, :31-39: keys always accepted: __firstlineno__,
    __str__, __repr__, __namespace__, __static_attributes__,
    __classcell__, __classdictcell__. The comment at :29-30 explains the
    last two are bound by the interpreter (super() use, and 3.14), and
    the first and fifth are compiler-set from 3.13.
  - Class variables __is_root__, __metaclass__ (annotated),
    __base_classes__, __class_name__, all None (:41-44); each is set per
    instance in __init__.
  - _getWhiteList, :46-48: maybe(cls.__white_list__, ()).
  - __init__(mcls, name, bases, **kw), :50-56: stores the metaclass,
    bases and name, reads the '_root' keyword into __is_root__, and
    sets self['__namespace__'] = self through its own __setitem__.
  - __setitem__(key, value), :58-69: a whitelisted key is stored. For a
    non-root space any other key must be an attribute Exception already
    holds and that attribute must not be callable (so __doc__,
    __module__ and __qualname__ pass, a method or new name does not);
    otherwise ControlClassError(self, key). The root space accepts
    everything.
- Interactions:
  - core: because the space carries '__namespace__', MetaType.__new__
    sees spaceState True and inserts nothing; the finished signal class
    has __namespace__ pointing at this ControlSpace in its __dict__.
    This is the first confirmation that cls.__namespace__ is a real
    feature of MetaType-made classes, not a leftover.
  - The structure (a dict subclass with metaclass, name, bases and a
    guarded __setitem__) is the small-scale model of
    mcls.AbstractNamespace. Compare when mcls is read.
- Support: utilities.maybe (:11); waitaminute.meta.ControlClassError
  (:12). MetaFlow is imported only under TYPE_CHECKING (:17).
- Notes: the whitelist test precedes the root test, so even the root
  goes through the same __setitem__; only the order of the checks
  differs from a plain dict for the root.

## core/control_flow/_meta_flow.py : MetaFlow

- Item: src/worktoy/core/control_flow/_meta_flow.py, 81 lines. Second
  import of core/control_flow/__init__.py:28.
- What it is: the metaclass of the signals. It prepares a ControlSpace,
  gives every signal a default __str__ and __repr__ that render the
  class, and keeps exactly one root class.
- Symbols:
  - MetaFlow(MetaType, metaclass=MetaType), :22. Bases become
    (MetaType, _Chill) as for SentinelMeta. The body has the bare
    annotation __is_root__: bool (:31), so on 3.10+ MetaType.__new__
    installs _AnnotationsDescriptor on MetaFlow. __root_cls__ = None (:32).
  - getRootClass, :34-36: classmethod, the registered root or None.
  - _registerRoot(cls), :38-42: refuses a second root with
    VariableNotNone('__root_cls__', existing); otherwise stores it on
    the metaclass the call went through.
  - __prepare__(mcls, name, bases, **kwargs), :44-52: builds
    ControlSpace(mcls, name, bases, **kwargs), writes __str__ and
    __repr__ (the same function from _strFactory) and __is_root__ into
    it with dict.__setitem__, bypassing the guard.
  - __new__, :54-58: super().__new__ (MetaType.__new__, which hands the
    '_root' keyword on to type.__new__ and so to __init_subclass__,
    ending at _Chill), then registers the class as root when its
    __is_root__ is True.
  - __str__ and __repr__, :60-68: '<Root: [Root]>' for the root,
    '<Root: Name>' for any other signal.
  - _strFactory, :70-81: staticmethod returning an instance __str__
    that answers str(type(self)), so an instance renders as its class.
- Interactions:
  - core: the '_root' class keyword is the first concrete class keyword
    in the library and it is absorbed by _Chill at the end of the
    ControlFlow MRO (ControlFlow, Exception, BaseException, _Chill,
    object). MetaType.__init__ receives the keyword too and ignores it.
  - Object.__set__ in core catches SkipSet, a class under this
    metaclass; nothing in dispatch or desc touches MetaFlow directly.
- Support: waitaminute.VariableNotNone (:10); MetaType from the parent
  package (:11); ControlSpace from this package (:12).
- Notes:
  - __str__ at :61-66 reads root.__name__; with no root registered and a
    non-root class asking, root is None and this would raise
    AttributeError. In practice ControlFlow registers itself at import
    before any other signal exists, so it is reachable only through a
    MetaFlow subclass with no root of its own.
  - __root_cls__ is set on 'mcls', the metaclass the call went through,
    so a subclass of MetaFlow would keep its own root while
    MetaFlow.getRootClass() keeps ControlFlow.

## core/control_flow/_control_flow.py : ControlFlow

- Item: src/worktoy/core/control_flow/_control_flow.py, 14 lines. Third
  import of core/control_flow/__init__.py:29.
- What it is: class ControlFlow(Exception, metaclass=MetaFlow,
  _root=True), docstring-only body (:11-14). The root signal.
- Interactions: it is an Exception, not a WorkToyException, which is why
  the waitaminute docstring exempts the control-flow signals from the
  common base. Its bases are (Exception,), so MetaType.__new__ appends
  _Chill (Exception is not a MetaType instance). Every other signal is
  based on it and must keep its body to __str__ and __repr__.
- Support: MetaFlow from the package (:8).

## core/control_flow/_skip_set.py : SkipSet

- Item: src/worktoy/core/control_flow/_skip_set.py, 26 lines. Last
  import of core/control_flow/__init__.py:30.
- What it is: class SkipSet(ControlFlow), docstring-only body (:12-26).
  The one signal the library raises itself.
- Interactions (from its docstring, to confirm in core/_object.py): the
  Object.__set__ wrapper catches SkipSet raised from hookPreSet and
  skips __instance_set__ and hookOnSet entirely; the caller sees no
  exception (:15-17). The sanctioned use is redundant-set elision when
  newValue already equals the held value (:20-23); any other refusal
  should raise a proper typed exception that propagates (:23-25). desc
  descriptors that implement hookPreSet are the raisers.
- Support: ControlFlow from the package (:9).

## waitaminute/meta/_control_class_error.py : ControlClassError (support)

- Item: src/worktoy/waitaminute/meta/_control_class_error.py, 52 lines.
- What it is: raised by ControlSpace.__setitem__ when a non-root signal
  body assigns a disallowed name. Based on WorkToyException then
  TypeError (:20). The docstring (:22-29) restates the whitelist and
  the Exception-non-callable rule.
- Symbols: __slots__ = ('space', 'badKey') (:32); __init__(space,
  badKey) (:34-37) calls TypeError.__init__ with nothing; __str__
  (:39-50) reads space.__metaclass__.getRootClass().__name__ and
  space.__class_name__ and formats through textFmt, which is imported
  locally inside __str__ (:49); __repr__ = __str__ (:52).
- Interactions: only ControlSpace raises it
  (core/control_flow/_control_space.py:65, :68). The TYPE_CHECKING
  import at :15 points up at core.control_flow for the annotations.
- Notes:
  - The local textFmt import at :49 differs from the module-level
    import the other meta exceptions use; it reads like a leftover
    from when the class lived in waitaminute.control_flow.
  - Derived, not executed: the captured 'space' is a ControlSpace
    whose '__str__' value is a closure from MetaFlow._strFactory, which
    pickle cannot store by reference, so WorkToyException.__reduce__
    would replace the space with a Detached stand-in. The rebuilt
    exception's __str__ then reads self.space.__metaclass__, a dunder,
    which Detached.__getattr__ refuses. This is the concrete case of
    the Detached dunder inconsistency noted under waitaminute/_detached.py.

## core/control_flow package summary

- Four items, read in order. The design mirrors sentinels: a stateless
  class used by its type (raise SkipSet, except SkipSet) instead of by
  its identity. The '_root' keyword, the ControlSpace self-registration
  under '__namespace__' and the _Chill absorption are the three places
  this package exercises MetaType.

## waitaminute/_variable_not_none.py : VariableNotNone (support, read ad hoc from MetaFlow._registerRoot)

- Item: src/worktoy/waitaminute/_variable_not_none.py, 39 lines. Fourth
  import of waitaminute/__init__.py:27.
- What it is: the write-once guard exception. Raised when a slot that
  must be assigned exactly once already holds a value. Based on
  WorkToyException then Exception (:12).
- Symbols: __slots__ = ('name', 'value') (:26); __init__(*args) (:28-30)
  unpacks name and value from the args padded with two Nones, so it
  accepts zero, one or two arguments, then calls Exception.__init__
  with nothing; __str__ (:32-37) formats "Unexpected value: 'v' at name
  'n' expected to be None!" through textFmt; __repr__ = __str__ (:39).
- Interactions: raised by MetaFlow._registerRoot
  (core/control_flow/_meta_flow.py:40-41) on a second root. Expect it
  wherever core.Object or desc guards a one-time binding such as a
  field name or owner.
- Support: utilities.textFmt (:8).

## core/_instance_owner.py : ContextInstance, ContextOwner

- Item: src/worktoy/core/_instance_owner.py, 51 lines. Fourth import of
  core/__init__.py:18.
- What it is: two non-data descriptors (only __get__) that back
  Object.instance and Object.owner. Accessed on a class they return
  themselves (:30-31, :49-50); accessed on an Object instance they
  return instance.getContextInstance() (:32) and
  instance.getContextOwner() (:51), the top of the descriptor's context
  stack.
- Interactions: they have no worktoy imports at all and know Object
  only by the two method names they call. The docstrings say
  WithoutException (waitaminute.desc) is raised when no context frame
  is active (:21-22, :40-41), which means the raise lives in Object's
  getters, not here. desc's descriptors read self.instance and
  self.owner through these two during __get__, __set__ and __delete__.
- Support: none.
- Notes: being non-data descriptors, an instance attribute named
  'instance' or 'owner' in an Object's __dict__ would shadow them; core
  presumably never writes such names. Both carry the author's
  'Python API' banner without the empty banners (see memory rule on
  omitting empty section banners).

## waitaminute/_missing_variable.py : MissingVariable (support, read ad hoc from DELETED and core/_object.py)

- Item: src/worktoy/waitaminute/_missing_variable.py, 91 lines. Last
  top-level import of waitaminute/__init__.py:30.
- What it is: the 'expected a value, found None or DELETED' exception.
  Based on WorkToyException then AttributeError (:18), so hasattr and
  getattr defaults treat it as a missing attribute.
- Symbols: __slots__ = ('instance', 'varName', 'expectedTypes') (:62);
  __init__(instance, varName, *type_) (:64-68) calls
  AttributeError.__init__ with nothing; __str__ (:70-89) renders
  "Missing 'Owner.name: Type'!" where Owner is the instance's class name,
  or the instance's own name when it is a class (:71-76), the types by
  __name__ or str (:78-80), several as Union[...] (:86-87), none as no
  type part (:81-83); __repr__ = __str__ (:91).
- Interactions: core.Object raises it from _deletedGuard
  (core/_object.py:416-419) when __instance_get__ returns DELETED, from
  getPrivateName when no field name is recorded (:431), and defensively
  in the context getters (:227, :241). This is the AttributeError a
  user sees after 'del obj.field'.
- Support: utilities.textFmt (:11).

## waitaminute/desc/_without_exception.py : WithoutException (support)

- Item: src/worktoy/waitaminute/desc/_without_exception.py, 47 lines.
- What it is: raised when a context-only descriptor method is used with
  no frame on the context stack. Based on WorkToyException then
  RuntimeError (:17).
- Symbols: __slots__ = ('desc',) (:31); __init__(desc) (:33-35);
  __str__ (:37-45) renders "Context-less call detected for descriptor at
  'Owner.field'!" using desc.getFieldOwner() and desc.getFieldName()
  with 'NO-OWNER' and 'NO-FIELD' fallbacks, importing maybe locally and
  absolutely (:42) and not going through textFmt; __repr__ = __str__.
- Interactions: raised by Object.getContextInstance and
  Object.getContextOwner on a placed descriptor with an empty stack
  (core/_object.py:233, :247) and by Object.exitContext on an empty
  stack (:407). A descriptor no class holds raises a plain
  AttributeError instead, so this is specific to a placed descriptor.
- Notes: derived, not executed: if the captured descriptor does not
  pickle and travels as Detached, the rebuilt message calls
  self.desc.getFieldOwner(); Detached.__getattr__ returns the stand-in
  for the plain name, and calling it raises TypeError since Detached is
  not callable. Second instance of the stand-in limits noted under
  waitaminute/_detached.py: attribute chains pass, method calls do not.

## waitaminute/desc/__init__.py : index of the descriptor exceptions (support)

- Item: src/worktoy/waitaminute/desc/__init__.py, 39 lines.
- What it is: the exceptions raised by the descriptor protocol in desc
  and core. Import order (:17-26): DescriptorException, AccessError,
  ProtectedError, ReadOnlyError, WithoutException, WriteOnceError,
  PhantomBoxError, MissingInstanceDict, StorageCollision,
  NamelessCallback. Per the docstring (:4-11): AccessError,
  ProtectedError, ReadOnlyError and PhantomBoxError share
  DescriptorException and the first three are AttributeErrors;
  WriteOnceError and MissingInstanceDict are TypeErrors; WithoutException
  is a RuntimeError; StorageCollision and NamelessCallback are
  SyntaxErrors, and these do not share the base.
- Interactions: core.Object uses WithoutException, ReadOnlyError and
  ProtectedError; the rest belong to desc and are read when met.

## core/_object.py : Object, _PRIVATE_KEY_PATTERN

- Item: src/worktoy/core/_object.py, 572 lines. Last import of
  core/__init__.py:19.
- What it is: the primitive base class of every worktoy descriptor and
  of every worktoy value that can sit in a class body. It implements a
  contextual descriptor protocol: __get__, __set__ and __delete__ push
  an (instance, owner) frame on a per-descriptor stack, call a small
  __instance_* hook, bracket it with notification hooks, and pop the
  frame in a finally. Inside a hook self.instance and self.owner read
  the top frame. It also captures its own constructor call, which is
  what deferred construction in desc builds on.
- Symbols:
  - _PRIVATE_KEY_PATTERN, :24: the one compiled regex in the library,
    the camelCase splitter '(?<!^)(?=[A-Z])', compiled once because
    getPrivateName is on the hot path (:22-23). This is the accepted
    exception to the no-regex preference.
  - Object(metaclass=MetaType), :27. Bases () so MetaType gives it
    (_Chill,); its MRO is Object, _Chill, object. The body is annotated
    but no base subclasses type, so no annotations descriptor.
  - Class variables (:143-148), all None: __field_owner__,
    __field_name__, __private_name__ (cache), __pos_args__,
    __key_args__, __call_chain__. Public: directory = Directory() (:151),
    instance = ContextInstance() (:152), owner = ContextOwner() (:153).
  - getFieldOwner, getFieldName, :159-163.
  - getContextualSentinels, :165-179: {THIS: top instance or THIS,
    OWNER: top owner or OWNER, DESC: self}; the stack may be empty.
  - filterSentinels(arg), :181-191: dict .get(arg, arg) with a TypeError
    guard for unhashable args; an arg that is one of the three sentinels
    is replaced, anything else returned as is.
  - getPosArgs, getKeyArgs, :193-203: the captured constructor
    arguments with sentinels substituted for the current context.
  - hasSentinelArgs, :205-219: identity test of every captured argument
    against THIS, OWNER, DESC. The docstring (:206-211) says a
    descriptor uses it to tell a value that only became an instance of
    the field type through substitution from a genuine pre-built value.
  - getContextInstance, getContextOwner, :221-247: top of stack; with
    an empty stack, plain AttributeError when the descriptor is not
    placed in any class (so hasattr and inspect.getmembers answer), and
    WithoutException when it is placed. The MissingVariable branches at
    :226-227 and :240-241 are unreachable (hasContext is False for
    None) and purely defensive.
  - hasContext, :249-254: bool of the stack.
  - __init__(*args, **kwargs), :260-265: object.__init__, then stores
    __pos_args__, __key_args__ and an empty __call_chain__ with
    object.__setattr__ to bypass any subclass __setattr__. Every
    argument is accepted and captured, none is validated here.
  - __set_name__(owner, name, **kwargs), :271-277: records owner and
    name via object.__setattr__, then hookSetName(owner, name, **kwargs).
    The **kwargs exist for manual callers; Python passes none.
  - __get__(instance, owner), :279-296: class access returns self;
    otherwise createContext, hookPreGet, __instance_get__(instance,
    owner), _deletedGuard, hookOnGet, exitContext in finally.
  - __set__(instance, newValue, **kwargs), :298-316: the frame's owner
    is type(instance) since Python passes no owner; hookPreSet may
    raise SkipSet, which is swallowed and skips both __instance_set__
    and hookOnSet; otherwise hookOnSet receives the value
    __instance_set__ returned, or the assigned value when it returned
    None.
  - __delete__(instance, **kwargs), :318-342: reads the old value with
    __instance_get__(instance, owner, _deleting=True, **kwargs), an
    AttributeError from that read becoming None, a DELETED result
    going through _deletedGuard; then hookPreDelete, __instance_delete__
    (instance, oldVal), hookOnDelete. No SkipSet handling here.
  - __instance_get__, :348-358: default returns self.
  - __instance_set__, :360-370: default raises ReadOnlyError(instance,
    self, value).
  - __instance_delete__, :372-385: default raises ProtectedError
    (instance, self, old).
  - createContext, exitContext, :387-410: push and pop by rebinding a
    copied list through object.__setattr__; exitContext on an empty
    stack raises WithoutException. createContext tolerates the None
    class default, so a subclass that skips Object.__init__ still has a
    working stack.
  - _deletedGuard, :412-420: DELETED becomes MissingVariable(instance,
    field name, object), or MissingVariable(instance, '__field_name__',
    str) when the descriptor has no name.
  - getPrivateName, :422-437: '__foo_bar__' from 'fooBar', cached in
    __private_name__ on first use; MissingVariable before __set_name__;
    TypeException if the cache holds a non-string.
  - hookPreGet, hookOnGet, hookPreSet, hookOnSet, hookPreDelete,
    hookOnDelete, hookSetName, :439-527: no-op notification hooks.
  - parseKwargs(cls, *args, **kwargs), :529-572: classmethod. Types and
    string keys are picked out of args (other args ignored silently);
    no keys gives (None, copy); types default to [object]; complex
    admits float and int, float admits int, bool passes as int by
    isinstance. The first key present whose value matches a type is
    removed and returned with the remaining kwargs; a present key with
    a non-matching value raises TypeException(key, value, *types); no
    key present gives (None, copy). Only one key is ever consumed per
    call.
- Interactions:
  - core: uses MetaType (:27), the sentinels THIS, DESC, OWNER, DELETED,
    Sentinel (:16), SkipSet (:15), ContextInstance and ContextOwner
    (:17). The class docstring (:100-114) fixes the design that a
    worktoy value in a class body is a shared read-only class
    attribute: reads return the object itself, instance writes raise
    ReadOnlyError, instance deletions ProtectedError, and class-level
    writes bypass the descriptor protocol as with type.
  - dispatch: the docstring (:54-58) names Dispatcher as a subclass that
    overrides __get__, __set__ and __delete__ itself and uses Object
    only for the field name and owner that __set_name__ records.
  - desc: the docstring names Alias the same way. The boxes are
    expected to implement __instance_get__/__instance_set__/
    __instance_delete__, to use getPrivateName for their per-instance
    storage key, to raise SkipSet from hookPreSet for redundant-set
    elision, to resolve deferred arguments through getPosArgs and
    getKeyArgs, and to honour _deleting=True by not building a default
    during a deletion.
  - mcls: AbstractSpaceHook is the third named subclass overriding the
    entry points (:55-56). The namespace machinery presumably calls
    __set_name__ with keywords (:271 accepts **kwargs).
- Support: utilities.Directory and maybe (:11); waitaminute
  TypeException and MissingVariable (:12); waitaminute.desc
  WithoutException, ReadOnlyError, ProtectedError (:13-14). Directory,
  TypeException, ReadOnlyError, ProtectedError and their base
  DescriptorException are read next.
- Notes:
  - The owner in a __set__ or __delete__ frame is type(instance), which
    for an instance of a subclass is the subclass, while the owner in a
    __get__ frame is whatever class Python passed. self.owner therefore
    means slightly different things in the three hooks.
  - Deleting twice: an __instance_get__ that returns DELETED makes the
    second deletion raise MissingVariable from the else branch at :337
    (the except at :334 covers only the read itself), before
    hookPreDelete runs; an __instance_get__ that raises AttributeError
    instead lets the second deletion proceed with old=None. Two
    subclass styles, two behaviours.
  - hookOnSet receives maybe(storedValue, newValue), so a box whose
    __instance_set__ deliberately stores None reports the assigned
    value, not None.
  - The context stack is per descriptor object and shared across all
    owning instances; the docstring (:86-98) states the resulting
    thread and coroutine limitation openly.
  - getPrivateName maps 'fooBar' and 'foo_bar' to the same
    '__foo_bar__', so two such fields on one class share storage;
    StorageCollision in waitaminute.desc exists for exactly this and is
    expected to be raised by desc or mcls, not here.
  - parseKwargs treats a bool as an int through isinstance, which the
    docstring (:540) states; the value is returned uncast (:540-541).
  - The temporary '__namespace__' from MetaType.__new__ stays in
    Object.__dict__, pointing at Object's original class namespace dict
    (derived, not executed).

## utilities/_directory.py : Directory (support, read ad hoc from Object.directory)

- Item: src/worktoy/utilities/_directory.py, 55 lines.
- What it is: a plain-class data descriptor (no worktoy base) that
  answers, on instance access, the absolute directory of the source
  file behind the instance's class module, so a class can find
  resources beside its own file.
- Symbols: __field_name__ = None (:30); __set_name__ records the name
  (:32-34); __get__ (:36-47) returns self on class access, otherwise
  looks the module up in sys.modules and takes dirname of its __file__;
  a module with no __file__ (REPL, exec) raises MissingVariable
  (instance, name, str) chained from the AttributeError, with the
  recorded name or 'directory' as fallback; __set__ (:49-51) raises
  ReadOnlyError; __delete__ (:53-55) raises ProtectedError with no old
  value.
- Interactions: placed on Object as the public class variable directory
  (core/_object.py:151), so every descriptor and every Object-based
  value can read self.directory. The three imports from waitaminute are
  local to the methods (:44, :50, :54): utilities loads before
  waitaminute, so this breaks a real import cycle and is intentional.
- Notes: it is a data descriptor outside the Object protocol, so it
  never pushes a context frame; it also records only the name, not the
  owner. The typing name Never (:14) is under TYPE_CHECKING only.

## waitaminute/_type_exception.py : TypeException (support, read ad hoc from Object.getPrivateName and parseKwargs)

- Item: src/worktoy/waitaminute/_type_exception.py, 63 lines. Third
  import of waitaminute/__init__.py:26.
- What it is: the library's TypeError for a value of the wrong type at a
  checked boundary, described as the most widely raised exception
  (:19-21). It must not be used for None, which belongs to
  MissingVariable (:23-25). Based on WorkToyException then TypeError.
- Symbols: __slots__ = ('varName', 'actualObject', 'actualType',
  'expectedTypes') (:40); __init__(name, obj, *types) (:42-47) calls
  TypeError.__init__ with nothing first, then stores name, object, its
  type and the accepted types in order; __str__ (:49-61) renders
  "Expected object at name 'n' to be an instance of 'A' or 'B', but
  received object: 'repr' of type 'T'!", truncating a repr beyond 50
  characters (:57-58) and naming typing aliases by str when they have
  no __name__ (:52-54); __repr__ = __str__.
- Interactions: raised by Object.parseKwargs (core/_object.py:570) when a
  keyword is present with a wrong type and defensively by
  getPrivateName (:437). Expect it at every cast and signature boundary
  in dispatch and desc.
- Support: utilities.textFmt and joinWords (:10).

## waitaminute/desc/_descriptor_exception.py : DescriptorException (support)

- Item: src/worktoy/waitaminute/desc/_descriptor_exception.py, 47
  lines. First import of waitaminute/desc/__init__.py:17.
- What it is: the shared base of AccessError, ProtectedError,
  ReadOnlyError and PhantomBoxError, based on WorkToyException then
  Exception (:18); WriteOnceError and WithoutException stay outside it
  (:24-27).
- Symbols: _fieldName(instance, desc), :30-47, a staticmethod the
  messages use. It answers desc.__field_name__ when recorded, otherwise
  searches the dicts of type(instance).__mro__ for a value that is desc
  by identity, otherwise 'object'. The docstring (:33-38) gives the
  identity case its reason: a KeeNum member placed in a class body is a
  shared singleton that may sit under several names and records none.
- Interactions: the identity search is what makes ReadOnlyError and
  ProtectedError name a worktoy value in a class body (the read-only
  class attribute design in Object's docstring) even when the value
  never received __set_name__.
- Notes: the search is by identity so a value that appears under two
  names answers the first one in MRO and dict order.

## waitaminute/desc/_read_only_error.py : ReadOnlyError (support)

- Item: src/worktoy/waitaminute/desc/_read_only_error.py, 55 lines.
- What it is: the refusal of a write to a read-only attribute, based on
  DescriptorException then AttributeError (:17), so code that skips what
  it cannot set through 'except AttributeError' skips worktoy
  attributes too (:21-24).
- Symbols: __slots__ = ('instance', 'desc', 'newVal') (:37); __init__
  (instance, desc, val) (:39-43) ends in DescriptorException.__init__
  with nothing, which resolves through the MRO to AttributeError's;
  __str__ (:45-53) renders "Attempted to overwrite read-only attribute
  'Owner.field' with new value: 'v'!" using _fieldName; __repr__ =
  __str__.
- Interactions: raised by the default Object.__instance_set__
  (core/_object.py:370), by Directory.__set__, and per the docstring by
  QuickDesc in utilities and any descriptor forbidding writes.
- Support: utilities.textFmt (:11).

## waitaminute/desc/_protected_error.py : ProtectedError (support)

- Item: src/worktoy/waitaminute/desc/_protected_error.py, 55 lines.
- What it is: the refusal of a deletion, based on DescriptorException
  then AttributeError (:17), for the same catchability reason.
- Symbols: __slots__ = ('instance', 'desc', 'oldVal') (:37); __init__
  (instance, desc, oldValue=None) (:39-43); __str__ (:45-53) renders
  "Attempted to delete protected attribute 'Owner.field' with value:
  'old'" using _fieldName; __repr__ = __str__.
- Interactions: raised by the default Object.__instance_delete__
  (core/_object.py:385) with the old value Object.__delete__ read first,
  and by Directory.__delete__ without one.
- Support: utilities.textFmt (:11).

## core package summary

- Items read, in order: _annotations_descriptor (unexported sibling),
  _meta_type (MetaType, _Chill), sentinels (SentinelMeta, Sentinel,
  DELETED, OWNER, THIS, DESC, METACALL, ARGS with _MetaARGS),
  control_flow (ControlSpace, MetaFlow, ControlFlow, SkipSet),
  _instance_owner (ContextInstance, ContextOwner), _object (Object).
- The spine: MetaType makes every worktoy class end its MRO in _Chill
  (class keywords die there), gives annotated metaclass bodies the
  annotations descriptor, and leaves '__namespace__' in every class
  __dict__. SentinelMeta and MetaFlow are the two primitive metaclasses
  built on it before mcls exists. Object is the descriptor base with
  the context stack, the captured constructor call, the DELETED
  translation, the private-name cache and the SkipSet elision.
- Open threads to resolve in later packages: who reads __skip_hash__;
  who reads cls.__namespace__; whether any worktoy metaclass body lacks
  annotations (the 3.10+ plain-dict shadowing); where StorageCollision
  is raised for colliding private names; how TypeSig treats THIS and
  ARGS; how AttriBox resolves THIS, OWNER, DESC through getPosArgs.

## utilities/_join_words.py : joinWords (support, read ad hoc from TypeException)

- Item: src/worktoy/utilities/_join_words.py, 55 lines.
- What it is: joins words into a phrase: '' for none, the word for one,
  'a and b' for two, 'a, b and c' beyond, with sep='or' for a
  disjunction (:46-55). Arguments are flattened first with
  unpack(*words, strict=False) (:47), so lists and tuples of words are
  accepted in source order while strings stay atomic.
- Interactions: TypeException.__str__ uses it with sep='or' to list the
  accepted types (waitaminute/_type_exception.py:55). Expect it in other
  messages that list names.
- Support: utilities.unpack (:8).

## utilities/_unpack.py : unpack, _iterate, _flatten (support)

- Item: src/worktoy/utilities/_unpack.py, 108 lines.
- What it is: recursive flattening of positional arguments. str, bytes
  and bytearray are atomic (:93-95); an iterable is expanded one level
  with shallow=True or all the way down otherwise (:96-103); a
  non-iterable is kept (:104); with strict=True (the default) a call
  with no iterable at all, including an empty call, raises
  UnpackException (:85-89, :105-108).
- Symbols:
  - _iterate(arg), :15-26: None unless arg is a collections.abc
    Iterable and iter(arg) succeeds. The docstring (:17-20) records
    why the try is needed: every worktoy class claims to be iterable
    because its metaclass defines __iter__ for the __class_iter__
    hook, and iterating one without the hook raises TypeError.
  - _flatten(arg, items), :29-39: an item that is arg itself is kept
    whole (ARGS yields itself; a list may contain itself), everything
    else recurses through unpack(item, shallow=False, strict=False).
  - unpack(*args, **kwargs), :42-108.
- Interactions:
  - core: this is where ARGS.__iter__ yielding itself pays off: unpack
    sees ARGS as iterable, iterates it, meets itself and keeps it as
    one element (:35-37). So a signature flattened through unpack keeps
    an ARGS[int] intact. Expect TypeSig in dispatch to rely on this.
  - mcls: the TypeError fallback at :23-26 is a contract with
    AbstractMetaclass.__iter__: a class without __class_iter__ must
    raise TypeError from iter(), not return an empty iterator, or
    unpack would silently drop it. Verify when mcls is read.
- Support: UnpackException imported locally from waitaminute (:87,
  :107), the sanctioned utilities-to-waitaminute lazy import.
- Notes: strict defaults to True, so unpack(1, 2) raises; callers that
  flatten possibly-plain arguments must pass strict=False as joinWords
  does.

# Package: dispatch

Import order from dispatch/__init__.py:21-27: flexCall and isFlex,
CallMeMaybe, Permuter, PermuterMethod, TypeSig, Dispatcher, overload.
The package docstring (:2-8) sets the division of labour: overload only
records signatures; BaseMeta in mcls compiles them into a Dispatcher
during class construction; the tools are meant to be used through a
BaseObject subclass or by wiring a Dispatcher onto a class by hand.

## waitaminute/_unpack_exception.py : UnpackException (support, read ad hoc from unpack)

- Item: src/worktoy/waitaminute/_unpack_exception.py, 42 lines. Fifth
  import of waitaminute/__init__.py:28.
- What it is: raised by unpack in strict mode when no argument is an
  unpackable iterable. Based on WorkToyException then ValueError (:13).
- Symbols: __slots__ = ('posArgs',) (:28); __init__(*args) (:30-32);
  __str__ (:34-40) lists each argument on its own indented line using
  the '<br><tab>' tokens of textFmt and tells the caller to pass
  strict=False; __repr__ = __str__.
- Interactions: only unpack raises it (utilities/_unpack.py:88, :108).
  Any dispatch or desc call that unpacks user arguments in strict mode
  surfaces this ValueError.

## waitaminute/dispatch/__init__.py : index of the overload exceptions (support)

- Item: src/worktoy/waitaminute/dispatch/__init__.py, 21 lines. Three
  exceptions in order (:13-15): DispatchException, DuplicateSignature,
  TypeCastException. Read ad hoc when the dispatch modules raise them.

## dispatch/_flex_call.py : flexCall, isFlex, _missingNames

- Item: src/worktoy/dispatch/_flex_call.py, 161 lines. First import of
  dispatch/__init__.py:21.
- What it is: a wrapper giving a plain function truncating
  positional-argument dispatch: extra positional arguments beyond the
  declared positional count are dropped, a required positional
  parameter left without a value by position or keyword raises
  TypeError, keywords pass through unchanged.
- Symbols:
  - _CO_VARARGS = 0x04 (:17), the CPython code flag for *args;
    _FLEX_MARKER = '__flex_wrapped__' (:18), the idempotency marker.
  - isFlex(func), :21-41: True when the marker attribute exists.
  - _missingNames(requiredNames, received, kwargs), :44-62: the required
    positional names after the first 'received' that kwargs does not
    name. A positional-only parameter named by keyword counts as
    supplied here and the wrapped function then refuses it itself.
  - flexCall(func), :65-161. Not a FunctionType raises TypeException
    (:109-110). Returned unchanged: an already-wrapped function
    (:113-114), a *args function (:119-120), a dunder (:124-126). Arity
    is cached at wrap time (:130-132): maxPos = co_argcount, minPos =
    co_argcount minus the number of defaults, requiredNames =
    co_varnames[:minPos]. The wrapper (:134-146) raises a plain
    TypeError with a textFmt message naming the missing parameters
    through joinWords, truncates args to maxPos, and calls func.
    Metadata is copied by hand (:150-157): __dict__, __name__,
    __qualname__, __module__, __doc__, __annotations__, __wrapped__,
    then the marker.
- Interactions:
  - desc: the docstring (:67-70) says the descriptor notification
    callbacks of BaseDescriptor are wrapped this way because a
    descriptor passes each of them the same arguments however few it
    declares. So a user callback 'def onSet(self, instance)' silently
    drops the value argument.
  - mcls: every plain function in the body of a class whose namespace
    declares FlexCallHook is wrapped (:70-71); an ordinary method is
    otherwise left alone (:71-72).
  - core: no contact.
- Support: utilities.joinWords and textFmt (:11); waitaminute
  TypeException (:12).
- Notes:
  - isFlex tests presence of the marker while flexCall tests its truth
    (:113), so a function carrying the marker set to False reads as
    flex to isFlex yet is wrapped again by flexCall. Only flexCall sets
    the marker, always True, so this cannot arise from library code.
  - co_argcount counts positional-only and positional-or-keyword
    parameters, including self on a method, and excludes keyword-only
    ones, which travel in kwargs untouched.
  - The wrapper is a plain function, so placed in a class body it binds
    as a method exactly as the original would.
  - __annotations__ is shared by reference with the original (:155).

## dispatch/_call_me_maybe.py : CallMeMaybe, _Wrapped

- Item: src/worktoy/dispatch/_call_me_maybe.py, 194 lines. Second import
  of dispatch/__init__.py:22.
- What it is: a minimal callable wrapper. An instance holds one function
  and forwards calls to it through __call__ and an overridable invoke.
  It deliberately is not a descriptor: __set_name__ always raises, so
  it cannot sit in a class body; it exists for the overload.flex
  machinery where descriptor binding would interfere (:46-51).
- Symbols:
  - T = TypeVar('T') (:17).
  - _Wrapped(QuickDesc, Generic[T]), :20-33: a QuickDesc subclass whose
    __get__ reads the one-tuple stored at the instance's private key
    and returns its first element, raising MissingVariable when the key
    or the tuple is None and TypeException when either has the wrong
    type.
  - CallMeMaybe, :36. __function_case__ = None (:62) holds the
    one-tuple; __wrapped__ = _Wrapped('__function_case__') (:65) exposes
    the function under the name inspect.unwrap looks for.
    - _getWrappedFunction, :71-95: the tuple's first element,
      MissingVariable when unset. The docstring (:76-91) explains the
      one-tuple as a defence against FunctionType.__get__ binding.
    - setFunction(func), :101-112: stores (func,).
    - __init__(func=None), :118-122: a non-callable func raises
      TypeException('func', func, Callable); None leaves it unset.
    - __call__, :128-130: invoke(self._getWrappedFunction(), *args,
      **kwargs).
    - __set_name__, :132-156: raises a plain TypeError (textFmt) on
      every call, so class creation refuses a CallMeMaybe in a body.
    - __getattr__(key), :158-166: '__function_case__' and '__wrapped__'
      go to object.__getattribute__; any other missing attribute is
      looked up on the wrapped function (so __name__, __doc__,
      __code__ and the flex marker read through), falling back to the
      normal AttributeError.
    - invoke(func, *args, **kwargs), :172-194: passthrough.
- Interactions:
  - dispatch: Permuter subclasses it and overrides invoke; the
    overload.flex machinery is the stated consumer. Dispatcher is not
    based on it (Dispatcher is an Object per core/_object.py:54-55).
  - core, desc, mcls: none directly.
- Support: utilities.textFmt and QuickDesc (:11); waitaminute
  MissingVariable and TypeException (:12). QuickDesc is read next.
- Notes:
  - Derived from Python's attribute rules, not executed: a function
    stored in an instance __dict__ is never bound; binding happens only
    when the function is found on the class. The one-tuple therefore
    protects only a function stored on the class itself, which
    setFunction never does. The tuple is harmless, and the docstring's
    stated reason (:78-83) overstates the hazard for per-instance
    storage.
  - When no function is set, reading self.__wrapped__ raises
    MissingVariable, an AttributeError, which triggers __getattr__
    (:158) for '__wrapped__', which re-reads the descriptor and raises
    it again; the result is the right exception by a roundabout route.
  - The typing name Self (:15) is under TYPE_CHECKING only.

## dispatch/_permuter.py : Permuter

- Item: src/worktoy/dispatch/_permuter.py, 225 lines. Third import of
  dispatch/__init__.py:23.
- What it is: a CallMeMaybe that holds an Arrangement and, at call time,
  permutes the received positional arguments back into the canonical
  order the wrapped function expects (:31-35). It is how a Dispatcher
  can accept one overload's arguments in several orders.
- Symbols:
  - __arg_arrangement__ = None (:57); arrangement =
    QuickDesc('__arg_arrangement__') (:60), the public read.
  - _getArrangement, :66-74: MissingVariable when unset.
  - setArrangement(arrangement), :80-100: TypeException for a
    non-Arrangement, WriteOnceError(self, old, new) on a second call.
  - __init__(*args), :119-158: at most two positional arguments, in any
    order, one Arrangement and one types.FunctionType; a third argument
    or a duplicate kind raises ValueError with a textFmt message; any
    other type raises TypeException('arg', arg, Arrangement, Func);
    then super().__init__(_func) and setArrangement when given. The
    typing.overload stubs at :106-117 only document the shapes.
  - newArrangement(original, arrangement), :160-181: classmethod
    building cls(original.__wrapped__, arrangement), the same function
    under a new arrangement.
  - __lshift__, :187-191: permuter << arrangement gives a new Permuter;
    __ilshift__, :193-197: permuter <<= arrangement sets in place
    (write-once) and returns self; __rrshift__, :199-200: arrangement
    >> permuter is permuter << arrangement. Non-Arrangement operands
    return NotImplemented.
  - invoke(func, *args, **kwargs), :206-225:
    func(*arrangement.restoreFrom(*args), **kwargs).
- Interactions:
  - dispatch: Dispatcher or overload are expected to build one Permuter
    per accepted argument order of an overload; TypeSig may carry the
    Arrangement. Confirm in _type_sig.py and _dispatcher.py.
  - core: none. desc: WriteOnceError is borrowed from the descriptor
    exceptions for the write-once arrangement.
- Support: CallMeMaybe (:12, imported as '..dispatch', which is this
  package); utilities.textFmt and QuickDesc (:13);
  utilities.combinatorics.Arrangement (:14); waitaminute TypeException
  and MissingVariable (:15); waitaminute.desc.WriteOnceError (:16).
  Arrangement and WriteOnceError are read next.
- Notes: only types.FunctionType passes as the function (:142), so a
  bound method, a builtin or another callable is refused with
  TypeException even though CallMeMaybe itself accepts any callable.
  The ValueError messages (:121-127, :134-141, :146-153) are plain
  ValueErrors, not worktoy exceptions.

## dispatch/_permuter_method.py : PermuterMethod

- Item: src/worktoy/dispatch/_permuter_method.py, 48 lines. Fourth
  import of dispatch/__init__.py:24.
- What it is: a Permuter whose invoke (:24-48) takes the calling
  instance as the first positional argument, forwards it untouched, and
  permutes only the remaining positional arguments:
  func(instance, *arrangement.restoreFrom(*args), **kwargs).
- Interactions: the shape a Dispatcher needs for a method: it receives
  (instance, *args) from its own __get__ binding and hands the instance
  through while the signature's permutation applies to the arguments
  after it. Confirm in _dispatcher.py.
- Support: Permuter from the package (:11).
- Notes: instance defaults to None (:24), so a call with no positional
  arguments forwards None as the instance rather than failing here.

## utilities/_quick_desc.py : QuickDesc (support, read ad hoc from CallMeMaybe and Permuter)

- Item: src/worktoy/utilities/_quick_desc.py, 94 lines.
- What it is: the foundation packages' own minimal read-only descriptor,
  Generic[T]. Built with the name of a private attribute, it reads that
  attribute on instance access and refuses writes and deletions. The
  docstring (:28-31) tells project authors to prefer AttriBox and Field
  from desc.
- Symbols: class defaults __private_key__, __field_name__,
  __field_owner__ = None (:47-49); __get__ (:62-72) returns self on
  class access, MissingVariable when no key was given (local import,
  reason at :66-69), else getattr(instance, key); __set__ (:74-78)
  raises ReadOnlyError and __delete__ (:80-82) ProtectedError, both
  imported locally; __set_name__ (:84-91) refuses a key equal to the
  field name with a plain ValueError and records name and owner;
  __init__(key) (:93-94). The typing.overload stubs (:55-60) only type
  the two __get__ shapes.
- Interactions: dispatch uses it for CallMeMaybe.__wrapped__ (through
  the _Wrapped subclass), Permuter.arrangement, and the four public
  views on Arrangement and the two on Arrangements. It is a data
  descriptor, so it shadows an instance attribute of the same name.
  Being outside Object it pushes no context frame and has no hooks.
- Notes: getattr(instance, key) returns the class-level None default
  without complaint when the private slot was never set, so a QuickDesc
  read never signals absence by itself; the owning class's _get* method
  does that with MissingVariable.

## waitaminute/desc/_write_once_error.py : WriteOnceError (support, read ad hoc from Permuter.setArrangement)

- Item: src/worktoy/waitaminute/desc/_write_once_error.py, 52 lines.
- What it is: the refusal of a second write to a write-once attribute,
  named for FixBox fields and Permuter arrangements (:19-21). Based on
  WorkToyException then TypeError (:17); it is not a DescriptorException.
- Symbols: __slots__ = ('desc', 'oldValue', 'newValue') (:33); __init__
  (desc, oldVal, newVal) (:35-39); __str__ (:41-50) renders "Attempted
  to overwrite write-once attribute at 'Owner.field' having existing
  value: 'old' with new value: 'new'!", reading __field_owner__ and
  __field_name__ off desc with 'Unknown' fallbacks; __repr__ = __str__.
- Interactions: Permuter.setArrangement raises it with desc=self
  (dispatch/_permuter.py:99). A Permuter has neither __field_owner__
  nor __field_name__ (its __getattr__ forwards to the wrapped function,
  which has none either), so that message reads 'Unknown.Unknown'.
  desc's FixBox is the other raiser.
- Support: utilities.textFmt (:10).

## utilities/combinatorics/__init__.py and _index_permutations.py : indexPermutations (support)

- Items: src/worktoy/utilities/combinatorics/__init__.py, 19 lines,
  exporting indexPermutations, Arrangement, Arrangements in that order
  (:11-13, __all__ as a tuple at :15-19);
  src/worktoy/utilities/combinatorics/_index_permutations.py, 57 lines.
- What it is: indexPermutations(n) (:17-57) returns an iterator over
  every permutation of (0, ..., n-1) in lexicographic order, n! of
  them, built by a recursive inner generator (:48-55). A negative n
  raises ValueError at call time (:45-46), before anything is drawn.
- Interactions: only Arrangements uses it.

## utilities/combinatorics/_arrangement.py : Arrangement (support, read ad hoc from Permuter)

- Item: src/worktoy/utilities/combinatorics/_arrangement.py, 182 lines.
- What it is: one permutation of a ground tuple, Generic[ItemTypeT],
  holding both index recipes. forward[k] is the position in items that
  fills slot k of values; inverse[k] is the slot where items[k] landed
  (:32-37). The docstring (:39-44) insists on applyTo and restoreFrom
  over the raw recipes, since confusing the two fails silently on every
  involution and only shows on 3-cycles.
- Symbols: private slots __ground_items__, __forward_indices__,
  __inverse_indices__, __current_order__ (:52-55) read through the
  QuickDesc views items, forward, inverse, values (:58-61); __init__
  (items, forward) (:67-84) validates length and that forward is a
  permutation of the positions (plain ValueErrors via textFmt),
  computes values and the inverse; __len__ (:90-91) and __iter__ over
  values (:93-94); __eq__ (:96-101) compares values with another
  Arrangement or a tuple, NotImplemented otherwise; __hash__ is
  hash(values) (:103-104); __str__ '<Arrangement: a, b>' (:106-110) and
  __repr__ as the constructor call (:112-118); applyTo(*values)
  (:124-152) maps items order to values order through forward;
  restoreFrom(*values) (:154-182) maps values order back to items
  order through inverse; both check the length.
- Interactions: Permuter.invoke calls restoreFrom on the received
  arguments (dispatch/_permuter.py:225), so a Permuter's arrangement
  has items in the wrapped function's canonical parameter order and
  values in the order the caller is allowed to use. Equality and hash
  are by values alone, which is what lets Arrangements deduplicate.
- Support: QuickDesc and textFmt from utilities (:10).

## utilities/combinatorics/_arrangements.py : Arrangements (support)

- Item: src/worktoy/utilities/combinatorics/_arrangements.py, 139 lines.
- What it is: the deduplicated set of all arrangements of a ground tuple
  (:28-33): repeated items collapse, so ('A', 'A', 'B') yields three,
  not six.
- Symbols: __ground_items__, __cached__, __is_hashable__ (:46-48) with
  views items and permutations (:51-52); __init__(*items) builds the
  cache at once (:58-60); _createIsHashable and isHashable (:66-85)
  probe hash() on every item, using the '_recursion' keyword sentinel
  pattern the author uses deliberately for peek-then-recurse;
  _buildCacheHashed (:91-101) dedupes with a set of values,
  _buildCacheNoHash (:103-113) with a list; _buildCache picks one
  (:115-119); __iter__, __len__, __getitem__, __contains__ (:125-139),
  the last accepting an Arrangement or a values tuple.
- Interactions: expected consumer is the flex machinery in dispatch,
  enumerating the orders in which an overload's typed parameters may
  be supplied. n! growth bounds practical signature length.
- Support: Arrangement and indexPermutations from the subpackage
  (:10); QuickDesc (:11).

## dispatch/_type_sig.py : TypeSig

- Item: src/worktoy/dispatch/_type_sig.py, 320 lines. Fifth import of
  dispatch/__init__.py:25.
- What it is: the hashable, ordered tuple of classes that keys one
  overload. Equality and hashing go by identity of each entry in
  declared order, with one exception: an ARGS entry compares and
  hashes by its inner type, since every ARGS[int] subscript is a new
  instance (:24-31). A signature keeps the types it was declared with
  beside the types it dispatches on, so THIS can be swapped for the
  finished class and put back (:45-49).
- Symbols:
  - Class defaults __raw_types__ = None, __declared_types__ = None,
    __allow_flex__ = True (:84-86). The flag says whether the
    dispatcher's slow path may try typeCast against this signature;
    overload.flex and Dispatcher.flex set it False on generated
    signatures, and overload and Dispatcher.overload set it False on a
    signature naming THIS unless strict=False, because casting to the
    class calls the class on the argument and a class accepting
    anything would take every call (:33-43).
  - getRawTypes, getDeclaredTypes, :92-100.
  - namesTHIS(*types), :102-113: THIS as an entry or as the inner type
    of any ARGS entry.
  - _getTypeName(rawType), :115-124: an ARGS in subscript form, a
    class by __name__.
  - __init__(*rawTypes), :130-132: raw and declared start as the same
    tuple.
  - fromArgs(*args), :134-151: the types of concrete arguments, the
    lookup key of a call.
  - validateTypes(*types, variadic=True), :153-207: each entry must
    have a metaclass as its type (issubclass(type(entry), type), chosen
    because isinstance(list[int], type) is True on 3.9 and 3.10), else
    TypeException('types[i]', entry, type); a trailing ARGS is unwrapped
    to its inner type only when variadic is True, so a misplaced ARGS
    fails the class test; OWNER raises a plain TypeError (:195-199);
    an entry isinstance refuses, such as typing.Any, raises TypeError
    chained from the probe isinstance(None, entry) (:200-207).
  - __iter__, __hash__ (hash of the raw tuple), __len__, __contains__
    (by identity), :213-226.
  - __eq__, :228-239: same class, same length, each pair identical or
    an ARGS pair equal by inner type.
  - __str__ '<TypeSig: [int, str]>' and __repr__ 'TypeSig(int, str)',
    :241-250.
  - __call__(this=None, owner=None), :252-285: a new signature with
    bare THIS and OWNER entries substituted where an argument was
    given, carrying __allow_flex__; a call with neither is a copy,
    which Dispatcher._copySig relies on (:256-258).
  - swapTHIS(thisType), :291-312: in place, THIS becomes the class and
    a trailing ARGS[THIS] becomes ARGS[class]; declared types untouched.
  - restoreTHIS, :314-320: raw types reset to the declared tuple.
- Interactions:
  - core: THIS and OWNER are sentinel classes, so a signature holding
    THIS hashes through SentinelMeta.__hash__ (by names), the same in
    every class body, which the docstring (:57-70) argues is harmless
    because such a signature keys only one overload object's registry
    until swapTHIS runs, after which registries are only iterated and
    the dispatcher compiles fresh tables. ARGS instances are recognised
    by isinstance and read through __inner_type__.
  - dispatch: Dispatcher derives call keys with fromArgs, copies with
    __call__, and swaps THIS once the class exists; overload validates
    with validateTypes.
  - mcls: BaseMeta is the caller that knows when the class exists and
    so when swapTHIS can run; a clone placed on a subclass restores and
    re-swaps (:45-49).
- Support: core.sentinels THIS, OWNER, ARGS (:10); utilities.textFmt
  (:11); waitaminute.TypeException (:12).
- Notes:
  - __call__ substitutes only a bare THIS entry; a trailing ARGS[THIS]
    passes through unchanged, unlike swapTHIS. A substituted copy also
    has the substituted types as its declared types, so restoreTHIS on
    a copy cannot bring the sentinel back.
  - __hash__ depends on mutable state (swapTHIS rebinds __raw_types__),
    so a TypeSig used as a dict key before the swap is found under a
    different hash after it; the docstring owns this and the dispatcher
    is expected to rebuild its tables.
  - A THIS entry is a class with a metaclass, passes validateTypes, and
    isinstance(None, THIS) is a valid probe.

## waitaminute/dispatch/_dispatch_exception.py : DispatchException (support)

- Item: src/worktoy/waitaminute/dispatch/_dispatch_exception.py, 88
  lines.
- What it is: the failure of a Dispatcher to resolve a call to a
  registered overload. Based on WorkToyException then TypeError (:28).
- Symbols: __slots__ = ('dispatch', 'posArgs', 'keyArgs') (:49);
  __init__(dispatch, args, kwargs=None) (:51-60); __str__ (:62-86) is a
  got-then-expected report naming 'Owner.field' from the dispatcher's
  __field_owner__ and __field_name__, each received argument with its
  type and repr, the received keyword names when any, the argument
  signature via TypeSig.fromArgs (imported locally from dispatch,
  :64) and the declared signatures from dispatch._getDeclaredSigs()
  (:73), a variadic declaration showing as itself rather than as the
  expansions it produced (:71-72).
- Interactions: raised by Dispatcher for an unmatched call; the
  message depends on the Dispatcher having been placed (an unplaced
  one has __field_owner__ None and the message would fail on
  owner.__name__). The TYPE_CHECKING block (:20-25) records that
  'overload' objects become 'Dispatcher' objects at runtime, which the
  checker cannot see.
- Notes: the captured dispatcher must pickle for the message to
  survive a process boundary; as Detached, the dunder reads at :65-66
  are refused (see waitaminute/_detached.py notes).

## waitaminute/dispatch/_duplicate_signature.py : DuplicateSignature (support)

- Item: src/worktoy/waitaminute/dispatch/_duplicate_signature.py, 69
  lines.
- What it is: a second registration under a TypeSig a Dispatcher
  already holds, or a second fallback or finalizer, with the role
  string in place of the signature (:24-28). Based on WorkToyException
  then TypeError (:22).
- Symbols: __slots__ = ('sig', 'existing', 'duplicate') (:41); __init__
  (sig, existing, duplicate) (:43-49); __str__ (:51-67) with one
  wording for a role string and one for a signature; __repr__ =
  __str__.
- Interactions: raised by Dispatcher on registration and by overload
  in a class body; the role strings 'fallback' and 'finalizer' name
  two special registrations the Dispatcher supports.

## waitaminute/dispatch/_type_cast_exception.py : TypeCastException (support)

- Item: src/worktoy/waitaminute/dispatch/_type_cast_exception.py, 46
  lines.
- What it is: raised by utilities.typeCast when a value cannot reach
  the target type without loss. Based on WorkToyException then
  TypeError (:17).
- Symbols: __slots__ = ('type_', 'arg') (:31); __init__(type_, arg)
  (:33-36); __str__ (:38-44) renders "Unable to cast value 'v' to type
  'T'!" with textFmt imported locally (:43), the same leftover pattern
  as ControlClassError; __repr__ = __str__.
- Interactions: the dispatcher's slow path catches it to move on to
  the next candidate signature; confirm in _dispatcher.py.

## utilities/_valid_slice.py : ValidSlice, _MetaSlice (support, read ad hoc from typeCast)

- Item: src/worktoy/utilities/_valid_slice.py, 84 lines.
- What it is: an un-instantiable predicate type. isinstance(s, ValidSlice)
  is True exactly when s is a slice whose start, stop and step are each
  None, an int, or an object whose type has a callable __index__ (not
  invoked) (:19-39, :59-68).
- Symbols: _MetaSlice(type) (:16-55) with __instancecheck__ (:19-39),
  a __call__ that refuses instantiation with a plain TypeError
  (:41-45), __str__ and __repr__ (:47-55); ValidSlice(metaclass=
  _MetaSlice) (:58-84), an empty body.
- Interactions: core's MetaType docstring names _MetaSlice as the one
  metaclass in the library that subclasses type directly, because
  utilities loads before core. typeCast uses it to validate every slice
  it returns.
- Notes: the metaclass is private and single-purpose by design.

## utilities/_type_cast.py : typeCast, castRule and the _cast* helpers (support, read ad hoc from Dispatcher)

- Item: src/worktoy/utilities/_type_cast.py, 397 lines.
- What it is: the library's one conversion routine, lossless by
  contract. An argument already of the target type is returned as is
  (slice excepted, always revalidated); otherwise a per-type rule
  applies, and any failure is TypeCastException (:292-375).
- Symbols:
  - _exc(target, arg), :20-27: builds TypeCastException through a
    deferred import, so utilities does not load waitaminute at import.
  - _castSlice, :30-49: a ValidSlice passes; a lone None is refused
    (:33-39, no single subscript meaning; a class wanting it declares
    @overload(type(None))); a single value is the stop; a list or
    tuple of at most three values are the slice arguments; anything
    else is refused.
  - _castStr, :52-58: only bytes and bytearray, decoded UTF-8; objects
    are never stringified. _castBytes and _castByteArray (:68-81) take
    str (encoded) and each other, never an int or an iterable of ints.
  - _castBool, :84-90: only a Number equal to 0 or 1, so a foreign
    __eq__ is never asked.
  - _castInt, :93-107: integral float, real integral complex, parseable
    str. _castFloat, :110-128: int that round-trips exactly, real
    complex, parseable str. _castComplex, :131-147: int (exact), float,
    parseable str.
  - _castDict, :150-154: anything that splats as {**arg}.
  - _CONTAINERS and _castContainer, :157-176: list, tuple, set,
    frozenset from one another or from a dict's items.
  - _SCALAR_HANDLERS, :179-188: the rule table.
  - _ruledBase, :191-198: the first MRO entry with a rule.
  - _ownsConstructor(target, base), :201-210: whether target resolves a
    __new__ or __init__ other than base's, comparing resolved
    attributes so a constructor inherited from a class between the two
    or from a mixin counts.
  - castRule(target), :213-258: the builtin whose rule applies, or None
    when the target's own constructor is trusted (an IntEnum, a
    Counter, any class based on no ruled builtin). The docstring says
    AttriBox asks this as well, so boxes and dispatch decide alike
    (:227-228).
  - _castRuled, :261-265; _castSubclass(target, base, arg), :268-289:
    arg held to the builtin's rule unless already an instance of it,
    then target(value), which must give an instance of target.
  - typeCast(target, arg, allowInstantiation=True), :292-397: slice
    first; identity passthrough; target 'type' only succeeds by the
    passthrough; ruled builtin; ruled subclass; else the constructor
    fallback when allowed, whose result must be an instance of target.
- Interactions:
  - dispatch: Dispatcher's SLOW passes call it per argument through
    castArg, with allowInstantiation=False for the sole argument of an
    __init__ whose target is the owning class (the recursion guard).
    TypeCastException is a TypeError, which is what the SLOW loops
    catch.
  - desc: AttriBox is named as a caller of castRule (:227-228); expect
    typeCast in its value coercion.
- Support: ValidSlice (:12); TypeCastException by deferred import
  (:26, :276).
- Notes:
  - A bool is an int, so typeCast(int, True) returns True unchanged
    through the passthrough, while typeCast(bool, 1) goes through
    _castBool and gives True.
  - The except at :507 and :582 of the dispatcher also lists
    ValueError, but every failure here is already wrapped as
    TypeCastException; the ValueError is defensive.
  - float('nan') and float('inf') parse and are accepted by _castFloat.

## dispatch/_dispatcher.py : Dispatcher, _uniformType

- Item: src/worktoy/dispatch/_dispatcher.py, 1217 lines. Sixth import of
  dispatch/__init__.py:26. The largest file in the four packages.
- What it is: the descriptor that holds signature-to-function
  registrations for one method name and compiles them into a single
  dispatch function. It is an Object that overrides __get__, __set__
  and __delete__ outright (no context stack, no hooks), using Object
  only for the recorded field name and owner.
- Dispatch design (docstring :51-148): up to five ordered passes,
  returning at the first match: FASTEST (exact concrete types by one
  dict lookup, then exact variadic by prefix and uniform tail),
  FAST-concrete and FAST-variadic (isinstance, registration order),
  SLOW-concrete and SLOW-variadic (typeCast, only where __allow_flex__,
  farthest class first), then the fallback, else DispatchException.
  Keyword calls bind to parameter names of the concrete registrations
  and pick the best type match in three tiers. No specificity ranking:
  first registered wins. BaseSpace in mcls registers the class body's
  own signatures first, then inherited ones nearest first, each with a
  distance.
- Symbols:
  - _uniformType(types), :32-43: the one type every entry is, by
    identity, or None; callers pass non-empty tuples only.
  - Dispatcher(Object), :46. Private slots :155-166: __sig_funcs__,
    __sig_distances__, __variadic_funcs__, __variadic_distances__,
    __fallback_func__, __field_name__, __field_owner__,
    __finalizer_func__, __compiled_func__, __latest_func__.
  - Getters :172-194: the lists with [] fallbacks, a dict view, and
    _getDeclaredSigs (concrete then variadic) used by messages.
  - _coversExactly(sig, types), :196-213: a variadic signature accepts
    'types' by identity of the prefix and of every tail entry.
  - _getExactFuncMap, :215-239: concrete sig to function, except that a
    variadic signature from a strictly nearer class that covers the
    sig's types exactly takes it over; same distance never displaces.
  - _getExactVariadics, :241-274: two tables keyed by (prefix length,
    prefix, inner) and by (prefix length, prefix) for a prefix-only
    call, each entry (rank, func) with rank (distance, -index) so the
    nearest class and then the latest declaration wins; plus the
    distinct prefix lengths ascending.
  - _getCastOrder, :276-307: greatest distance first, stable within a
    distance, indexing rather than zipping so a length mismatch raises.
  - _getVariadicOrder(nearestFirst), :309-323: by signed distance then
    latest declaration first.
  - _getFieldName, _getFieldOwner, :331-372: MissingVariable when
    unplaced.
  - _getKeywordBindings(owner), :374-408: per concrete registration
    with readable __code__: the first len(types) positional names
    after self, the further positional and keyword-only names, whether
    **kwargs is taken (co_flags & 0x08), the types, the target and the
    flex flag. A PermuterMethod registration is listed once under its
    wrapped function with the canonical types from
    arrangement.items, THIS replaced by the owner (:388-391).
  - _createCachedFunction, :410-643: builds the closure. Inner
    helpers: castArg (:426-436, allowInstantiation False when the sole
    argument's target is the owning class of an __init__),
    exactVariadic (:438-455), bindKeywords (:457-479), keywordDispatch
    (:481-511, exact, isinstance, then cast tiers over the bound
    candidates), dispatch (:513-635). dispatch records the in-flight
    exception (:625-627) so a raising finalizer is chained from it
    (:628-635). The FASTEST lookup is guarded for an unhashable argument
    class (:528-535). The compiled function takes the field name,
    'Owner.name' qualname, the owner's module and the docstring of the
    first registered function (:637-643).
  - _getDocumentedFunction, :645-657; _getCachedFunction, :659-665
    (the '_recursion' peek pattern).
  - addSigFunc(sig, func, distance=0), :671-714: resolves THIS when
    already placed, refuses an equal signature with DuplicateSignature,
    appends, invalidates the cache. addVariadicSigFunc, :716-758: the
    same without the duplicate check (latest of nearest wins).
  - _resolveTHIS, :760-769: swapTHIS(owner) when placed.
  - setFallbackFunction, setFinalizerFunction, :771-839: callable
    check (TypeException naming FunctionType and MethodType), second
    registration refused with DuplicateSignature('fallback' or
    'finalizer', ...).
  - __get__(instance, owner), :845-894: _adoptOwner first; class access
    returns the compiled function; instance access returns a fresh
    MethodType every time and stores nothing on the instance (reasons
    at :858-865: a stored bound method would be found by the parent's
    Dispatcher through super, carried by copy.copy still bound, and
    would keep the instance alive).
  - _adoptOwner(owner), :896-911: an unplaced dispatcher installed with
    setattr adopts the class along the MRO that holds it, by identity,
    running __set_name__.
  - __set__ raises ReadOnlyError and __delete__ ProtectedError,
    :913-934.
  - __set_name__(owner, name, **kwargs), :936-939: sets name and owner
    directly (Object.__set_name__ and hookSetName are not used) and
    swapAllTHIS(owner).
  - __str__ and __repr__, :941-953.
  - _copySig(sig), :959-972: a new TypeSig from the declared types,
    with the raw types and the flex flag copied.
  - clone, :974-1010: a new unplaced Dispatcher with copied signatures,
    the same functions, distances, fallback and finalizer.
  - _stackedFunction(func), :1016-1036: each decorator returns the
    dispatcher, so a decorator stacked above another receives the
    dispatcher and registers the function recorded by the one below.
  - overload(*types, strict=None), :1038-1087: validateTypes, then a
    decorator registering a TypeSig, strict defaulting to namesTHIS,
    variadic when the last entry is an ARGS.
  - finalize, fallback, :1089-1136: through _stackedFunction.
  - flex(*types), :1138-1183: validateTypes(variadic=False); one
    concrete signature per Arrangement of the types, flex flag off,
    each wrapping the function in a PermuterMethod with that
    arrangement, registered through addSigFunc.
  - restoreTHIS, swapAllTHIS, :1185-1217: over both lists, cache
    invalidated.
- Interactions:
  - core: Object base (:13); ARGS and THIS (:14); ReadOnlyError and
    ProtectedError from waitaminute.desc for the refusals (:18).
  - dispatch: TypeSig and PermuterMethod (:20); Arrangements for flex
    (:16); typeCast for the SLOW passes (:15).
  - mcls: BaseSpace is the builder (:124-133); it supplies distances
    and is expected to use clone and restoreTHIS when a subclass
    inherits a parent's dispatcher, and __set_name__ fires when the
    class is made, which is when THIS is swapped.
  - desc: none directly; the Dispatcher is the model of an Object
    subclass that opts out of the context protocol.
- Support: utilities maybe, typeCast, textFmt (:15), combinatorics
  Arrangements (:16); waitaminute TypeException, MissingVariable (:17),
  DispatchException, DuplicateSignature (:19).
- Notes:
  - TypeSig.__call__'s docstring (:256-258 there) says _copySig relies
    on a no-argument call copying the signature; _copySig (:969-972)
    builds the copy from getDeclaredTypes and sets the raw types by
    hand instead, which is what keeps the declared sentinel on the
    clone. The TypeSig docstring is stale on that point.
  - The FAST-concrete pass iterates the exact map (:540), so a parent's
    concrete signature whose function was taken over by a nearer
    variadic (exact coverage) dispatches to the variadic's function on
    an isinstance match too; the override is consistent across tiers.
  - Keyword calls never reach the positional tiers, the variadic
    registrations or the SLOW passes beyond the per-candidate cast
    (:519-526), and a flexCall-wrapped function has a (*args, **kwargs)
    code object, so _getKeywordBindings skips it (:397-400). Whether an
    overloaded function can ever be flex-wrapped depends on mcls'
    FlexCallHook ordering; check there.
  - flex registrations go through addSigFunc, so a flex over types that
    an explicit overload already covers in that order raises
    DuplicateSignature.
  - Permuter.__init__ accepts only types.FunctionType, so flex over a
    non-function callable fails inside PermuterMethod construction
    (:1179), not at validation.
  - __field_name__ and __field_owner__ are declared again here
    (:160-161) though Object already has them; harmless shadowing.
  - The compiled closure captures the owner and name at compile time;
    _adoptOwner runs on every __get__ but returns at once once placed.

## dispatch/_overload.py : overload

- Item: src/worktoy/dispatch/_overload.py, 469 lines. Last import of
  dispatch/__init__.py:27.
- What it is: the user-facing decorator. It only records signatures
  against one function; it never dispatches. BaseMeta (mcls) finds the
  overload instances in a class namespace and compiles them into a
  Dispatcher (:27-47). Decorators stacked on one function each add a
  role for that function in any order (:53-62).
- Symbols:
  - Private slots :108-114: __sig_func_dict__,
    __variadic_sig_func_list__, __next_sig__, __next_func__,
    __latest_func__, __fallback_func__, __finalizer_func__.
  - _getSigFuncDict, :120-121; getVariadics, :123-137; _getLatestFunc,
    :139-144 (a plain RuntimeError when nothing is registered);
    isFallback, getFallback, isFinalizer, getFinalizer, :146-162.
  - _addSigFunc(sig, func), :168-195: a signature ending in an ARGS
    instance goes to the variadic list as written; any other goes into
    the concrete dict, where an equal signature stacked again keeps
    its first position but takes the new function; __latest_func__ is
    set to func.
  - _extendLatest(sig), :197-209: another signature for the latest
    function, which is how a stack of @overload lines shares one body.
  - __new__(cls, *types, **kwargs), :215-269: with _root=True it
    returns a bare instance (for _stackOn); otherwise it refuses any
    keyword but strict with the TypeError wording Python uses
    (:384-395), validates the types, and returns a decorator. The
    decorator builds the TypeSig, sets __allow_flex__ from strict
    (default: refuse casts when the signature names THIS), extends an
    overload instance it is stacked on, or refuses a staticmethod,
    classmethod or non-callable (:397-410) and builds a fresh instance
    through object.__new__ and _addSigFunc. Because __new__ returns a
    function rather than an instance, __init__ (:271-272) runs only on
    the _root path and does nothing.
  - flex(*types), :274-322: classmethod; validateTypes(variadic=False);
    the decorator takes the overload and function from _stackOn, adds
    one concrete signature per Arrangement with the flex flag off,
    each over a PermuterMethod(function, arrangement), then resets
    __latest_func__ to the function so a decorator above registers the
    function, not the last wrapper (:317-319).
  - fallback(func), finalize(func), :324-364: classmethods through
    _stackOn setting the role.
  - _stackOn(func), :366-382: an overload from below returns itself and
    its latest function; a function is refused by kind and wrapped in
    a new overload via cls(_root=True).
  - __getattr__(key), :416-428: delegates to the latest function, else
    the fallback, else MissingVariable(self, key) with no type.
  - __iter__, :430-442: the concrete (TypeSig, function) pairs.
  - __call__ exists only under TYPE_CHECKING (:444-446) to tell
    linters the object is not callable; at runtime calling an overload
    instance fails, which is correct since only the Dispatcher calls.
  - __str__ and __repr__, :448-469.
- Interactions:
  - mcls: the consumer. It must read the instance by iteration (concrete
    pairs), getVariadics(), getFallback() and getFinalizer(), pass the
    pairs to a Dispatcher with distances, and clone or restore THIS for
    inherited dispatchers. The same TypeSig objects carry
    __allow_flex__ across.
  - dispatch: Dispatcher.overload, .flex, .fallback and .finalize
    mirror these for by-hand wiring; TypeSig and PermuterMethod are
    shared.
  - core: ARGS (:12) to recognise a variadic tail.
- Support: utilities maybe and textFmt (:13), combinatorics
  Arrangements (:14); waitaminute MissingVariable and TypeException
  (:15).
- Notes:
  - __next_sig__ and __next_func__ (:110-111) are declared and never
    used in this file; leftovers.
  - A concrete signature registered twice on one overload is silently
    merged by the dict (:192-194), so DuplicateSignature from the
    Dispatcher can only arise from two different overload objects or
    an explicit overload beside a flex with the same order.
  - The 'overload' name is lowercase by design (NOQA at :26), so it
    reads as a decorator.

## dispatch package summary

- Items read, in order: flexCall and isFlex, CallMeMaybe, Permuter,
  PermuterMethod, TypeSig, Dispatcher, overload; support read ad hoc:
  joinWords, unpack, UnpackException, QuickDesc, WriteOnceError, the
  combinatorics subpackage, ValidSlice, typeCast, and the three
  waitaminute.dispatch exceptions.
- The spine: overload records (TypeSig, function) pairs plus roles;
  Dispatcher compiles them into one closure with FASTEST, FAST, SLOW
  tiers and keyword binding, resolving THIS when placed; flex expands
  a signature into every Arrangement with a PermuterMethod restoring
  canonical order; typeCast is the lossless cast of the SLOW tier;
  flexCall is unrelated to overloads and serves callbacks.
- Threads for mcls: who builds the Dispatcher from overload instances
  (BaseSpace), how distances are assigned, whether overloaded
  functions can be flexCall-wrapped by FlexCallHook, and who reads
  __skip_hash__ and cls.__namespace__ (still unseen).

# Package: desc

Import order from desc/__init__.py:36-43: _RootAlias (private, first
because FastBox and AttriBox need it), FastBox, BaseDescriptor, Alias,
Field, AttriBox, FixBox, SymbolicName. The package docstring (:2-17)
restates the descriptor-context idea from core.Object and adds the
pickling contract: a placed box pickles by reference to the box its
owner declares, so an object whose fields a box created keeps naming
that box after a round trip, and copying a box gives the box itself
(AttriBox.__reduce__ and __deepcopy__); FastBox creates no tags and
follows the default protocol.

## desc/_root_alias.py : _RootAlias

- Item: src/worktoy/desc/_root_alias.py, 109 lines. First import of
  desc/__init__.py:36, private, listed in the docstring's private group.
- What it is: a subclass of typing._GenericAlias (declared with
  _root=True, which typing's _Final.__init_subclass__ demands of any
  subclass of its special classes) that a box subscript returns for
  anything but a plain class: a TypeVar, as in class Sub(AttriBox[T]),
  or a parametrized generic such as list[int] (:20-31). The plain alias
  typing returns has no __get__, so a class body that stores
  'x = AttriBox[list[int]]' without the trailing call would hold an
  alias that reads back silently; re-clothing it gives the stored
  object a type with __set_name__ and __get__.
- Symbols:
  - fromAlias(alias), :33-59: rebuilds the alias as this class from
    its origin, args, _name and _inst; copy_with cannot be used for
    that because it builds self.__class__ and self is the plain alias
    (:41-44).
  - copy_with(args), :61-82: keeps this class through typing's internal
    copies (TypeVar substitution); snake_case because it overrides a
    CPython internal (:68-69).
  - __set_name__(owner, name), :84-100: raises PhantomBoxError(self,
    owner, name) as the class is created; 3.7 through 3.11 wrap that
    in a RuntimeError with the original as __cause__ (:96-98).
  - __get__(instance, owner=None), :102-109: raises PhantomBoxError
    (self, owner) for an alias installed by setattr after the fact.
- Interactions: FastBox.__class_getitem__ and AttriBox's are the two
  producers (desc/_fast_box.py:126). A base-class entry such as
  AttriBox[T] in a class statement never reaches __set_name__, so the
  legitimate generic-subclass use keeps working (:88-90). Nothing in
  core, dispatch or mcls touches it.
- Support: waitaminute.desc.PhantomBoxError (:13), read next.
- Notes: the constructor keywords passed (name, inst) are the two that
  exist on every supported typing version; the class relies on private
  typing internals (_GenericAlias, _name, _inst) by design.

## desc/_fast_box.py : FastBox

- Item: src/worktoy/desc/_fast_box.py, 281 lines. Second import of
  desc/__init__.py:37.
- What it is: the lean type-enforced attribute descriptor. It is a
  plain Generic[T] class, not an Object: no context stack, no hooks, no
  sentinel resolution, no cast on write. The value lives in the owning
  instance's __dict__ under '__fast_<name>__' (:159), so a read is one
  dict lookup and a write one isinstance check plus a store (:32-36).
- Symbols:
  - _CONTAINERS, _TEXT_TYPES, _NUMBER_TYPES, :22-24, the same groups
    AttriBox names.
  - Class defaults :65-69: __field_type__, __field_name__,
    __private_name__, __default_args__ = (), __default_kwargs__.
  - __class_getitem__(fieldType), :84-126: a plain class (its type is a
    metaclass, the version-proof test explained at :111-115) yields a
    fresh instance carrying the field type; anything else is handed to
    Generic's __class_getitem__ and the result re-clothed as _RootAlias;
    a failure there raises TypeException('fieldType', ..., type,
    TypeVar). So FastBox[int] is an instance, and FastBox[int](42) is a
    call on it.
  - __call__(*args, **kwargs), :128-142: captures the default
    arguments and returns self for the class-body assignment.
  - __set_name__(owner, name), :148-159: a box with no field type
    (FastBox() or the alias route) raises MissingVariable; records the
    name and the private name.
  - __get__, :161-170: class access returns self; instance access reads
    the dict or builds, stores and returns the default on a KeyError.
  - __set__, :172-179: isinstance or TypeException(fieldName, value,
    fieldType); no numeric tower, so a float field refuses an int.
  - __delete__, :181-187: removes the dict entry; a missing entry is
    MissingVariable(instance, fieldName) chained from the KeyError. The
    next read builds a fresh default, unlike the other boxes which
    raise after deletion (:54-57).
  - _build, :193-233: MissingVariable without a field type; with one
    positional argument and no keywords, a container field type
    refuses a text argument rather than splitting it, and a number
    field type (castRule in _NUMBER_TYPES, so a subclass keeping the
    builtin constructor counts) casts it through typeCast; otherwise
    _callFieldType, whose result must be an instance of the field type.
  - _callFieldType, :235-259: fieldType(*args, **kwargs); a TypeError
    from a builtin container with no keywords gets one more try as
    fieldType(args), so FastBox[tuple](1, 2) holds (1, 2); refusals
    become _refusal (:261-268), a TypeException naming the field.
  - _castNumber, :270-281: typeCast, TypeCastException rewritten as
    TypeException naming the field.
- Interactions:
  - core: none; FastBox is outside the Object protocol and outside
    MetaType.
  - dispatch: shares typeCast and castRule, so a FastBox number default
    and the SLOW dispatch tier decide a cast the same way.
  - desc: the four default-building rules are stated to be AttriBox's
    (:45-47, :196-203); AttriBox is expected to differ by adding
    context, hooks, sentinels and set-time coercion. The desc docstring
    says FastBox creates no tags and pickles by the default protocol.
  - mcls: the owning instance must have a __dict__ (:52); a slots-only
    BaseObject could not hold one.
- Support: _RootAlias (:11); utilities typeCast and castRule (:12);
  waitaminute TypeException and MissingVariable (:13);
  waitaminute.dispatch.TypeCastException (:14).
- Notes:
  - A bool passes the isinstance check of an int field, as it does
    everywhere isinstance is used.
  - The 'in _CONTAINERS' tests use identity, so a subclass of list does
    not get the second constructor call.
  - Re-entrant access is safe because __get__ reads its instance
    parameter rather than shared state (:49-52), the design argument
    Object's context stack exists to make for the other boxes.

## waitaminute/desc/_phantom_box_error.py : PhantomBoxError (support, read ad hoc from _RootAlias)

- Item: src/worktoy/waitaminute/desc/_phantom_box_error.py, 108 lines.
- What it is: the refusal of a class-body attribute that holds a typing
  alias where a box was meant, 'x = AttriBox[list[int]]' without the
  trailing call. Based on DescriptorException alone (:18), not an
  AttributeError. The docstring (:23-36) explains why the subscript
  itself cannot be refused: class Sub(AttriBox[T]) legitimately wants
  the alias, and only the alias landing in a class body settles it.
- Symbols: __slots__ = ('alias', 'owner', 'fieldName') (:51); __init__
  (alias, owner=None, fieldName=None) (:53-62); _getBoxName from the
  alias's __origin__ (:64-67); _renderArg (:69-83) renders a plain
  class by bare name and anything else by typing's str, sorting by
  __origin__ rather than isinstance(arg, type) for the 3.9 and 3.10
  reason; _getSubscript (:85-89); __str__ (:91-106) names the
  declaration, the class when known, and the completed form to write,
  with the article chosen by the box name's first letter.
- Interactions: raised by _RootAlias.__set_name__ with owner and name
  and by _RootAlias.__get__ with owner alone (desc/_root_alias.py:100,
  :109). On 3.7 through 3.11 the __set_name__ raise reaches the user
  wrapped in RuntimeError.
- Support: utilities.textFmt (:12).

## desc/_base_descriptor.py : BaseDescriptor

- Item: src/worktoy/desc/_base_descriptor.py, 315 lines. Third import
  of desc/__init__.py:38.
- What it is: Object plus decorators that register access-notification
  callbacks by name. Each decorator (preGet, onGet, preSet, onSet,
  preDelete, onDelete, setName) records the callback's __name__ in
  registration order and returns the callback wrapped by flexCall; the
  Object hooks then look each name up on type(instance) at access time,
  so a subclass override is used, and call it with the instance first
  (:25-45). It changes nothing of the descriptor protocol itself: the
  Object defaults (return self, ReadOnlyError, ProtectedError) stand
  (:98-102), and subclasses implement the three __instance_* methods
  (:104-115).
- Symbols:
  - BaseDescriptor(Object, Generic[T]), :24. With Generic resolved into
    the bases, MetaType appends _Chill, giving the MRO BaseDescriptor,
    Object, Generic, _Chill, object; Generic.__init_subclass__ runs for
    every subclass and its super() call lands in _Chill, which absorbs
    any class keyword (derived from the MRO, not executed).
  - Seven key tuples :127-133 with getters :145-164.
  - _getCallbackName(role, callback), :170-181: the callback's __name__,
    NamelessCallback(self, role, callback) for a lambda or a callable
    without one.
  - The seven decorators, :183-223: append the name, return
    flexCall(callback). flexCall refuses anything but a plain function,
    so the setName example puts @classmethod above @bar.setName
    (:89-91).
  - _getCallback(owner, key), :229-240: getattr(owner, key), a bound
    method (a classmethod) unwrapped through __func__, then flexCall,
    which is a no-op on an already wrapped function and wraps an
    undecorated override on every call.
  - hookPreGet, hookOnGet, hookPreSet, hookOnSet, hookPreDelete,
    hookOnDelete, :242-288: for each key, the callback found on
    type(instance) called with the instance, the value where there is
    one, and the keywords; nothing happens when no key is registered.
  - hookSetName(owner, name, **kwargs), :290-294: each callback read
    off the owner, unwrapped through __func__, called as callback(owner,
    self, **kwargs); flexCall is not applied here.
  - TYPE_CHECKING-only __get__ overloads and a __set__ stub (:300-315)
    for checkers.
- Interactions:
  - core: the Object hooks are the extension points this fills; the
    context stack and DELETED translation stay Object's.
  - dispatch: flexCall (:13) is the first desc-to-dispatch dependency;
    it is why a callback may declare fewer parameters than the hook
    passes.
  - desc: Field, AttriBox and FixBox are expected to be based on it;
    the callbacks are a per-descriptor feature declared in the owner's
    class body, the pattern the docstring example shows (:50-96).
  - mcls: an owner must expose the callback names as attributes, which
    any class body gives; FlexCallHook would wrap the same functions
    again harmlessly since flexCall is idempotent.
- Support: utilities.maybe (:11); core.Object (:12); dispatch.flexCall
  (:13); waitaminute.desc.NamelessCallback (:14), read next.
- Notes:
  - A name registered twice fires twice (:31-32), and the lookup is by
    name on the instance's class, so a subclass that defines a method
    of the same name silently replaces the parent's callback.
  - hookSetName skips flexCall while the six access hooks apply it, so
    an undecorated setName override must take exactly (cls, desc)
    while an undecorated access override may take fewer arguments.
  - hookPreSet raising SkipSet from a registered preSet callback is the
    sanctioned redundant-set elision route through Object.__set__.

## desc/_alias.py : Alias

- Item: src/worktoy/desc/_alias.py, 130 lines. Fourth import of
  desc/__init__.py:39.
- What it is: a descriptor that re-exposes another attribute, usually
  inherited, under a second name (:19-27). It is an Object that
  overrides __get__, __set__ and __delete__ outright, as Object's
  docstring says, using Object only for the recorded name and owner.
- Symbols:
  - __real_name__ = None (:63); __init__(realName) (:128-130) captures
    the argument through Object.__init__ and records it.
  - _getRealObject(owner), :69-84: the first entry under the real name
    in the __dict__ of the classes along owner.__mro__, before the
    descriptor protocol applies (so a staticmethod stays one and a
    classmethod binds at read time), else getattr(owner, realName) for
    a metaclass-supplied name, which raises AttributeError when nothing
    supplies it.
  - __set_name__(owner, name), :90-101: when the real object already
    resolves, setattr(owner, name, realObject) replaces the alias in
    the class by the real object, so later access needs no
    indirection; otherwise the alias stays and forwards. Either way
    Object.__set_name__ records owner and name.
  - __get__, :103-108: the real object's type's __get__ if it has one,
    else the plain value.
  - __set__, :110-115 and __delete__, :117-122: forwarded to the real
    object's type's __set__ or __delete__, or ReadOnlyError and
    ProtectedError when the target is no descriptor.
- Interactions:
  - core: Object base; the setattr at :100 goes through the owner's
    metaclass __setattr__, so whatever AbstractMetaclass does on
    attribute assignment applies to this replacement; check in mcls.
    The replacement does not call __set_name__ on the real object, so
    the target keeps its own field name.
  - desc: the usual target is an AttriBox of a parent class; the
    forwarded __set__ passes type(instance) as the owner, matching
    Object.__set__'s own choice.
  - mcls: whether the namespace hooks see the alias or the replaced
    real object depends on when __set_name__ fires relative to the
    hooks; check in mcls.
- Support: core.Object (:10); waitaminute.desc ProtectedError and
  ReadOnlyError (:11).
- Notes: __get__ reads the real object through owner, which for an
  instance access is the class Python passes, while __set__ and
  __delete__ use type(instance); a subclass holding its own entry
  under the real name therefore wins in both cases.

## waitaminute/desc/_nameless_callback.py : NamelessCallback (support, read ad hoc from BaseDescriptor)

- Item: src/worktoy/waitaminute/desc/_nameless_callback.py, 62 lines.
- What it is: the refusal of a lambda or a __name__-less callable by a
  callback decorator of BaseDescriptor or an accessor decorator of
  Field, since callbacks are stored by name and looked up on the class
  of the instance (:20-30). Based on WorkToyException then SyntaxError
  (:18), like the other refusals of a class-body line.
- Symbols: __slots__ = ('desc', 'role', 'callback') (:42); __init__
  (desc, role, callback) (:44-50) calls SyntaxError.__init__ with
  nothing and then sets self.msg = str(self) because a SyntaxError
  traceback shows msg rather than str (:49-50); __str__ (:52-60) names
  the role, the descriptor class and the callback.
- Interactions: raised by BaseDescriptor._getCallbackName
  (desc/_base_descriptor.py:180), which Field's GET, SET and DELETE
  also use.
- Support: utilities.textFmt (:11).

## desc/_field.py : Field

- Item: src/worktoy/desc/_field.py, 273 lines. Fifth import of
  desc/__init__.py:40.
- What it is: the property-like descriptor whose accessors are methods
  decorated below it in the class body with @GET, @SET and @DELETE.
  Accessors are stored by name and looked up on the type of the
  instance at access time, so a subclass overrides one by redefining a
  method of the same name without decorating again (:54-70); the
  samplers in work_test rely on this.
- Symbols:
  - __get_key__, __set_keys__, __delete_keys__ (:79-81).
  - _getGetterKey, :87-92: AccessError(self) when no getter was
    registered; _getSetterKeys and _getDeleterKeys, :94-98.
  - GET, :104-122: records one name through _getCallbackName (so a
    lambda raises NamelessCallback) and returns the method unchanged;
    a second @GET replaces the first. SET, :124-145, and DELETE,
    :147-168: append names, return the method unchanged. None of the
    three wraps with flexCall, unlike BaseDescriptor's notification
    decorators.
  - __instance_get__(instance, owner, **kwargs), :174-193: with
    _deleting=True answers _peekValue; otherwise getattr(owner, key)
    (instance).
  - _peekValue, :195-211: the getter's answer, or None when there is no
    getter or it raises, so a deletion is never stopped by the read;
    DELETED from a getter makes Object.__delete__ raise MissingVariable
    on a second deletion.
  - __instance_set__, :213-226: ReadOnlyError without setters; each
    setter called as method(instance, value) on type(instance), in
    order; returns None, so hookOnSet receives the assigned value.
  - __instance_delete__(instance, old=None, **kwargs), :228-247:
    ProtectedError(instance, self, old) without deleters; each deleter
    called as method(instance, **kwargs).
  - __init__(other=None), :253-273: Object.__init__ captures 'other';
    a Field passed as other has its getter key and all nine key groups
    copied (tuples), so Field(parentField) clones the registrations;
    anything else raises TypeException.
- Interactions:
  - core: everything runs inside Object's context frames, and the
    DELETED translation applies to a getter answering DELETED.
  - desc: AttriBox declares 'fieldType: Field[type] = Field()' with
    @fieldType.GET on its getFieldType (desc/_attri_box.py:170-180),
    the Field[int] = Field() annotation style the author prefers.
    BaseDescriptor's notification hooks fire around the accessors.
  - mcls: accessor names must be attributes of the owner, which a
    class body gives; no further contact.
- Support: BaseDescriptor (:11); utilities.maybe (:12); waitaminute
  TypeException (:13); waitaminute.desc ProtectedError, ReadOnlyError,
  AccessError (:14). AccessError is read next.
- Notes:
  - The getter is read through the owner parameter of __get__, which
    is the class Python passed, while setters and deleters use
    type(instance); the two differ only for a super() or
    class-dict-mediated access.
  - A Field with no accessors is the read-only class attribute
    Object's docstring describes, except that a read raises
    AccessError rather than returning the descriptor.

## desc/_attri_box.py : AttriBox

- Item: src/worktoy/desc/_attri_box.py, 880 lines. Sixth import of
  desc/__init__.py:41. The central descriptor of the library.
- What it is: the lazily built, strongly typed attribute. The subscript
  fixes the field type, the call captures the deferred default through
  Object.__init__, the first read on an instance builds T(*args,
  **kwargs) with THIS, OWNER and DESC substituted, caches it in the
  instance dict under a storage name, and later assignments are
  coerced losslessly or built through the constructor (:41-160).
- Symbols:
  - _CONTAINERS, _TEXT_TYPES, _NUMBER_TYPES, :32-37, as in FastBox.
  - __field_type__ = None (:167); fieldType: Field[type] = Field()
    (:170) read through getFieldType (:176-180), which raises
    MissingVariable when no type was captured.
  - _getStorageName, :186-201: getPrivateName() plus the lower-cased
    box class name plus '_field_object__', so 'fooBar' on an AttriBox
    stores at '__foo_bar__attribox_field_object__' and a FixBox of the
    same name elsewhere.
  - _resolve(*args, **kwargs), :203-372: a lone argument already of the
    field type, with no keywords and no sentinel among the captured
    arguments, is deep-copied so each instance owns its default (an
    uncopyable value is shared rather than refused), the accepted use
    of deepcopy in the library; otherwise a text field's single
    argument goes to resolveText, a number field's to resolveNumber,
    everything else to _callFieldType; the result must be an instance
    of the field type; then _applyTags. The docstring (:235-317) fixes
    the tuple-splat convention: an assigned tuple is the argument list
    (value constructors), except for the five builtin containers which
    take it whole, and a captured default is never splatted, so
    AttriBox[T]((a, b)) builds T((a, b)) while 'obj.attr = (a, b)'
    builds T(a, b).
  - _isTextField, _isNumberField (by castRule), _isLoneNumber,
    :374-404.
  - resolveNumber(value), :406-455: typeCast; an OverflowError cause is
    re-raised as itself; any other refusal is TypeException naming the
    field, chained. Meant to be replaced by subclasses.
  - resolveText(value), :457-498: typeCast, TypeException chained;
    replaceable as well.
  - _callFieldType, :500-522: a builtin container with no keywords
    refuses a lone text argument, takes a lone argument whole and
    several as its elements; everything else is fieldType(*args,
    **kwargs); TypeError and ValueError become TypeException named
    'value', chained.
  - _assignedArgs(value), :524-537: a tuple becomes the argument list
    with filterSentinels applied per element, wrapped whole for a
    container field type; anything else is a one-element list after
    filterSentinels.
  - _applyTags(fieldObject, *args), :539-579: writes __field_name__,
    __field_owner__ and __field_box__ with object.__setattr__ onto an
    object this box created, skipping one of the build arguments
    (identity), a class, an instance of a class with __no_box_tag__
    true, an Enum member, and anything without an instance dict. The
    tags mean created-by, not held-by, and worQt reads them.
  - _store(instance, value), :581-595: object.__setattr__ under the
    storage name; an AttributeError becomes MissingInstanceDict
    (instance, fieldName).
  - _refuseStorageCollision(owner), :597-615: StorageCollision when
    another AttriBox in owner.__dict__ that already has a name derives
    the same storage name, so the later of 'fooBar' and 'foo_bar' is
    refused as the class is created.
  - __instance_get__, :617-641: object.__getattribute__ under the
    storage name (not getattr, so an owner's __getattr__ cannot
    answer); on a miss, _deleting=True re-raises the AttributeError,
    otherwise the default is built from getPosArgs() and getKeyArgs()
    (sentinels resolved against the current frame), stored, and the
    read repeated once with _recursion=True.
  - __instance_set__, :643-681: an instance of the field type is
    stored and returned; a text field goes through _resolve of the
    assigned arguments; otherwise typeCast with allowInstantiation
    False, an OverflowError cause re-raised as itself, a number field
    refusing a non-tuple with TypeException (no constructor fallback),
    anything else built by _resolve with the build's exception chained
    from the cast's; every branch ends in a recursive store with
    _recursion=True, so hookOnSet receives the value as stored.
  - __instance_delete__, :683-689: stores DELETED.
  - __get__, :695-714: an instance read on a box with no field type
    (installed by setattr) raises MissingVariable at the access;
    otherwise Object.__get__.
  - __copy__ and __deepcopy__, :716-751: the box itself, so a copy of a
    tagged object or of an owning instance keeps naming the box
    declared on the class; FixBox, Kee and KeeBox inherit this.
  - __reduce__, :753-767: a placed box pickles as getattr(owner, name),
    which class-level access answers with the box; an unplaced one by
    the spelled-out default protocol.
  - __class_getitem__, :769-812: a plain class gives object.__new__(cls)
    with the field type, so FixBox[int] is a FixBox; anything else goes
    to the generic machinery and comes back as _RootAlias.
  - __call__, :814-843: refused with TypeError once the box is placed
    (the call would replace every unread instance's default);
    otherwise Object.__init__ captures the arguments and self returns.
  - __set_name__, :845-880: no field type is refused with
    MissingVariable; a subscript never called gets an empty capture
    (BaseDescriptor.__init__); then Object.__set_name__ (records and
    fires hookSetName); then _refuseStorageCollision.
- Interactions:
  - core: THIS, OWNER and DESC resolve through Object.getPosArgs,
    getKeyArgs and filterSentinels against the frame Object.__get__ or
    __set__ pushed; hasSentinelArgs decides the deepcopy; DELETED marks
    deletion and _deletedGuard turns it into MissingVariable;
    getPrivateName supplies the storage prefix.
  - dispatch and utilities: typeCast and castRule are shared with the
    SLOW dispatch tier, so a box and an overload coerce alike;
    TypeCastException is caught here.
  - desc: based on BaseDescriptor (hooks), declares a Field, produces
    _RootAlias, parent of FixBox.
  - mcls: BaseObject instances must have a __dict__ (MissingInstanceDict
    otherwise); the box tags are read by worQt; __no_box_tag__ is how
    keenum members opt out; the pickle-by-reference needs class-level
    getattr on the owner to return the box, so the metaclass must not
    intercept that.
- Support: copyreg, deepcopy, Enum (:8-10); _RootAlias, Field,
  BaseDescriptor (:13); core.Object (:14); DELETED (:15); utilities
  typeCast, castRule, textFmt (:16); waitaminute TypeException,
  MissingVariable (:17); waitaminute.desc MissingInstanceDict,
  StorageCollision (:18); TypeCastException (:19). The two desc
  exceptions are read next.
- Notes:
  - _refuseStorageCollision inspects owner.__dict__ alone, so a
    subclass declaring 'foo_bar' while a parent declares 'fooBar' is
    not refused and both boxes store at the same name on a subclass
    instance (derived, not executed).
  - Deleting a never-read field stores DELETED without complaint
    (Object.__delete__ turns the _deleting AttributeError into
    old=None), while FastBox raises MissingVariable for the same act.
  - _callFieldType names its TypeException 'value' while _resolve and
    the resolve* methods name the field; the same refusal reads
    differently depending on the branch.
  - __instance_set__ substitutes sentinels in assigned values too, so
    'obj.attr = THIS' resolves to the instance of the __set__ frame.
  - The __call__ refusal after placement means a box read through its
    class cannot be re-armed; the earlier silent replacement is what it
    prevents (:825-828).

## waitaminute/desc/_access_error.py : AccessError (support, read ad hoc from Field)

- Item: src/worktoy/waitaminute/desc/_access_error.py, 41 lines.
- What it is: a descriptor with no way to produce a value, the Field
  with no @GET being the named case (:14-17). Based on
  DescriptorException then AttributeError (:12).
- Symbols: __slots__ = ('desc',) (:25); __init__(desc) (:27-29);
  __str__ (:31-39) names the descriptor type and 'Owner.field' from
  __field_owner__ and __field_name__ with 'object' fallbacks.
- Interactions: raised by Field._getGetterKey (desc/_field.py:89), so
  reading such a Field through an instance is an AttributeError to
  hasattr, while Field._peekValue swallows it during a deletion.
- Support: utilities.textFmt (:9).

## waitaminute/desc/_missing_instance_dict.py : MissingInstanceDict (support, read ad hoc from AttriBox._store)

- Item: src/worktoy/waitaminute/desc/_missing_instance_dict.py, 55 lines.
- What it is: a box that must store on an instance with no __dict__ (a
  class declaring __slots__ without one). Based on WorkToyException then
  TypeError (:18), because the owner is of a kind the box cannot serve;
  the bare AttributeError it replaced read as 'attribute absent' to
  hasattr (:23-27).
- Symbols: __slots__ = ('instance', 'ownerName', 'fieldName') (:39);
  __init__(instance, fieldName) (:41-45); __str__ (:47-53) tells the
  user to add __dict__ to the slots or hold the value in a slot.
- Interactions: raised by AttriBox._store (desc/_attri_box.py:591-595)
  for AttriBox and every class based on it; FastBox lets the
  AttributeError escape instead. A slots-only BaseObject in mcls would
  meet it at the first field access.
- Support: utilities.textFmt (:11).

## waitaminute/desc/_storage_collision.py : StorageCollision (support, read ad hoc from AttriBox)

- Item: src/worktoy/waitaminute/desc/_storage_collision.py, 67 lines.
- What it is: two boxes of one class body whose names derive one
  storage name ('fooBar' and 'foo_bar', 'X' and 'x'); the second is
  refused as the class is created (:15-24). Based on WorkToyException
  then SyntaxError (:13), with msg set from str (:52-53).
- Symbols: __slots__ = ('ownerName', 'fieldName', 'existingName',
  'storageName') (:38); __init__(owner, fieldName, existingName,
  storageName) (:40-53); __str__ (:55-65).
- Interactions: raised by AttriBox._refuseStorageCollision
  (desc/_attri_box.py:615) from __set_name__, so on 3.7 through 3.11
  it reaches the user wrapped in RuntimeError. The check covers one
  class body only (see the AttriBox notes).
- Support: utilities.textFmt (:9).

## desc/_fix_box.py : FixBox

- Item: src/worktoy/desc/_fix_box.py, 61 lines. Seventh import of
  desc/__init__.py:42.
- What it is: the write-once AttriBox: a second store raises
  WriteOnceError and deletion raises ProtectedError (:22-24). The
  single write is whatever stores the value, so a lazily built default
  on first read consumes it, and a field meant to be assigned at runtime
  must be written before it is read (:26-31).
- Symbols:
  - FixBox(AttriBox[T]), :20. AttriBox[T] with a TypeVar goes through
    AttriBox.__class_getitem__ to the generic machinery and comes back
    as a _RootAlias, whose __mro_entries__ turns the base list into
    (AttriBox, Generic); MetaType then appends _Chill. This is the
    legitimate generic-subclass use the _RootAlias docstring defends,
    and it never reaches __set_name__.
  - __instance_set__, :38-53: an existing storage entry, detected by
    the absence of AttributeError so an explicit None counts, raises
    WriteOnceError(self, oldValue, value); otherwise
    AttriBox.__instance_set__, whose recursive stores pass through this
    method again while the slot is still empty.
  - __instance_delete__, :55-61: Object.__instance_delete__, which
    raises ProtectedError.
- Interactions: the storage name carries 'fixbox', so a FixBox and an
  AttriBox of one name never share a slot; __copy__, __deepcopy__ and
  __reduce__ are inherited, as AttriBox's docstring says.
- Support: core.Object (:10); waitaminute.desc.WriteOnceError (:11);
  AttriBox (:12).
- Notes: WriteOnceError's message reads __field_owner__ and
  __field_name__ off the box, which a placed FixBox has, so unlike the
  Permuter case the message names the field.

## desc/_symbolic_name.py : SymbolicName

- Item: src/worktoy/desc/_symbolic_name.py, 179 lines. Last import of
  desc/__init__.py:43.
- What it is: an immutable array of words rendered as snake_case,
  SCREAMING_SNAKE_CASE, kebab-case, SCREAMING-KEBAB-CASE, PascalCase and
  camelCase (:25-39). Two names of the same words compare equal and
  hash alike ignoring case; order counts (:41-46).
- Symbols:
  - SymbolicName(Object), :23; __part_words__ (:58); seven Fields,
    words plus the six renderings (:61-69), each with a @GET getter
    (:75-108); _getCamel builds the rest through a fresh instance's
    pascal (:93-100); the screaming forms use str.upper in the unbound
    form the author reserves for such calls (:104, :108).
  - __init__(*words), :114-118: every word must be a str
    (TypeException); Object.__init__ is not called, so the captured
    call stays the class default and createContext tolerates it.
  - __bool__, __len__, __iter__, :124-131; __getitem__ (:144-149) with
    _resolveIndex (:133-139, negative indices, IndexError) and
    _resolveSlice (:141-142), TypeException otherwise; __str__ and
    __repr__ (:151-161); __contains__ (:163-164); _getKey (:166-171)
    lower-cases the words; __eq__ (:173-176) NotImplemented for
    anything else; __hash__ (:178-179).
- Interactions:
  - core: as an Object it is a data descriptor, so a SymbolicName in a
    class body is the shared read-only class attribute of Object's
    docstring (reads give the object, instance writes raise
    ReadOnlyError). Its own Fields run inside Object context frames on
    the class-level Field objects.
  - desc: a consumer of Field only. No contact with boxes.
  - mcls, dispatch: none seen. The rendering set matches the names a
    code generator or a Qt binding would need, which fits the author's
    stated cross-language direction.
- Support: core.Object (:10); utilities.textFmt (:11); waitaminute
  MissingVariable and TypeException (:12); Field (:13).
- Notes: every rendering reads self.words, which raises
  MissingVariable only when __init__ never ran; the empty name is a
  valid value rendering as ''.

## desc package summary

- Items read, in order: _RootAlias, FastBox, BaseDescriptor, Alias,
  Field, AttriBox, FixBox, SymbolicName; support read ad hoc:
  PhantomBoxError, NamelessCallback, AccessError, MissingInstanceDict,
  StorageCollision (WriteOnceError earlier).
- The spine: BaseDescriptor adds name-registered callbacks over Object
  and wraps them with flexCall; Field is accessor-by-name; AttriBox is
  the deferred, typed, sentinel-aware, tagged box with lossless
  coercion shared with dispatch through typeCast and castRule; FixBox
  is its write-once form; FastBox is the lean cousin outside the
  Object protocol; Alias forwards or replaces itself; _RootAlias closes
  the alias-in-class-body hole; SymbolicName is a value object that
  happens to be an Object.
- Threads for mcls: BaseObject must give instances a __dict__;
  whether the metaclass intercepts class-level getattr (pickling by
  reference) and setattr (Alias replacement); where hooks see
  overload, AttriBox and Field objects in the namespace; who reads
  __skip_hash__ and cls.__namespace__.

# Package: mcls

Import order from mcls/__init__.py:38-43: space_hooks (public
subpackage, first), AbstractNamespace, AbstractMetaclass, BaseSpace,
BaseMeta, BaseObject. The package docstring (:2-25) states the pattern:
the metaclass returns a namespace object from __prepare__, the class
body fills it, __new__ asks it to compile() into a plain dict for
type.__new__, per-name validation happens during the body through the
namespace hooks, each base's __subclasshook__ is called with the new
class and may only reject it by raising, and abc.ABCMeta bases cannot be
combined since ABCMeta is outside the MetaType family.

# mcls/space_hooks subpackage

Import order from mcls/space_hooks/__init__.py:22-28: SpaceDesc,
ReservedNames, AbstractSpaceHook, FlexCallHook, ReservedNamespaceHook,
NamespaceHook, LoadSpaceHook. The docstring (:2-8) names the six phases
(prepare, set-item, get-item, pre-compile, post-compile, new-class) and
says LoadSpaceHook is where stacked overload declarations become
Dispatcher objects.

## mcls/space_hooks/_space_desc.py : SpaceDesc

- Item: src/worktoy/mcls/space_hooks/_space_desc.py, 41 lines.
- What it is: a Generic non-data descriptor (only __get__) that, read
  on a hook instance, answers the hook's __space_object__, the
  namespace currently bound to it; on the class it answers itself
  (:33-41).
- Interactions: AbstractSpaceHook declares 'space = SpaceDesc()' so a
  hook's phase methods reach the active namespace as self.space. No
  worktoy imports; the hook type appears only under TYPE_CHECKING.

## mcls/space_hooks/_reserved_names.py : ReservedNames

- Item: src/worktoy/mcls/space_hooks/_reserved_names.py, 48 lines.
- What it is: a descriptor whose instance read is the tuple of names
  the interpreter sets in a class body on its own (:33-48): __dict__,
  __weakref__, __module__, __annotations__, __match_args__, __doc__,
  __name__, __qualname__, __firstlineno__, __static_attributes__,
  __classcell__, __classdictcell__, __orig_bases__, __type_params__.
- Interactions: the list a namespace hook consults to let those names
  through; compare ControlSpace.__white_list__ in core, which is the
  narrower hand-written version of the same idea. Note that
  __annotations__ appears here, so the eager annotations dict of a
  class body is expected to pass whatever hook uses this list.

## mcls/space_hooks/_abstract_space_hook.py : AbstractSpaceHook

- Item: src/worktoy/mcls/space_hooks/_abstract_space_hook.py, 190
  lines. Third import of the subpackage.
- What it is: the base of every namespace hook. A hook is instantiated
  in the body of a namespace class; its __set_name__ registers it with
  that class through addHook; the namespace then calls the hook's
  phase methods during the class body and compilation (:34-98).
- Symbols:
  - AbstractSpaceHook(Object), :27; __space_object__ = None (:106);
    space = SpaceDesc() (:109).
  - preparePhase(space), :115-120: during the namespace's __init__; no
    changes allowed; raise to interrupt.
  - getItemPhase(key, value), :122-128: after a read, return ignored;
    can only raise.
  - setItemPhase(key, val, old=None) -> bool, :130-136: before a bind;
    True blocks the namespace's own assignment.
  - preCompilePhase(compiledSpace) -> dict, :138-144 and
    postCompilePhase, :146-152: during compile(), before and after the
    class-body names are merged; must return the dict.
  - newClassPhase(cls) -> cls, :154-161: after the metaclass created
    the class, before it is returned.
  - __set_name__(owner, name, **kwargs), :167-177: Object's
    registration (the keywords are dropped), then owner.addHook(self).
  - __get__(instance, owner, **kwargs), :179-190: class access gives
    the hook; namespace-instance access rebinds __space_object__ to
    that namespace and gives the hook. __set__ and __delete__ are
    inherited from Object and so refuse.
- Interactions:
  - core: the third named Object subclass that overrides an entry
    point (here __get__) and uses Object only for the recorded name and
    owner; no context frame is pushed by its __get__.
  - mcls: AbstractNamespace must provide addHook and must read each
    hook through the descriptor (so that __space_object__ is rebound to
    the namespace at hand) before calling a phase. Because the hook
    object is one per namespace class and the binding is a single
    mutable attribute, a nested class body (an inner class statement
    inside an outer body) rebinds it to the inner namespace; whether
    the outer namespace re-reads the hook before its next phase call
    decides whether that is safe. Check in _abstract_namespace.py.
  - dispatch and desc: none here; the concrete hooks bring them in.
- Support: SpaceDesc (:10); core Object and MetaType (:11).
- Notes: setItemPhase is the only phase with a veto; the others
  signal by raising or by returning a transformed dict.

## mcls/space_hooks/_flex_call_hook.py : FlexCallHook

- Item: src/worktoy/mcls/space_hooks/_flex_call_hook.py, 53 lines.
  Fourth import of the subpackage.
- What it is: an opt-in hook whose postCompilePhase (:31-53) replaces
  every plain function in the compiled namespace with its flexCall
  wrapper, so methods of the class drop positional arguments beyond
  those they declare. No namespace in worktoy declares it (:21-25), so
  BaseObject methods are called exactly as Python calls any method.
- Interactions: closes the dispatch thread: an overloaded function is
  captured by its overload object before the namespace ever stores a
  function, and the Dispatcher LoadSpaceHook writes is not a
  FunctionType, so even an opted-in namespace never flex-wraps an
  overload's functions; keyword dispatch through _getKeywordBindings is
  unaffected. flexCall itself refuses nothing here since every value
  wrapped is a FunctionType.
- Support: dispatch.flexCall (:10); AbstractSpaceHook (:11).

## mcls/space_hooks/_reserved_namespace_hook.py : ReservedNamespaceHook

- Item: src/worktoy/mcls/space_hooks/_reserved_namespace_hook.py, 97
  lines. Fifth import of the subpackage.
- What it is: setItemPhase (:68-97) raises ReservedName(key) when a
  reserved name is bound while already present in the namespace; a
  first binding passes, which is how the interpreter's own deferred
  writes of __module__, __qualname__, __doc__ and the rest go through
  (:41-47). reservedNames = ReservedNames() (:62) supplies the list.
- Interactions: 'key in self.space' is the namespace's __contains__,
  so a namespace whose __contains__ is hooked answers here too. A user
  re-binding __doc__ after a docstring, or __module__, is refused as
  the class body runs.
- Support: waitaminute.meta.ReservedName (:10); AbstractSpaceHook and
  ReservedNames (:11).

## mcls/space_hooks/_name_hook.py : NamespaceHook

- Item: src/worktoy/mcls/space_hooks/_name_hook.py, 312 lines. Sixth
  import of the subpackage.
- What it is: the name screen of a class body plus the seeding of the
  routed __class_*__ hooks. It refuses near-miss dunder spellings, a
  __del__ without the trustMeBro keyword, a routed hook bound as a
  plain function or staticmethod, and a routed hook whose operation a
  metaclass before AbstractMetaclass implements itself (:24-64).
- Symbols:
  - _getClassDunders, :78-120: the routed names: __class_call__,
    __class_init__, __class_instancecheck__, __class_subclasscheck__,
    __class_str__, __class_repr__, __class_iter__, __class_next__,
    __class_bool__, __class_contains__, __class_len__, __class_hash__,
    __class_setitem__, __class_delitem__, __class_getattr__,
    __class_setattr__, __class_delattr__. Commented out: __class_eq__
    and __class_ne__ (undefined behaviour), __class_getitem__ (an
    interpreter feature since 3.7, with a long footnote :105-119).
  - _getNearMisses, :122-133: (__set_name__, __setname__),
    (__getitem__, __get_item__), (__setitem__, __set_item__),
    (__delitem__, __del_item__).
  - _getChainedHooks, :135-144: ['__class_init__'], the one hook not
    called from an operation but from AbstractMetaclass.__init__.
  - _getOperation(hookName), :146-152: '__class_len__' to '__len__'.
  - _getShadowingMetaclass(hookName), :154-177: with
    AbstractMetaclass imported locally, the first class in the building
    metaclass's MRO before AbstractMetaclass whose __dict__ holds the
    operation, else None; a metaclass outside the family calls no hook.
  - _validateName, :179-190: QuestionableSyntax(intended, mistyped).
  - _validateDel, :192-201: the namespace's class keywords must carry a
    truthy trustMeBro.
  - setItemPhase, :207-263: __del__ handling (DelException with the
    metaclass, class name, bases and namespace), ShadowedClassHook,
    UnboundClassHook for a FunctionType or staticmethod value (the
    metaclass invokes hooks as bound classmethods, :256-260), then the
    near-miss check. Always returns False for an accepted name.
  - preCompilePhase, :265-298: for each routed name the body did not
    bind (checked with dict.__contains__ on the namespace, bypassing
    hooks), a class along space._getLookupOrder() that supplies it is
    validated through _validateInheritedHook (plain function or
    staticmethod on a plain base raises UnboundClassHook naming the
    base), otherwise compiledSpace[name] = METACALL.
- Interactions:
  - core: METACALL is written here for every routed hook a class and
    its bases leave undefined; AbstractMetaclass reads it to fall back
    to its own implementation. This resolves the METACALL thread.
  - mcls: relies on the namespace API getMetaclass, getClassName,
    getBases, getKwargs, _getLookupOrder. The trustMeBro class keyword
    is a second concrete class keyword, read from the namespace's
    kwargs and absorbed by _Chill at the end.
  - keenum and ezdata: KeeMeta and EZMeta are the named shadowing
    metaclasses (:57-59).
- Support: METACALL (:12); waitaminute.meta QuestionableSyntax,
  DelException, UnboundClassHook, ShadowedClassHook (:13-14);
  AbstractSpaceHook (:15).
- Notes:
  - Derived from CPython's PyObject_GetItem, not executed: subscripting
    a class calls the metaclass's __getitem__ when the metaclass has
    one and consults __class_getitem__ only when it has none. The
    footnote at :111-113 states the opposite order. The practical
    question is whether AbstractMetaclass defines __getitem__; read
    there.
  - A routed hook bound as a classmethod in the body passes; one bound
    through a plain base is validated only at the class statement of
    the subclass, which is where it would first be called.

## mcls/space_hooks/_load_space_hook.py : LoadSpaceHook

- Item: src/worktoy/mcls/space_hooks/_load_space_hook.py, 146 lines.
  Last import of the subpackage.
- What it is: the bridge from overload to Dispatcher. setItemPhase
  claims every overload bound in the class body and records its
  registrations on the namespace; postCompilePhase builds one
  Dispatcher per overloaded name from the registrations the namespace
  merges across the MRO and writes it into the compiled dict (:20-26).
- Symbols:
  - setItemPhase, :32-86. A non-overload value under a name this body
    already overloaded raises OverloadConflict(className, key, True);
    otherwise the name is noted as plain and stored normally. An
    overload under a name already bound plainly raises OverloadConflict
    (..., False). The first binding of an overload object claims the
    name (addClaimedName); a later binding of the same object under
    another name in the same body is an alias and copies every
    registration the source name holds so far, inherited ones included
    (:57-73). A fresh claim records the fallback and finalizer roles and
    adds each concrete and variadic pair with the signature copied
    through sig() (:79-85), because naming the class rewrites THIS in
    place and an overload bound in two class bodies must not hand the
    second the first's fixed signatures. Returns True, so the overload
    object itself is never stored in the namespace.
  - postCompilePhase, :88-119: for each name in getOverloadNames() not
    held by the namespace dict (a plain definition in the body wins
    over inherited overloads), _buildDispatcher.
  - _buildDispatcher(name), :125-146: collectOverloads, collectVariadics,
    collectFallback and collectFinalizer; None when all are empty (a
    plain definition in a base shadows everything); otherwise a fresh
    Dispatcher fed with addSigFunc(sig, func, distance),
    addVariadicSigFunc, setFallbackFunction, setFinalizerFunction.
- Interactions:
  - dispatch: TypeSig.__call__ with no arguments is the copier relied
    on here (:83, :85), which corrects the TypeSig docstring's claim
    that _copySig is the one relying on it. Every class gets a fresh
    Dispatcher built from merged registrations with distances, so
    Dispatcher.clone and restoreTHIS are not on this path; they serve
    by-hand wiring. The Dispatcher's __set_name__ then fires when
    type.__new__ sees it in the compiled dict, swapping THIS. An equal
    signature from the body and from a base must be de-duplicated by
    the namespace's collect methods, since addSigFunc refuses
    duplicates; check in BaseSpace.
  - core: nothing directly.
  - mcls: relies on the BaseSpace API hasOverloads, addPlainName,
    getPlainNames, getClaimedName, addClaimedName, collectOverloads,
    collectVariadics, collectFallback, collectFinalizer, addOverload,
    addVariadic, addFallback, addFinalizer, getOverloadNames. Expect
    those to read inherited registrations off the bases, which is the
    likely consumer of cls.__namespace__.
- Support: dispatch overload and Dispatcher (:10);
  waitaminute.meta.OverloadConflict (:11); AbstractSpaceHook (:12).
- Notes: the copy made by sig() shares a trailing ARGS instance with
  the original; swapTHIS later replaces it inside the copy's own raw
  tuple, so the shared instance is never mutated.

## mcls/space_hooks summary

- Seven items read in order. The subpackage is where the class body is
  policed (NamespaceHook, ReservedNamespaceHook), where overloads
  become Dispatchers (LoadSpaceHook), where METACALL is seeded, and
  where flexCall could be applied if a namespace opted in. The hooks
  address the namespace only through a small method API that
  AbstractNamespace and BaseSpace must supply.

## waitaminute/meta : the nine remaining metaclass exceptions (support, read ad hoc from the hooks and AbstractNamespace)

All nine are based on WorkToyException first. Six are SyntaxErrors
(refusals of a class-body line) and set self.msg = str(self) in
__init__ because a SyntaxError traceback shows msg; three are plain
Exceptions. Each formats through textFmt.

- _reserved_name.py, 41 lines: ReservedName(name), a SyntaxError, slot
  resName; raised by ReservedNamespaceHook.setItemPhase on a
  reassignment of an interpreter-set name.
- _questionable_syntax.py, 44 lines: QuestionableSyntax(realName,
  derpName), a SyntaxError; raised by NamespaceHook._validateName for a
  near-miss dunder.
- _del_exception.py, 55 lines: DelException(mcls, name, bases, space),
  a SyntaxError, unpacking exactly four positional arguments (:36); the
  message names the metaclass and bases and tells the user about
  trustMeBro=True. Raised by NamespaceHook.setItemPhase.
- _unbound_class_hook.py, 71 lines: UnboundClassHook(className,
  hookName, baseName=None), a SyntaxError, with one wording for a hook
  bound in the body and one for a hook inherited from a plain base.
  Raised by NamespaceHook.setItemPhase and _validateInheritedHook.
- _shadowed_class_hook.py, 70 lines: ShadowedClassHook(className,
  hookName, metaclassName, methodName), a SyntaxError; the docstring
  (:22-28) records that KeeMeta, KeeFlagsMeta and EZMeta implement most
  operations themselves and that a __class_call__ in an enumeration
  body used to break the class statement. Raised by
  NamespaceHook.setItemPhase.
- _overload_conflict.py, 63 lines: OverloadConflict(className,
  overloadName, overloadsFirst), a SyntaxError; a name bound both to
  overloads and to a plain definition in one body, in either order; a
  subclass may still replace what it inherits either way (:21-22).
  Raised by LoadSpaceHook.setItemPhase. Its __str__ passes two strings
  to textFmt (:61).
- _hook_exception.py, 78 lines: HookException(exception, namespace,
  key, val, hook), an Exception; wraps anything a hook's getItemPhase
  raises so it cannot be mistaken for the KeyError the class-body name
  lookup uses as its fall-through signal (:21-30). Raised by
  AbstractNamespace.__getitem__.
- _duplicate_hook.py, 50 lines: DuplicateHook(owner, name, existing,
  new), an Exception, padded unpacking of up to four arguments (:34);
  a different hook object at a field name already taken, while
  re-registering the same hook is a no-op. Raised by
  AbstractNamespace.addHook.
- _claimed_name.py, 53 lines: ClaimedName(className, keyName), a
  SyntaxError; a class body deleted a name whose latest binding a hook
  claimed; raised from compile rather than from the deletion because
  the interpreter turns any exception from a class-body 'del' into
  NameError (:24-27). Raised by AbstractNamespace.compile.

## mcls/_abstract_namespace.py : AbstractNamespace

- Item: src/worktoy/mcls/_abstract_namespace.py, 434 lines. Second
  import of mcls/__init__.py:39.
- What it is: the dict subclass a worktoy metaclass returns from
  __prepare__. It runs the registered hooks at each phase, keeps a
  shadow mapping of every class-body assignment so a claimed name stays
  readable, records claimed deletions for a refusal at compile, and
  compiles itself into the plain dict type.__new__ receives, which it
  also keeps so a subclass can collect what it inherits (:28-56).
- Symbols:
  - __owner_hooks_list_name__ = '__hook_objects__' (:63), the class
    attribute the hook list lives under; private slots :66-73
    (__metaclass__, __class_name__, __base_classes__, __class_mro__,
    __key_args__, __compiled_space__, __shadow_space__,
    __claimed_deletions__); the two hooks every namespace carries,
    reservedNameHook = ReservedNamespaceHook() and nameHook =
    NamespaceHook() (:76-77), registered through their __set_name__.
  - getBases, :83-84; getShadowSpace, :86-103; getClaimedDeletions,
    :105-111; deepGetItem, :113-125 (own dict, else the MRO space's
    list of values, else KeyError).
  - getHooks, :131-137: a generator yielding each registered hook after
    hook.__get__(self, cls) and a second explicit rebinding of
    __space_object__; classGetHooks, :139-154: the hooks of the class
    and its dict-based bases, de-duplicated by identity in MRO order.
  - getMetaclass, getClassName, getKwargs (a copy), getMRO, :156-168.
  - _getLookupOrder, :170-186: the resolved MRO of the bases, or with
    _strictMRO=False and no consistent order, each base's own MRO left
    to right without repeats.
  - getMROSpace, :188-212: for each class in the lookup order that has
    __namespace__ with a __compiled_space__, the compiled dict's items
    accumulated as key to list of values, nearest class first. A
    MetaType-made class whose __namespace__ is a plain dict (no
    __compiled_space__) is skipped, which makes the leftover key from
    MetaType.__new__ harmless here.
  - addHook(hook), :218-235: classmethod; a different hook at a taken
    field name raises DuplicateHook, the same hook is a no-op;
    otherwise the class attribute list becomes the inherited hooks
    followed by the new one, so inherited hooks always run before a
    subclass namespace's own.
  - __init__(mcls, name, bases, **kwargs), :241-265: stores the four,
    resolves the MRO of the bases through resolveMRO, re-raising its
    TypeError unless _strictMRO=False, then runs every hook's
    preparePhase.
  - __getitem__, :271-298: the dict value, else the shadow value, else
    the KeyError kept aside; every hook's getItemPhase runs (an
    exception becomes HookException); the KeyError is re-raised after
    the hooks so the class body's lookup falls through to globals.
  - __setitem__, :300-320: the shadow records the binding; hooks'
    setItemPhase in order until one returns True; else dict store.
  - __delitem__, :322-344: KeyError when never bound; a claimed latest
    binding is recorded for ClaimedName; removed from shadow and dict.
  - _isClaimed, :346-357: the shadow and the dict disagree exactly when
    the latest binding was claimed.
  - __str__ and __repr__, :359-380.
  - preCompile, :386-400; compile, :402-422: ClaimedName for recorded
    deletions, preCompile over a fresh dict, the class-body names
    merged in, postCompile, then __metaclass__, __namespace__ (self)
    and __keyword_arguments__ written into the dict, which is stored
    as __compiled_space__ and returned; postCompile, :424-434.
- Interactions:
  - core: every class a worktoy metaclass builds carries __namespace__,
    __metaclass__ and __keyword_arguments__ in its __dict__ (:418-420).
    This resolves the cls.__namespace__ thread: it is the designed
    channel through which a subclass namespace reads a base's compiled
    dict, and MetaType.__new__ sees the key already present and inserts
    nothing. The class keywords reach the namespace through __prepare__
    and are read by the hooks (trustMeBro) and here (_strictMRO).
  - mcls/space_hooks: every phase call site re-reads the hooks through
    getHooks, which rebinds __space_object__ before each call, so a
    nested class statement inside a class body rebinds the shared
    hooks to the inner namespace and the outer namespace's next phase
    call binds them back. This closes the AbstractSpaceHook thread.
  - dispatch: through LoadSpaceHook (declared by BaseSpace, not here);
    the shadow space is what lets a class body refer to an overloaded
    name after the overload object was claimed.
  - desc: an AttriBox or Field in a class body is stored normally (no
    hook claims it) and receives __set_name__ from type.__new__; Alias
    replacing itself by setattr happens after compile, on the class.
- Support: utilities maybe, textFmt, resolveMRO (:10); waitaminute
  TypeException (:11); waitaminute.meta HookException, DuplicateHook,
  ClaimedName (:12); space_hooks NamespaceHook, ReservedNamespaceHook
  (:13). resolveMRO is read next.
- Notes:
  - DuplicateHook makes it impossible for a namespace subclass to
    replace an inherited hook under the same attribute name; a new
    hook must take a new name.
  - The __getitem__, __setitem__ and __delitem__ signatures carry
    **kwargs the interpreter never passes; harmless.
  - getMROSpace collects values from every base's compiled dict, so
    the merged registrations LoadSpaceHook needs are one deepGetItem
    away; the BaseSpace collect methods are expected to build on it.

## utilities/_resolve_mro.py : resolveMRO (support, read ad hoc from AbstractNamespace.__init__)

- Item: src/worktoy/utilities/_resolve_mro.py, 90 lines.
- What it is: the C3 linearization of a set of bases, excluding the
  hypothetical derived class, so resolveMRO(*bases) equals
  Foo.mro()[1:] for class Foo(*bases) (:13-20). No bases give [], one
  base its own __mro__ (:57-60); otherwise canonical C3 over each
  base's __mro__ plus the base-order list (:61-90), a TypeError through
  textFmt and joinWords when no consistent order exists (:79-82), and
  a RecursionError bailout reachable only through the test-only
  _initialIterationCount keyword (:65, :87-89).
- Interactions: AbstractNamespace computes the lookup order of the
  class under construction from it, before the class exists. The
  bases it sees are the ones __prepare__ received, which the
  interpreter has already resolved through __mro_entries__; the _Chill
  that MetaType.__new__ appends later is absent from this order, which
  changes nothing since _Chill contributes no names.
- Support: joinWords and textFmt (:9).

## mcls/_abstract_metaclass.py : AbstractMetaclass

- Item: src/worktoy/mcls/_abstract_metaclass.py, 369 lines. Third
  import of mcls/__init__.py:40.
- What it is: the base metaclass of the library. It returns an
  AbstractNamespace from __prepare__, compiles it in __new__, runs the
  hooks' newClassPhase, calls __class_init__ and the bases'
  __subclasshook__ in __init__, and routes the builtin operations on a
  class to the __class_*__ hooks of that class, falling back to type
  where the hook is METACALL (:27-138).
- Symbols:
  - AbstractMetaclass(MetaType, metaclass=MetaType), :26. The body is
    annotated (:140-144), so on 3.10+ MetaType installs the
    annotations descriptor on it, and the four hook names
    __class_getattr__, __class_setattr__, __class_delattr__ and
    __class_call__ hold METACALL at metaclass level as a floor under
    the per-class seeding.
  - __prepare__(mcls, name, bases, **kwargs), :146-159: a fresh
    AbstractNamespace with the class keywords.
  - __new__(mcls, name, bases, space, **kw), :161-179: a plain dict is
    copied item by item into a namespace from __prepare__ so the hooks
    run (:169-173); space.compile(); MetaType.__new__ called directly
    with the keywords; each hook's newClassPhase may replace the class
    (maybe keeps it when the hook returns None).
  - __init__(cls, name, bases, space, **kwargs), :181-190:
    MetaType.__init__ (which sets __skip_hash__ False), then the
    __class_init__ hook when it is not METACALL, called as a bound
    classmethod with (name, bases, space, **kwargs), then
    _notifySubclassHook, which calls base.__subclasshook__(cls) on
    every base and ignores the result (:346-352).
  - __call__, :191-194; __instancecheck__ and __subclasscheck__,
    :196-204; __str__ and __repr__, :206-214: hook or the MetaType
    behaviour.
  - __iter__, :216-221 and __next__, :223-228: hook or a TypeError
    worded as Python's. This is the contract utilities.unpack relies
    on: a worktoy class claims to be iterable yet iter() raises
    TypeError when no hook exists, so unpack keeps the class whole.
  - __bool__, :230-247 (the Dante docstring is deliberate flair):
    __class_bool__, else truth of __class_len__, else whether
    __class_iter__ yields anything, else True.
  - __contains__, :249-259: hook, else iteration with ==, else
    TypeError. __len__, :261-268: hook, else a count of the iteration,
    else TypeError.
  - _skipHash(cls), :270-277 and __hash__, :279-287: with no
    __class_hash__, the hash of (class name, the names of the bases
    that are neither __skip_hash__ nor object, metaclass name). This
    is the consumer of __skip_hash__: _Chill carries True and so drops
    out of the hash of every class whose bases end in it, while every
    other class carries False and counts. Equality stays identity.
  - The commented-out __eq__, __ne__ and __getitem__ (:289-306) are
    kept on purpose; the metaclass defines no __getitem__, so the
    interpreter's own __class_getitem__ route applies (:117-121). That
    settles the precedence question raised under NamespaceHook: the
    footnote there misstates CPython's order, but since no __getitem__
    exists on the metaclass the outcome is as the author intends.
  - __setitem__ and __delitem__, :308-320: hook or TypeError.
  - __getattr__(cls, name), :322-330: a miss on a class raises
    MissingVariable(cls, name), an AttributeError, unless
    __class_getattr__ answers; the docstring warns that any other
    attribute read with the dot operator inside this method recurses.
  - __setattr__ and __delattr__, :332-340: hook or the MetaType
    (type) behaviour.
  - getNamespace(cls), :354-360: __namespace__ read through
    type.__getattribute__; getNamespaceClass(mcls), :362-369: the type
    of a throwaway __prepare__('_', ()).
- Interactions:
  - core: built on MetaType (bases become (MetaType, _Chill)); the
    class keywords travel to MetaType.__new__ and end in _Chill; the
    METACALL sentinel is the routing switch; the name-based hash
    parallels SentinelMeta.__hash__.
  - mcls: NamespaceHook seeds METACALL for every routed hook a class
    leaves undefined, so the 'is METACALL' tests above never miss and
    never trigger __getattr__; a class built from a plain dict still
    goes through a namespace and so is seeded too.
  - desc: AttriBox.__reduce__'s getattr(owner, name) finds the box in
    the class dict before __getattr__ could interfere; Alias's
    setattr during __set_name__ goes through __setattr__ and so
    through a __class_setattr__ hook if the class defines one;
    __getattr__ raising an AttributeError subclass keeps getattr
    defaults and hasattr working for every descriptor lookup.
  - dispatch: isinstance checks in the FAST tiers call
    __instancecheck__ here, one class-dict lookup of
    __class_instancecheck__ per check before type's own test.
- Support: MetaType (:10); METACALL and SentinelMeta (:11);
  utilities.maybe (:12); waitaminute.MissingVariable (:13);
  AbstractNamespace (:14).
- Notes:
  - __init__ calls MetaType.__init__ and __new__ calls MetaType.__new__
    by name rather than through super(), in keeping with the author's
    habit; a metaclass placed between the two in an MRO would be
    skipped by those calls.
  - Every class message from __getattr__ reads "Missing 'Cls.name'!"
    instead of Python's "type object 'Cls' has no attribute 'name'".
  - getNamespaceClass builds a real namespace, so the preparePhase of
    every hook runs for the throwaway.

## mcls/_base_space.py : BaseSpace

- Item: src/worktoy/mcls/_base_space.py, 438 lines. Fourth import of
  mcls/__init__.py:41.
- What it is: the namespace BaseMeta prepares. It adds the overload
  registries that LoadSpaceHook fills and the collect methods that
  merge a class body's own registrations with those of the classes
  along its method resolution order, nearest first, equal signatures
  skipped, the walk stopping at a plain definition, each registration
  carrying its distance (:40-64). Registrations are lists, not dicts
  keyed by signature, since a THIS signature hashes differently before
  and after its class exists (:62-64).
- Symbols:
  - Private maps :76-81: __overload_map__, __variadic_overload_map__,
    __fallback_map__, __finalizer_map__, __plain_names__,
    __claimed_overloads__; loadSpaceHook = LoadSpaceHook() (:84),
    registered after the two inherited hooks so it runs third.
  - getOverloads, getVariadics, getFallbacks, getFinalizers,
    getPlainNames, getClaimedName (by identity), hasOverloads,
    :90-158: the class body's own records only.
  - _definesPlainly(cls, name), :160-179: a name in cls.__dict__ that
    is not a Dispatcher, or a Dispatcher the class body wrote itself
    (present in that class's BaseSpace dict rather than added at
    compile), or anything a class not built by BaseSpace holds.
  - _getInheritedSpaces(name), :181-201: the BaseSpace namespaces of
    the lookup order up to the first plain definition;
    _getLookupSpaces, :203-214: all of them; getOverloadNames,
    :216-234: every name any of those registered, first appearance.
  - _mergeSigFuncs(collected, more, distance), :236-253: append the
    pairs whose signature equals none collected, with the distance.
  - collectOverloads and collectVariadics(name), :255-283: own at
    distance 0, then each inherited space at its index; collectFallback
    and collectFinalizer, :285-308: own, else the nearest.
  - addOverload(name, sig, func), :314-348: an equal signature with the
    same function is a no-op (an overload bound again under its own
    name), with a different function DuplicateSignature; addVariadic,
    :350-361, appends without a check; addPlainName, addClaimedName,
    :363-379; addFallback and addFinalizer, :381-438, DuplicateSignature
    with the role string for a different function, while an inherited
    one may be replaced.
- Interactions:
  - dispatch: the collected entries feed Dispatcher.addSigFunc and
    addVariadicSigFunc with distances; the de-duplication by
    TypeSig.__eq__ here is what keeps Dispatcher's own DuplicateSignature
    silent on the compile path. A body's @overload(THIS) and an
    inherited signature already swapped to the parent class are not
    equal, so both are collected and the subclass's wins by distance,
    the case the Dispatcher docstring describes.
  - core: the namespaces are reached through each class's
    __namespace__, the designed use of that attribute.
  - mcls: BaseMeta is expected to return this from __prepare__; the
    plain-definition rule gives overloads the precedence Python gives
    plain methods.
- Support: dispatch TypeSig and Dispatcher (:10); utilities.maybe
  (:11); waitaminute.dispatch.DuplicateSignature (:12);
  AbstractNamespace (:13); LoadSpaceHook (:14).
- Notes:
  - Derived, not executed: the inherited entries are the parent
    namespace's own TypeSig objects (the copies LoadSpaceHook stored),
    which the parent's Dispatcher also holds. A child's placement
    swaps nothing in them (THIS is gone), but Dispatcher.restoreTHIS on
    a namespace-built child would reset the parent's signatures to
    their declared THIS and leave the parent's compiled tables stale.
    Nothing in the library calls restoreTHIS on that path; it exists
    for by-hand clones.
  - Distance counts contributing BaseSpace namespaces, not MRO steps,
    so a plain mixin between two worktoy classes does not add to it.
  - A name no class body mentions again still gets a fresh Dispatcher
    in every subclass, built from the inherited registrations at
    distance 1 and beyond.

## mcls/_base_meta.py : BaseMeta

- Item: src/worktoy/mcls/_base_meta.py, 47 lines. Fifth import of
  mcls/__init__.py:42.
- What it is: AbstractMetaclass with one override, __prepare__ returning
  a BaseSpace (:40-47). Nothing else changes; the overload protocol is
  entirely BaseSpace's LoadSpaceHook (:25-28).
- Interactions:
  - mcls: the metaclass of BaseObject; BaseMeta.__new__ and __init__
    are AbstractMetaclass's, so a class statement under BaseMeta runs
    the three hooks (reserved, name, load) and ends with a Dispatcher
    per overloaded name in its dict.
  - core: BaseMeta's body carries no annotation, so on 3.10+ it has no
    annotations descriptor of its own and BaseMeta.__dict__ holds no
    '__annotations__'. Reading BaseMeta.__annotations__ (as
    inspect.get_annotations on the metaclass would) makes type store
    an empty plain dict on BaseMeta, which from then on sits ahead of
    AbstractMetaclass's descriptor for every BaseMeta class and revives
    the fall-through the descriptor exists to stop (derived from
    CPython's type_getattro and type_get_annotations, not executed).
    This is the concrete case of the concern recorded under
    core/_annotations_descriptor.py; nothing in the four packages reads
    a metaclass's annotations.
- Support: AbstractMetaclass and BaseSpace (:10-11).

## mcls/_base_object.py : BaseObject

- Item: src/worktoy/mcls/_base_object.py, 25 lines. Last import of
  mcls/__init__.py:43.
- What it is: class BaseObject(Object, metaclass=BaseMeta) with an
  empty body (:12-25), the standard entry point: Object's constructor
  capture, context-aware descriptor protocol and read-only class-value
  semantics, plus BaseMeta's overloading and hooks.
- Interactions:
  - core: its only declared base is Object, already a MetaType
    instance, so MetaType appends no second _Chill; the MRO is
    BaseObject, Object, _Chill, object. Instances have a __dict__, so
    AttriBox fields store without MissingInstanceDict. Object.__init__
    captures every constructor argument unless an @overload on
    __init__ replaces __init__ with a Dispatcher, in which case the
    capture only happens if the chosen overload calls Object.__init__;
    createContext tolerates the class-level None either way.
  - mcls: the class statement itself goes through BaseSpace, so
    BaseObject's dict carries the seventeen __class_*__ names as
    METACALL plus __namespace__, __metaclass__ and
    __keyword_arguments__; every subclass is built the same way.
  - dispatch: an @overload in a subclass body becomes a Dispatcher
    whose __set_name__ swaps THIS for the subclass; the compiled
    dispatch is reached as a fresh bound method on every attribute
    read.
  - desc: a BaseObject instance placed in another class body is a data
    descriptor whose reads return it and whose instance writes raise
    ReadOnlyError, the shared read-only class value of Object's
    docstring; a BaseObject with a FastBox or AttriBox field is the
    ordinary user class.
- Support: BaseMeta (:8); core.Object (:9).

## mcls package summary

- Items read, in order: space_hooks (SpaceDesc, ReservedNames,
  AbstractSpaceHook, FlexCallHook, ReservedNamespaceHook, NamespaceHook,
  LoadSpaceHook), AbstractNamespace, AbstractMetaclass, BaseSpace,
  BaseMeta, BaseObject; support read ad hoc: resolveMRO and all twelve
  waitaminute.meta exceptions.
- The spine: __prepare__ returns a hooked dict subclass; the class body
  runs through __setitem__ with the hooks screening names, claiming
  overloads and recording a shadow; compile() seeds METACALL, merges
  the body, builds Dispatchers and stamps __namespace__; MetaType
  builds the class with _Chill at the end; AbstractMetaclass routes the
  builtin operations on the class to the __class_*__ hooks or to type.

# Closing summary of the read

## Threads opened in core and where they closed

- __skip_hash__ (core/_meta_type.py:22, :29, :92): consumed by
  AbstractMetaclass._skipHash and __hash__
  (mcls/_abstract_metaclass.py:270-287) to drop _Chill from the
  name-based class hash.
- cls.__namespace__ (core/_meta_type.py:83-88): a designed attribute.
  AbstractNamespace.compile writes it (mcls/_abstract_namespace.py:419),
  ControlSpace writes it for signals (core/control_flow/_control_space.py:56),
  and BaseSpace reads a base's compiled dict through it to merge
  inherited overloads (mcls/_base_space.py:174-214). On a class built
  with a plain dict the key still lands in the class dict pointing at
  that dict, which getMROSpace skips.
- METACALL: seeded by NamespaceHook.preCompilePhase for every routed
  hook a class leaves undefined (mcls/space_hooks/_name_hook.py:265-298)
  and tested by identity in every AbstractMetaclass operation.
- THIS and ARGS in signatures: TypeSig recognises both; swapTHIS runs
  from Dispatcher.__set_name__ when the class exists; LoadSpaceHook
  copies signatures with sig() so an overload bound in two bodies is
  safe; ARGS.__iter__ yielding itself is what lets utilities.unpack
  keep an ARGS whole.
- THIS, OWNER, DESC in boxes: resolved by Object.getPosArgs,
  getKeyArgs and filterSentinels against the frame Object.__get__ or
  __set__ pushed, consumed by AttriBox._resolve and _assignedArgs.
- StorageCollision: raised by AttriBox._refuseStorageCollision from
  __set_name__, within one class body only.
- flexCall and overloads: FlexCallHook is opt-in and no worktoy
  namespace declares it; overload functions are captured before the
  namespace stores anything, so they are never flex-wrapped.
- Hook rebinding under nested class bodies: safe, because every phase
  call site re-reads the hooks through getHooks and rebinds
  __space_object__ (mcls/_abstract_namespace.py:131-137 and each call
  site).
- Metaclass bodies without annotations: AbstractMetaclass, SentinelMeta
  (no annotations but no annotated parent either), MetaFlow and
  _MetaARGS are annotated; BaseMeta is not, see its entry.

## Observations recorded as derived, not executed

Each is stated at the entry it belongs to; this list is the index.

1. Detached refuses every dunder (waitaminute/_detached.py:62-63), so a
   rebuilt exception whose message reads a dunder through a Detached
   argument fails inside __str__; its docstring example at :24 is such
   a read. Concrete cases: ControlClassError (space.__metaclass__),
   DispatchException (dispatch.__field_owner__). A method call through
   a Detached (WithoutException's desc.getFieldOwner()) fails as well.
2. MetaType.__new__ leaves '__namespace__' in the dict of a class built
   from a plain dict (core/_meta_type.py:83-88).
3. A metaclass body without annotations reading its own
   __annotations__ on 3.10+ shadows the parent's annotations descriptor
   for its classes (core/_annotations_descriptor.py; BaseMeta).
4. CallMeMaybe's one-tuple defence (dispatch/_call_me_maybe.py:76-91)
   guards against a binding that per-instance storage never performs.
5. TypeSig.__call__'s docstring names Dispatcher._copySig as the caller
   relying on the no-argument copy; _copySig builds its copy by hand,
   and LoadSpaceHook (:83, :85) is the actual caller.
6. NamespaceHook's footnote (mcls/space_hooks/_name_hook.py:111-113)
   reverses CPython's precedence between a metaclass __getitem__ and
   __class_getitem__; harmless because AbstractMetaclass defines no
   __getitem__.
7. AttriBox._refuseStorageCollision inspects owner.__dict__ only, so a
   subclass field whose private name equals an inherited field's
   shares its storage without a refusal (desc/_attri_box.py:597-615).
   Confirmed by running on 2026-10-20 and fixed the same day: the guard
   now walks owner.__mro__, exempting a box under the same name in a
   base as a redeclaration, and names an inherited box 'Parent.fooBar';
   pinned by tests/test_desc/test_attri_box_storage_collision.py.
8. Object.__delete__ treats an __instance_get__ that raises
   AttributeError (deletion proceeds with old=None) differently from
   one that returns DELETED (MissingVariable before the deleters run)
   (core/_object.py:329-337); AttriBox stores DELETED on a never-read
   field while FastBox raises.
9. Namespace-built Dispatchers share the parent namespace's TypeSig
   objects with the parent's Dispatcher, so Dispatcher.restoreTHIS on
   such a child would rewrite the parent's signatures
   (mcls/_base_space.py:255-283); no library path calls it there.
10. overload.__next_sig__ and __next_func__ (dispatch/_overload.py:110-111)
    are unused; _getLatestFunc raises a plain RuntimeError (:139-144).
11. The local textFmt imports inside ControlClassError.__str__ and
    TypeCastException.__str__, and the local maybe import inside
    WithoutException.__str__, differ from the module-level imports the
    other exceptions use.
12. AttriBox._callFieldType names its TypeException 'value' while the
    other build branches name the field (desc/_attri_box.py:512, :522).
13. AbstractNamespace.addHook refuses a subclass namespace that
    re-declares a hook under an inherited attribute name
    (mcls/_abstract_namespace.py:225-233).

## Coverage

- Every module of core (with sentinels and control_flow), dispatch,
  desc and mcls (with space_hooks) was read in full, every __init__
  included, in the order of the package __init__ files.
- Support read in full as referenced: utilities maybe, textFmt,
  Directory, joinWords, unpack, QuickDesc, ValidSlice, typeCast,
  resolveMRO and the combinatorics subpackage; waitaminute Detached,
  WorkToyException, TypeException, VariableNotNone, UnpackException,
  MissingVariable and the complete desc, meta and dispatch
  subpackages.
- Not read, because nothing in the four packages references them:
  utilities argsCount, bipartiteMatching, ClassBodyTemplate,
  ExceptionInfo, replaceFlex, sliceLen, stringList, wordWrap and the
  two empty modules _generic_fixed.py and _get_unbound.py;
  waitaminute SubclassException and the keenum, ezdata and
  control_flow subpackages.

