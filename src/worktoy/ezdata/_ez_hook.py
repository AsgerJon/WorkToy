"""
EZHook is the namespace hook that builds the 'EZData' methods from its
declared fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import operator
from collections.abc import Callable
from copy import deepcopy
from types import FunctionType
from typing import TYPE_CHECKING

from . import EZField
from ..mcls.space_hooks import AbstractSpaceHook, ReservedNames
from ..utilities import typeCast, textFmt
from ..waitaminute import TypeException
from ..waitaminute.dispatch import TypeCastException
from ..waitaminute.ezdata import ExtraPositionalException, \
  KwargsOnlyException, IncompleteFieldException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias, Iterator
  from . import EZSpace

  INIT: TypeAlias = Callable[..., None]
  ITER: TypeAlias = Callable[..., Iterator]
  BOOL: TypeAlias = Callable[..., bool]

_DESCRIPTOR_KEYS: tuple[str, ...] = (
  '__get__',
  '__set__',
  '__delete__',
  '__set_name__',
)


def _unorderable(self: Any, other: Any) -> Any:
  """
  The '_unorderable' function is the shared comparison dunder installed
  as '__lt__', '__le__', '__gt__', and '__ge__' on every non-ordered
  'EZData' subclass. It returns 'NotImplemented' unconditionally, so
  the interpreter falls back to its standard TypeError for unsupported
  comparisons, while ordering dunders inherited from an ordered base
  class are still shadowed.
  """
  return NotImplemented


class EZHook(AbstractSpaceHook):
  """
  EZHook is the namespace hook installed on every 'EZSpace'. It
  intercepts class-body assignments through 'setItemPhase' to
  capture EZField declarations, fail-fasts on incomplete fields
  via '_assertCompleteField', and synthesizes every generated
  method on the class through 'preCompilePhase' and
  'postCompilePhase'.

  Every code-generation factory lives on EZHook as a
  '@classmethod' rather than in separate per-method files. The
  factories that return user-overridable helpers ('__repr__',
  '__str__', '__field_pairs__', 'asDict', 'asTuple', 'replace')
  are wired in 'preCompilePhase' so a class-body method
  definition of the same name wins; the rest are wired
  unconditionally in 'postCompilePhase'.

  The three class-level synonym tuples ('__frozen_keys__',
  '__ordered_keys__', '__kw_only_keys__') hold the accepted
  spellings for the three build-option flags. A subclass of
  EZHook can extend these to accept additional spellings;
  'parseKwargs' (inherited from 'Object') picks the first
  spelling present in the class kwargs.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Annotations
  space: EZSpace

  #  Class Variables
  __frozen_keys__: tuple[str] = ('frozen', 'immutable', 'hashable',)
  __ordered_keys__: tuple[str] = ('ordered', 'sortable', 'comparable',)
  __kw_only_keys__: tuple[str] = ('kwOnly', 'keywordOnly', 'kw_only',)

  #  Public Variables
  reservedNames = ReservedNames()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    The 'setItemPhase' method intercepts class-body assignments. An
    EZField value is routed to 'EZSpace.registerEZField' after passing
    '_assertCompleteField'; a function value falls through to the
    namespace untouched; any other value is wrapped through
    'EZField.fromValue' and registered. A bare 'None' value is
    rejected outright, since no field type can be inferred from it.
    Reserved Python names (names starting and ending with double
    underscores that the interpreter populates automatically) are
    also passed through.

    Parameters
    ----------
    key : str
      The class-body attribute name.
    val : Any
      The value being assigned to 'key' in the class body.
    old : Any, optional
      The previous value of 'key' if any, supplied by the
      namespace's '__setitem__' wrapper. Unused here.

    Returns
    -------
    bool
      True when this hook has handled the assignment and the
      namespace should not perform the default 'dict.__setitem__';
      False when the assignment should fall through to the
      namespace.

    Raises
    ------
    IncompleteFieldException
      If the EZField at 'key' is missing its type or its
      construction arguments, or if a bare 'None' value was
      assigned in the class body, leaving no type to infer the
      field from. Raised before registration so the traceback
      points at the class-body line.
    ReservedFieldError
      If an EZField is being registered at a reserved name such
      as 'asDict' or '__post_init__'. Raised by
      'EZSpace.registerEZField'.
    DuplicateError
      If an EZField with the same name has already been
      registered in this class body. Raised by
      'EZSpace.registerEZField'.
    """
    if key in self.reservedNames:
      return False
    if isinstance(val, EZField):
      self._assertCompleteField(key, val)
      self.space.registerEZField(key, val)
      return True
    if isinstance(val, FunctionType):
      return False
    valType: type = type(val)
    for descriptorKey in _DESCRIPTOR_KEYS:
      try:
        _ = getattr(valType, descriptorKey)
      except AttributeError:
        continue
      else:
        break
    else:
      if val is None:
        clsName = self.space.getClassName()
        missing = 'a bare None default cannot infer a field type'
        raise IncompleteFieldException(clsName, key, missing)
      # noinspection PyTypeChecker
      valField = EZField.fromValue(val)
      self.space.registerEZField(key, valField)
      return True
    return False

  def _assertCompleteField(self, key: str, field: EZField) -> None:
    """
    The '_assertCompleteField' method asserts that 'field' carries both
    a type and at least one of the positional or keyword argument
    buckets used to build the default value. A missing piece raises
    'IncompleteFieldException' so the class body fails at the exact line
    that introduced the incomplete field, rather than waiting for class
    compilation or first instantiation.

    Parameters
    ----------
    key : str
      The class-body attribute name the field is being bound to.
    field : EZField
      The EZField instance being registered.

    Raises
    ------
    IncompleteFieldException
      If 'field.__field_type__' is None, or if both
      'field.__pos_args__' and 'field.__key_args__' are None.
    """
    clsName = self.space.getClassName()
    if field.__field_type__ is None:
      missing = 'no field type was set'
      raise IncompleteFieldException(clsName, key, missing)
    noPos = field.__pos_args__ is None
    noKey = field.__key_args__ is None
    if noPos and noKey:
      missing = 'no construction arguments were given'
      raise IncompleteFieldException(clsName, key, missing)

  def preCompilePhase(self, compiledSpace: dict) -> dict:
    """
    The 'preCompilePhase' method installs the dunder methods and
    conversion helpers that 'EZData' subclasses are allowed to overwrite
    ('__repr__', '__str__', '__field_pairs__', 'asDict', 'asTuple',
    'replace'). Each entry is installed before the class body is merged
    in, so a class-body method definition with the same name wins. The
    reserved-name guard in 'EZSpace.registerEZField' prevents these
    names from being used as field names while still permitting method
    overrides.

    Parameters
    ----------
    compiledSpace : dict
      The class namespace being assembled. Mutated in place.

    Returns
    -------
    dict
      'compiledSpace' with the overridable helpers installed.
    """
    compiledSpace['__field_pairs__'] = self.fieldPairsFactory()
    compiledSpace['asDict'] = self.asDictFactory()
    compiledSpace['asTuple'] = self.asTupleFactory()
    compiledSpace['replace'] = self.replaceFactory()
    compiledSpace['__repr__'] = self.reprFactory()
    compiledSpace['__str__'] = self.strFactory()
    return compiledSpace

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    """
    Finalizes the compiled namespace for an 'EZData' subclass under
    construction. Runs after the class body has been merged into
    'compiledSpace', so any user-defined entries are already
    present and may be inspected or replaced. Field-shape
    validation has already happened in 'setItemPhase', so every
    field in '__ez_fields__' is guaranteed complete by the time
    this phase runs.

    The phase performs three jobs:

    1. Records bookkeeping data on the class: '__ez_fields__'
       (the ordered name-to-'EZField' mapping) and '__key_args__'
       (the class keyword arguments captured at '__prepare__'
       time).

    2. Resolves the three build-option flags ('__is_frozen__',
       '__is_ordered__', '__kw_only__') from the class keyword
       arguments via 'parseKwargs', accepting any of the synonyms
       listed in the corresponding '__*_keys__' tuple. The first
       synonym present in the kwargs wins; the resolved value is
       truthy-coerced. Each flag defaults to 'False' when none
       of its synonyms is present.

    3. Installs the auto-generated dunder methods. '__slots__',
       '__match_args__', '__init__', '__iter__', '__eq__', and
       '__delattr__' are installed unconditionally;
       '__match_args__' is the empty tuple for keyword-only
       classes, since those have no positional construction
       shape and so no positional pattern can bind. '__delattr__'
       always raises because the EZData contract guarantees every
       declared field carries a value of the declared type;
       deletion would break the guarantee. Frozen classes also
       receive '__hash__' and '__setattr__'; non-frozen classes
       get '__hash__' set to 'None' so the interpreter rejects
       hashing. Ordered classes receive '__lt__', '__le__',
       '__gt__', and '__ge__' through 'orderingFactory';
       non-ordered classes get those four dunders set to the
       shared '_unorderable' function, which always returns
       'NotImplemented' so the interpreter raises its standard
       TypeError for unsupported comparisons while still blocking
       inheritance of an ordered base class's ordering dunders.

    The conversion helpers 'asDict', 'asTuple', and 'replace',
    plus the display dunders '__repr__'/'__str__' and the
    '__field_pairs__' helper, are installed in 'preCompilePhase'
    so a class body can replace them with method definitions of
    the same name. The reserved-name guard in
    'EZSpace.registerEZField' prevents the same names from being
    used as fields.

    Parameters
    ----------
    compiledSpace : dict
      The class namespace assembled so far. Mutated in place.

    Returns
    -------
    dict
      'compiledSpace', with the entries described above set.
    """
    ezFields = self.space.getFields()
    kwargs = self.space.getKwargs()
    compiledSpace['__ez_fields__'] = ezFields
    compiledSpace['__key_args__'] = {**kwargs, }

    isFrozen, _ = self.parseKwargs(*self.__frozen_keys__, **kwargs)
    isOrdered, _ = self.parseKwargs(*self.__ordered_keys__, **kwargs)
    isKwOnly, _ = self.parseKwargs(*self.__kw_only_keys__, **kwargs)
    compiledSpace['__is_frozen__'] = True if isFrozen else False
    compiledSpace['__is_ordered__'] = True if isOrdered else False
    compiledSpace['__kw_only__'] = True if isKwOnly else False

    compiledSpace['__slots__'] = self.slotsFactory(ezFields)
    compiledSpace['__match_args__'] = self.matchArgsFactory(
      ezFields, compiledSpace['__kw_only__']
    )
    compiledSpace['__init__'] = self.initFactory(ezFields)
    compiledSpace['__iter__'] = self.iterFactory()
    compiledSpace['__eq__'] = self.eqFactory()
    compiledSpace['__delattr__'] = self.badDelAttrFactory()
    if compiledSpace['__is_frozen__']:
      compiledSpace['__hash__'] = self.hashFactory()
      compiledSpace['__setattr__'] = self.badSetAttrFactory()
      compiledSpace['__copy__'] = self.copyFactory()
      compiledSpace['__deepcopy__'] = self.deepCopyFactory()
    else:
      compiledSpace['__hash__'] = None
    if compiledSpace['__is_ordered__']:
      compiledSpace['__lt__'] = self.orderingFactory(operator.lt)
      compiledSpace['__le__'] = self.orderingFactory(operator.le)
      compiledSpace['__gt__'] = self.orderingFactory(operator.gt)
      compiledSpace['__ge__'] = self.orderingFactory(operator.ge)
    else:
      compiledSpace['__lt__'] = _unorderable
      compiledSpace['__le__'] = _unorderable
      compiledSpace['__gt__'] = _unorderable
      compiledSpace['__ge__'] = _unorderable
    return compiledSpace

  @classmethod
  def slotsFactory(cls, ezFields: dict[str, EZField]) -> tuple[str, ...]:
    """
    Computes the '__slots__' tuple for the 'EZData' subclass under
    construction. Returns the field names in declaration order,
    including any inherited from EZData base classes, so 'dir(cls)'
    and 'cls.__slots__' present the full field surface in one
    tuple without forcing the caller to walk the MRO.

    Parameters
    ----------
    ezFields : dict[str, EZField]
      The ordered name-to-'EZField' mapping for this class,
      assembled by 'EZSpace.getFields'.

    Returns
    -------
    tuple[str, ...]
      The '__slots__' tuple for the class under construction.
    """
    slotNames = []
    for key, field in ezFields.items():
      slotNames.append(key)
    return (*slotNames,)

  @classmethod
  def matchArgsFactory(
      cls,
      ezFields: dict[str, EZField],
      isKwOnly: bool,
  ) -> tuple[str, ...]:
    """
    Computes the '__match_args__' tuple for the 'EZData' subclass
    under construction. Returns the field names in declaration
    order, or an empty tuple when the class is keyword-only and
    therefore not constructible by a positional pattern. Mirrors
    the behavior of 'dataclasses.dataclass' for the 'kw_only'
    flag: keyword-only fields are excluded from '__match_args__'
    so 'case Cls(a, b):' patterns do not bind against them.

    Parameters
    ----------
    ezFields : dict[str, EZField]
      The ordered name-to-'EZField' mapping for this class.
    isKwOnly : bool
      The resolved '__kw_only__' flag from the class keyword
      arguments.

    Returns
    -------
    tuple[str, ...]
      The '__match_args__' tuple. Empty when 'isKwOnly' is True.
    """
    if isKwOnly:
      return ()
    return (*ezFields,)

  @classmethod
  def initFactory(cls, ezFields: dict) -> INIT:
    """
    Creates the '__init__' method for the 'EZData' subclass under
    construction. When 'kwOnly' is False, the returned '__init__'
    assigns positional arguments to the fields in declaration order,
    then assigns keyword arguments by name, overriding any positional
    value given for the same field. When 'kwOnly' is True, the
    '__init__' rejects positional arguments and every field is set by
    keyword. Either way, every field still left unset finally receives
    its default value.

    Field metadata is resolved once, here at class creation: each
    field's type and a fresh-default recipe are captured so the
    per-construct path never reads them back through an 'EZField'
    descriptor. The recipe still builds a new value on every call, so
    mutable defaults stay unshared between instances.

    After every field has been populated, the generated '__init__'
    looks up '__post_init__' on 'type(self)' and calls it with
    'self' if it is defined. The lookup walks the MRO, so a
    subclass that does not define its own '__post_init__' still
    inherits the parent's. The hook is the supported customization
    point for validation, normalization, and derived state.

    Parameters
    ----------
    ezFields : dict[str, EZField]
      The class's merged own and inherited fields, in declaration
      order.

    Returns
    -------
    INIT: (self, *args, **kwargs) -> None
      The '__init__' method for the 'EZData' subclass under construction.
    """
    specs = []
    for key, field in ezFields.items():
      fieldType = field.fieldType
      posArgs = field.posArgs
      keyArgs = field.keyArgs

      def makeDefault(t=fieldType, a=posArgs, k=keyArgs) -> Any:
        return t(*a, **k)

      specs.append((key, fieldType, makeDefault))
    specs = (*specs,)
    fieldCount = len(specs)

    def _assignField(self: Any, key: str, val: Any, type_: type) -> None:
      try:
        casted = typeCast(type_, val)
      except TypeCastException as typeCastException:
        e = TypeException(key, val, type_)
        raise e from typeCastException
      else:
        object.__setattr__(self, key, casted)

    def _applyKwargs(self: Any, **kwargs) -> None:
      for key, type_, _ in specs:
        if key in kwargs:
          _assignField(self, key, kwargs[key], type_)

    def _applyArgs(self: Any, *args) -> None:
      if len(args) > fieldCount:
        raise ExtraPositionalException(type(self), fieldCount, len(args))
      for (key, type_, _), arg in zip(specs, args):
        _assignField(self, key, arg, type_)

    def _applyDefaults(self: Any) -> None:
      for key, _, makeDefault in specs:
        try:
          _ = getattr(self, key)
        except AttributeError:
          object.__setattr__(self, key, makeDefault())

    def __init__(self: Any, *args, **kwargs) -> None:
      if not self.__kw_only__:
        _applyArgs(self, *args)
      elif args:
        raise KwargsOnlyException(type(self), len(args))
      _applyKwargs(self, **kwargs)
      _applyDefaults(self)
      postInit = getattr(type(self), '__post_init__', None)
      if postInit is not None:
        postInit(self)

    return __init__

  @classmethod
  def iterFactory(cls, ) -> ITER:
    """
    Creates the '__iter__' method for the 'EZData' subclass under
    construction. The returned '__iter__' yields the field values
    in declaration order, so 'tuple(instance)' produces the same
    sequence as 'instance.asTuple()' and 'list(instance)' yields
    each field value once.

    Returns
    -------
    ITER: (self) -> Iterator
      Spells out to 'Callable[..., Iterator]'. The '__iter__'
      method for the 'EZData' subclass under construction.
    """

    def __iter__(self: Any) -> Iterator:
      for name, desc in self.__ez_fields__.items():
        yield getattr(self, name)

    return __iter__

  @classmethod
  def asDictFactory(cls, ) -> Callable[..., dict]:
    """
    Creates the 'asDict' method for the 'EZData' subclass under
    construction. The returned method returns a dict mapping each
    field name to its current value, in declaration order. The
    dict is a fresh object on every call, so the caller may
    mutate it freely without affecting the instance.

    Returns
    -------
    Callable[..., dict]: (self) -> dict
      The 'asDict' method for the 'EZData' subclass under
      construction.
    """

    def asDict(self: Any) -> dict:
      return {name: getattr(self, name) for name in self.__ez_fields__}

    return asDict

  @classmethod
  def asTupleFactory(cls, ) -> Callable[..., tuple]:
    """
    Creates the 'asTuple' method for the 'EZData' subclass under
    construction. The returned method returns a tuple of the
    field values in declaration order. Equivalent to
    'tuple(instance)' but spelled as a method, mirroring 'asDict'
    and offering a named accessor for callers who prefer one.

    Returns
    -------
    Callable[..., tuple]: (self) -> tuple
      The 'asTuple' method for the 'EZData' subclass under
      construction.
    """

    def asTuple(self: Any) -> tuple:
      return (*self,)

    return asTuple

  @classmethod
  def replaceFactory(cls, ) -> Callable[..., Any]:
    """
    Creates the 'replace' method for the 'EZData' subclass under
    construction. The returned method returns a new instance of
    the same class with the named fields overridden by the
    keyword arguments and every other field copied from 'self'.
    Mirrors 'dataclasses.replace' and is the canonical way to
    derive a modified copy of a frozen instance.

    Unlike the generated '__init__' (which silently ignores
    kwargs not matching any field, to support orthogonal kwarg
    injection in multi-base classes), 'replace' raises
    'TypeError' on any keyword that is not the name of a
    declared field. The user's intent with 'replace' is always
    'modify this field', so an unrecognized name is a mistake
    rather than a deliberate forward.

    Returns
    -------
    Callable[..., Any]: (self, **changes) -> Self
      The 'replace' method for the 'EZData' subclass under
      construction.
    """

    def replace(self: Any, **changes) -> Any:
      fields = self.__ez_fields__
      unknown = [k for k in changes if k not in fields]
      if unknown:
        infoSpec = (
          "replace() got unexpected field name(s) %s for "
          "EZData class '%s'. Known fields: %s."
        )
        names = ', '.join(repr(k) for k in unknown)
        known = ', '.join(repr(k) for k in fields)
        clsName = type(self).__name__
        raise TypeError(infoSpec % (names, clsName, known))
      return type(self)(**{**self.asDict(), **changes})

    return replace

  @classmethod
  def fieldPairsFactory(cls, ) -> Callable[..., list[str]]:
    """
    Creates the '__field_pairs__' method for the 'EZData' subclass
    under construction. The returned method returns a list of
    'name=value' strings, one per field, in declaration order. It
    is consumed by the generated '__str__' and '__repr__', so a
    subclass can customize field rendering by overriding
    '__field_pairs__' alone.

    Returns
    -------
    Callable[..., list[str]]: (self) -> list[str]
      The '__field_pairs__' method for the 'EZData' subclass under
      construction.
    """

    def __field_pairs__(self: Any) -> list[str]:
      pairs = []
      for key, value in self.__ez_fields__.items():
        pairs.append('%s=%r' % (key, getattr(self, key)))
      return pairs

    return __field_pairs__

  @classmethod
  def strFactory(cls, ) -> Callable[..., str]:
    """
    Creates the '__str__' method for the 'EZData' subclass under
    construction. The returned '__str__' renders the class name
    and each field as 'name=value' inside angle brackets, in
    declaration order. The 'name=value' rendering is delegated to
    '__field_pairs__' so subclasses can customize display by
    overriding that helper alone.

    Returns
    -------
    Callable[..., str]: (self) -> str
      The '__str__' method for the 'EZData' subclass under
      construction.
    """

    def __str__(self: Any) -> str:
      infoSpec = """<%s: %s>"""
      fieldValues = str.join(', ', self.__field_pairs__())
      clsName = type(self).__name__
      return infoSpec % (clsName, fieldValues)

    return __str__

  @classmethod
  def reprFactory(cls, ) -> Callable[..., str]:
    """
    Creates the '__repr__' method for the 'EZData' subclass under
    construction. The returned '__repr__' produces a string that
    reconstructs an equal instance when passed to the class. For
    non-keyword-only classes it emits the field values as
    positional arguments ('Foo(3.0, 4.0)'); for keyword-only
    classes it emits 'name=value' pairs through '__field_pairs__'
    ('Foo(x=3.0, y=4.0)'). Both forms match the call shape the
    class accepts.

    Returns
    -------
    Callable[..., str]: (self) -> str
      The '__repr__' method for the 'EZData' subclass under
      construction.
    """

    def __repr__(self: Any) -> str:
      infoSpec = '%s(%s)'
      clsName = type(self).__name__
      if self.__kw_only__:
        fieldValues = str.join(', ', self.__field_pairs__())
      else:
        fieldValues = str.join(', ', [repr(value) for value in self])
      return infoSpec % (clsName, fieldValues)

    return __repr__

  @classmethod
  def eqFactory(cls, ) -> Callable[..., bool]:
    """
    Creates the '__eq__' method for the 'EZData' subclass under
    construction. The returned '__eq__' yields 'NotImplemented' when
    'other' is not an 'EZData' instance, 'False' when it is one but
    not congruent, and otherwise compares the fields value by value.

    Returns
    -------
    Callable[..., bool]: (self, other) -> bool
      The '__eq__' method for the 'EZData' subclass under construction.
    """

    def __eq__(self: Any, other: Any) -> bool:
      selfCls, otherCls = type(self), type(other)
      if not isinstance(otherCls, type(selfCls)):
        return NotImplemented
      if not selfCls.isCongruent(otherCls):
        return False
      selfValues = (*self,)
      otherValues = (*other,)
      return True if selfValues == otherValues else False

    return __eq__

  @classmethod
  def hashFactory(cls, ) -> Callable[..., int]:
    """
    Creates the '__hash__' method for the 'EZData' subclass under
    construction. The returned '__hash__' hashes the tuple of
    field values in declaration order, so two equal instances of
    a frozen class have equal hashes. Only installed on frozen
    classes; non-frozen classes set '__hash__' to 'None' so the
    interpreter rejects 'hash(instance)'.

    Returns
    -------
    Callable[..., int]: (self) -> int
      The '__hash__' method for the frozen 'EZData' subclass
      under construction.
    """

    def __hash__(self: Any) -> int:
      return hash((*self,))

    return __hash__

  @classmethod
  def orderingFactory(cls, op: Callable[..., bool]) -> Callable[..., bool]:
    """
    Creates an ordering dunder method for the 'EZData' subclass under
    construction. The returned function compares the tuple of field
    values against another instance of the same class using the
    supplied binary operator.

    Parameters
    ----------
    op : Callable[..., bool]
      A binary operator from the standard 'operator' module, such as
      'operator.lt', 'operator.le', 'operator.gt', or 'operator.ge'.
      It is applied to the field-value tuples of 'self' and 'other'.

    Returns
    -------
    Callable[..., bool]: (self, other) -> bool
      The ordering dunder method for the 'EZData' subclass under
      construction. Its '__name__' is set to '__<op>__' so that
      tracebacks and introspection report the operator name.
    """

    def __ordering__(self: Any, other: Any) -> bool:
      if type(other) is not type(self):
        return NotImplemented
      selfValues = (*self,)
      otherValues = (*other,)
      return True if op(selfValues, otherValues) else False

    __ordering__.__name__ = '__%s__' % op.__name__
    __ordering__.__qualname__ = __ordering__.__name__
    return __ordering__

  @classmethod
  def badSetAttrFactory(cls, ) -> INIT:
    """
    Creates the '__setattr__' method for a frozen 'EZData' subclass.
    The returned '__setattr__' raises 'AttributeError' on every
    assignment, so instances are immutable once constructed. The
    generated '__init__' populates the fields through
    'object.__setattr__' and is therefore unaffected.

    Returns
    -------
    INIT: (self, key, value) -> None
      The '__setattr__' method for the frozen 'EZData' subclass.
    """

    # noinspection PyUnusedLocal
    def __setattr__(self: Any, key: str, value: Any) -> None:
      clsName = type(self).__name__
      infoSpec = """'%s' is frozen; cannot assign to attribute '%s'!"""
      raise AttributeError(infoSpec % (clsName, key))

    return __setattr__

  @classmethod
  def badDelAttrFactory(cls, ) -> INIT:
    """
    Creates the '__delattr__' method installed on every 'EZData'
    subclass, frozen or not. The returned '__delattr__' raises
    'AttributeError' on every deletion, since the EZData contract
    is 'every declared field always holds a value of the declared
    type'; deleting a field would leave the instance in a state
    that violates the type guarantee.

    Returns
    -------
    INIT: (self, key) -> None
      The '__delattr__' method for the 'EZData' subclass.
    """

    def __delattr__(self: Any, key: str) -> None:
      clsName = type(self).__name__
      infoSpec = """EZData class '%s' does not allow deleting
      attribute '%s'."""
      raise AttributeError(textFmt(infoSpec % (clsName, key)))

    return __delattr__

  @classmethod
  def copyFactory(cls, ) -> Callable[..., Any]:
    """
    Creates the '__copy__' method for a frozen 'EZData' subclass. A
    frozen class rejects every assignment through its generated
    '__setattr__', so the default 'copy.copy' reconstruction (build a
    blank instance, then set each slot) raises. The returned '__copy__'
    instead builds a fresh instance and writes the field values straight
    through 'object.__setattr__', the same bypass '__init__' uses, so a
    frozen instance copies as a faithful shallow clone.

    Returns
    -------
    Callable[..., Any]: (self) -> Self
      The '__copy__' method for the frozen 'EZData' subclass.
    """

    def __copy__(self: Any) -> Any:
      newSelf = type(self).__new__(type(self))
      for name in self.__ez_fields__:
        object.__setattr__(newSelf, name, getattr(self, name))
      return newSelf

    return __copy__

  @classmethod
  def deepCopyFactory(cls, ) -> Callable[..., Any]:
    """
    Creates the '__deepcopy__' method for a frozen 'EZData' subclass,
    the deep counterpart of 'copyFactory'. Each field value is deep
    copied (threading the 'memo' dict so shared and cyclic references
    are preserved) and written through 'object.__setattr__' to sidestep
    the frozen guard. The new instance is registered in 'memo' before
    its fields are filled, so a value that refers back to the instance
    resolves to the same clone.

    Returns
    -------
    Callable[..., Any]: (self, memo) -> Self
      The '__deepcopy__' method for the frozen 'EZData' subclass.
    """

    def __deepcopy__(self: Any, memo: Any) -> Any:
      newSelf = type(self).__new__(type(self))
      memo[id(self)] = newSelf
      for name in self.__ez_fields__:
        value = deepcopy(getattr(self, name), memo)
        object.__setattr__(newSelf, name, value)
      return newSelf

    return __deepcopy__
