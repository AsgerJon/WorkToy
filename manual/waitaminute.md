# worktoy manual: waitaminute

`worktoy.waitaminute` holds the exceptions of worktoy, about seventy of
them. The name is a joke on what an exception says, and it is the only
name: there is no `worktoy.exceptions`. The other chapters say when
each exception is raised; this one says how to catch them, how to read
them, and how to raise them yourself.

Everything shown here is promised. The examples are checked against
every release, so they keep working in every update. Anything this
chapter does not show may change.

Contents:

1. Catching worktoy's exceptions
2. Reading an exception: attributes, not messages
3. Where each exception lives
4. Raising them yourself
5. Exceptions of your own


## 1. Catching worktoy's exceptions

Every exception worktoy defines is two things at once: a
`WorkToyException`, and the builtin that best matches its meaning. So
you can catch it either way:

```
>>> from worktoy.utilities import typeCast
>>> from worktoy.waitaminute import WorkToyException
>>> try:
...   typeCast(int, '3')
... except TypeError:
...   print('caught as the builtin')
caught as the builtin
>>> try:
...   typeCast(int, '3')
... except WorkToyException:
...   print('caught as worktoy')
caught as worktoy

```

Code you already have, catching `TypeError` or `AttributeError`, keeps
working when worktoy raises one of its own.

`except WorkToyException` catches every exception worktoy defines, but
not everything worktoy raises. A few small helpers raise a plain
builtin, as `sliceLen` raises Python's own `ValueError` for a step of
zero, and the chapters say where. The control-flow signals of the core
chapter are no `WorkToyException` either, on purpose: they are not
errors.

A few bases are worth knowing before they surprise you:

- `RecursiveRead` is a `RecursionError`, so a handler you wrote for deep
  recursion catches it too.
- `KeeResolveError`, raised when an enumeration has no member for a
  name or a value, is a plain `Exception`, not a `ValueError` as with
  Python's `Enum`.
- `KeeTypeException` is a `TypeError` but no `TypeException`; catch
  `TypeError` to get both.
- `VariableNotNone`, raised when a value meant to be set once is set
  again, is a plain `Exception`.


## 2. Reading an exception: attributes, not messages

Each worktoy exception keeps the facts it was raised with as
attributes. The message is written for a person and may be reworded in
any release; the attributes are promised.

```
>>> from worktoy.waitaminute.dispatch import TypeCastException
>>> try:
...   typeCast(int, 3.5)
... except TypeCastException as refusal:
...   print(refusal.type_.__name__, refusal.arg)
int 3.5

```

Each chapter names the attributes of the exceptions it raises.


## 3. Where each exception lives

The exceptions are grouped by the part of worktoy that raises them, and
each imports from its group:

- `worktoy.waitaminute`, the cross-cutting ones: `TypeException`,
  `UncheckableType`, `SubclassException` (`TypeError`);
  `UnpackException` (`ValueError`); `MissingVariable`
  (`AttributeError`); `VariableNotNone` (`Exception`); and the root,
  `WorkToyException`.
- `worktoy.waitaminute.desc`, the descriptors: `AccessError`,
  `ReadOnlyError`, `ProtectedError` (`AttributeError`, and all three
  `DescriptorException`s); `WriteOnceError`, `MissingInstanceDict`,
  `NotADescriptor` (`TypeError`); `WithoutException` (`RuntimeError`);
  `RecursiveRead` (`RecursionError`); `NamelessCallback`,
  `DanglingAlias`, `SharedDescriptor`, `ReferenceConflict`,
  `OverloadReference` (`SyntaxError`); `PhantomBoxError` and
  `DescriptorException` (`Exception`).
- `worktoy.waitaminute.meta`, the metaclasses: `IllegalInstantiation`,
  `DuplicateSentinel`, `ControlClassError` (`TypeError`);
  `DelException`, `QuestionableSyntax`, `ReservedName`,
  `UnboundClassHook`, `OverloadConflict`, `ReboundOverload`,
  `MixedMethodKind`, `ClaimedName`, `ShadowedClassHook`, `SlotsRefused`
  (`SyntaxError`); `DuplicateHook`, `HookException` (`Exception`).
- `worktoy.waitaminute.dispatch`, the overloads and conversion:
  `BareOverload`, `DispatchException`, `DuplicateSignature`,
  `TypeCastException` (`TypeError`); `UnboundCastHook` (`SyntaxError`).
- `worktoy.waitaminute.keenum`, the enumerations: `KeeBoxTypeError`,
  `KeeTypeException` (`TypeError`); `KeeBoxValueError`,
  `KeeNameConflict`, `KeeCaseException`, `KeeFlagNameError`
  (`ValueError`); `KeeWriteOnceError` (`AttributeError`);
  `KeeMemberNameError` (`SyntaxError`); `KeeBoxException`,
  `KeeDuplicate`, `KeeFlagDuplicate`, `KeeResolveError` (`Exception`).
- `worktoy.waitaminute.ezdata`, the dataclasses: `ExtraPositionalException`,
  `KwargsOnlyException`, `ExtraKeywordException`,
  `RepeatedFieldException` (`TypeError`); `DuplicateError`,
  `IncompleteFieldException`, `ReservedFieldError`, `ClassFieldError`,
  `ReservedMethodError`, `ReservedAttributeError` (`SyntaxError`).

So the place to import from follows the part of worktoy you were
using when it was raised: `TypeCastException` sits with the overloads,
which convert through `typeCast` on every call.

Many of them are `SyntaxError`s. That marks a mistake in a declaration:
the code is valid Python, but what it declares is refused, most often
as the class is created, at the line of the class body that made the
mistake. A refusal of a value passed at run time is a `TypeError`,
`ValueError` or `AttributeError` instead.


## 4. Raising them yourself

The cross-cutting exceptions at the top of `worktoy.waitaminute` are
offered for your own checks as well:

- `TypeException(name, value, *types)` for a value of the wrong type;
- `MissingVariable(instance, name, *types)` for a value still `None`;
- `VariableNotNone(name, value)` for a value meant to be set once, set
  again, `value` being the one already there;
- `UnpackException(*args)` for arguments with nothing to unpack;
- `SubclassException(subClass, baseClass)` for a class that is no
  subclass of the one required.

```
>>> from worktoy.waitaminute import TypeException
>>> def setWidth(width):
...   if not isinstance(width, (int, float)):
...     raise TypeException('width', width, int, float)
...   return width
>>> try:
...   setWidth('wide')
... except TypeError as refusal:
...   print(refusal.varName, refusal.actualType.__name__)
width str

```

Each records what you give it and checks nothing: deciding that the
value is wrong is your code's job. Mind the order of the arguments:
`TypeException` takes the name first, `MissingVariable` the instance
first. The other exceptions of worktoy are raised by worktoy, and their
constructors are not promised for raising by hand.


## 5. Exceptions of your own

A project may base its own exceptions on `WorkToyException`, with the
builtin it means beside it. Such an exception takes its message as any
Python exception does:

```
>>> class BudgetExceeded(WorkToyException, ValueError):
...   pass
>>> try:
...   raise BudgetExceeded('over by 5')
... except ValueError as error:
...   print(error)
over by 5

```

Do that when your code extends worktoy and should be caught with it.
An `except WorkToyException` then catches your exceptions too, which is
the point; for exceptions that have nothing to do with worktoy, a base
of your own is the better choice.
