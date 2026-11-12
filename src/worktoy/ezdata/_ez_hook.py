"""
EZHook is the namespace hook that builds the 'EZData' methods from its
declared fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import operator
from collections.abc import Callable
from types import FunctionType, BuiltinFunctionType
from typing import TYPE_CHECKING

from . import EZField, EZStore
from ..core import Object
from ..mcls.space_hooks import AbstractSpaceHook, ReservedNames
from ..utilities import typeCast, textFmt
from ..waitaminute import TypeException
from ..waitaminute.dispatch import TypeCastException
from ..waitaminute.ezdata import ExtraPositionalException, \
  KwargsOnlyException, IncompleteFieldException, ClassFieldError, \
  ReservedMethodError, ExtraKeywordException, \
  RepeatedFieldException, ReservedAttributeError, DuplicateError

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, TypeAlias, Iterator
  from . import EZSpace

  Keys: TypeAlias = tuple[str, ...]

  INIT: TypeAlias = Callable[..., None]
  ITER: TypeAlias = Callable[..., Iterator]
  SETATTR: TypeAlias = Callable[..., None]
  DELATTR: TypeAlias = Callable[..., None]


def _unorderable(self: Any, other: Any) -> Any:
  """
  A dataclass that is not ordered must refuse '<' and its kin as a plain
  class does, with the interpreter's own 'TypeError', and a class
  declared 'ordered=False' below an ordered one must stop comparing
  although its base does.

  Implementation
  --------------

  One function stands at '__lt__', '__le__', '__gt__' and '__ge__' of
  every unordered 'EZData' subclass. It returns 'NotImplemented', so the
  interpreter raises its standard 'TypeError' for an unsupported
  comparison, and at those four names it shadows the ordering methods of
  an ordered base.
  """
  return NotImplemented


class EZHook(AbstractSpaceHook):
  """
  A dataclass is made from its class body: the fields the body declares
  become the constructor, the equality, the iteration and the conversions
  of the class. Something must watch the body as it runs, take each field
  as it is bound, refuse at its line what a dataclass body may not hold,
  and write the methods the class is owed once the body has ended. A
  project building a dataclass base of its own must be able to change
  that work, another spelling of an option or another generated method,
  without writing all of it again.

  Implementation
  --------------

  'EZHook' is the namespace hook of 'EZSpace'. 'setItemPhase' claims
  every field of the body, an 'EZField' once '_assertCompleteField' has
  passed it and a plain value wrapped by 'EZField.fromValue', and refuses
  the names EZData keeps for itself. 'postCompilePhase' resolves the
  options, settles the optional names and installs the generated methods.
  Every method is made by a factory that is a classmethod of the hook,
  not a file of its own.

  The generated names come in two kinds. The reserved methods, such as
  '__init__' and '__iter__', are installed on every class; an EZData
  class body may not define them, and a plain base may, but gives way.
  The optional names, '__field_pairs__', 'asDict', 'asTuple', 'replace',
  '__repr__', '__str__' and '__match_args__', are generated only where
  neither the class body nor a base supplies one, an EZData base and a
  plain base alike; see '_settleOptional'.

  The three build options are read from the class keywords under the
  spellings of '__frozen_keys__', '__ordered_keys__' and
  '__kw_only_keys__'; 'parseKwargs', inherited from 'Object', picks the
  first spelling present. A subclass of 'EZHook' can extend these to
  accept additional spellings. A project declares such a subclass in the
  body of a subclass of 'EZSpace', at a name of its own, since a
  namespace cannot replace a hook it inherits. The hook declared last
  then acts alone, and the one the namespace inherits stands down; see
  '__set_name__' and '_standsDown'.

  Attributes
  ----------

  __frozen_keys__ : tuple[str, ...]
    The spellings of the class keyword that freezes a class.

  __ordered_keys__ : tuple[str, ...]
    The spellings of the class keyword that orders a class.

  __kw_only_keys__ : tuple[str, ...]
    The spellings of the class keyword that makes a class keyword-only.

  __installed__ : tuple[str, ...]
    The methods 'postCompilePhase' installs on every class.

  reservedNames : tuple[str, ...]
    The names the interpreter writes into a class body on its own; see
    'ReservedNames'.

  __ez_acting_hook__ : EZHook
    Set on the namespace class a hook of this kind is declared in: the
    hook that acts for the class bodies run in that namespace.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Annotations
  if TYPE_CHECKING:  # pragma: no cover, no mutate
    space: EZSpace

  #  Class Variables
  __frozen_keys__: Keys = ('frozen', 'immutable', 'hashable')
  __ordered_keys__: Keys = ('ordered', 'order', 'sortable', 'comparable')
  __kw_only_keys__: Keys = ('kwOnly', 'keywordOnly', 'kw_only')
  #  The methods 'postCompilePhase' installs on every class.
  __installed__: Keys = (
    '__init__', '__iter__', '__len__', '__eq__', '__hash__', '__lt__',
    '__le__', '__gt__', '__ge__', '__setattr__', '__delattr__',
  )

  #  Public Variables
  reservedNames = ReservedNames()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    A project building a dataclass base of its own changes what the hook
    does by declaring a subclass of it in the body of a subclass of
    'EZSpace'. A namespace class cannot replace a hook it inherits, so
    the subclass is declared at a name of its own, and the namespace then
    holds two hooks of this kind. Only one of them may claim the fields
    and settle the generated names of a class body: two in turn would
    each undo part of what the other did.

    Implementation
    --------------

    The hook registers as every hook does, then records itself on the
    namespace class under '__ez_acting_hook__'. A subclass of that
    namespace class declaring no hook of this kind inherits the record.
    '_standsDown' reads it at the start of each phase.

    Parameters
    ----------

    owner : type
      The namespace class the hook is declared in.

    name : str
      The name it is declared at.
    """
    AbstractSpaceHook.__set_name__(self, owner, name, **kwargs)
    setattr(owner, '__ez_acting_hook__', self)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _standsDown(self) -> bool:
    """
    A namespace may hold several hooks of this kind, the one it inherits
    from 'EZSpace' and one a project declared in a subclass, and each
    phase of a class body must be the work of one of them alone.

    Implementation
    --------------

    The hook acts when the class of the namespace recorded it as the
    acting one, as '__set_name__' does for the hook declared last, and
    stands down otherwise.

    Returns
    -------

    bool
      Whether another hook acts for the namespace.
    """
    try:
      acting = type.__getattribute__(type(self.space), '__ez_acting_hook__')
    except AttributeError:
      #  This branch is reached by the following:
      #  - The hook was registered with 'addHook' by hand, on a namespace
      #    class whose body declares no hook of this kind, so nothing was
      #    recorded and no other hook could act
      return False
    return False if acting is self else True

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    Every binding of a dataclass body must be sorted as it is made: a field
    is taken for the class, a method or a descriptor is left where it is,
    and what a dataclass body may not hold is refused at its line, where
    the traceback points at the mistake.

    Implementation
    --------------

    A hook standing down for another answers 'False' at once; see
    '_standsDown'. Otherwise, in order: a method EZData generates and keeps
    for itself, listed in 'EZSpace.__reserved_ez_methods__', and an
    attribute EZData sets on every class itself, listed in
    'EZSpace.__reserved_ez_attributes__', may not be bound at all. The
    names the interpreter writes into a class body on its own, listed by
    'ReservedNames', pass through untouched. An 'EZField' is registered
    through 'EZSpace.registerEZField' once '_assertCompleteField' has
    passed it. A function, written in Python or a builtin such as 'len',
    falls through to the namespace, as does a descriptor, an 'Alias' of a
    method among them; an 'Alias' of a field is refused by the core, since
    no class holds the name. Either is refused first at the name of a
    field of the class, own or inherited; see '_refuseAtFieldName'. A
    class object is refused, since it would become a field of type
    'type', and so is a bare 'None', since no field type can be taken from
    it. Any other value is wrapped by 'EZField.fromValue' and registered.

    Parameters
    ----------

    key : str
      The name bound in the class body.

    val : Any
      The value bound to it.

    old : Any, optional
      The value the name held before, which the namespace passes to every
      hook. Unused here.

    Returns
    -------

    bool
      'True' when the hook has taken the binding and the namespace is not
      to store it; 'False' when the namespace stores it, which is also the
      answer of a hook standing down for another.

    Raises
    ------

    IncompleteFieldException
      The 'EZField' at 'key' lacks its type or its arguments, or a bare
      'None' was bound, leaving no type to take. Raised before the field is
      registered, so the traceback points at the line of the class body.

    ReservedFieldError
      A field is bound at a name reserved for a method of the class, such
      as 'asDict' or '__post_init__'. Raised by 'EZSpace.registerEZField'.

    DuplicateError
      A field is bound twice in the body, or at the name of a method or
      a descriptor of the body; raised by 'EZSpace.registerEZField'. Or a
      method or a descriptor is bound at the name of a field of the class,
      own or inherited; raised by '_refuseAtFieldName'.

    ClassFieldError
      'val' is a class object, bound by a nested class statement or by an
      assignment such as 'kind = int'.

    ReservedMethodError
      'key' names a method EZData generates and keeps for itself, such as
      '__setattr__'.

    ReservedAttributeError
      'key' names an attribute EZData keeps for itself, such as
      '__kw_only__'.
    """
    if self._standsDown():
      return False
    if key in self.space.__reserved_ez_methods__:
      raise ReservedMethodError(key, self.space)
    if key in self.space.__reserved_ez_attributes__:
      raise ReservedAttributeError(key, self.space)
    if key in self.reservedNames:
      return False
    if isinstance(val, EZField):
      self._assertCompleteField(key, val)
      self.space.registerEZField(key, val)
      return True
    if isinstance(val, (FunctionType, BuiltinFunctionType)):
      self._refuseAtFieldName(key)
      return False
    if isinstance(val, type):
      raise ClassFieldError(self.space.getClassName(), key, val)
    if self._isDescriptor(val):
      self._refuseAtFieldName(key)
      return False
    if val is None:
      clsName = self.space.getClassName()
      missing = 'a bare None default cannot infer a field type'
      raise IncompleteFieldException(clsName, key, missing)
    # noinspection PyTypeChecker
    valField = EZField.fromValue(val)
    self.space.registerEZField(key, valField)
    return True

  def _refuseAtFieldName(self, key: str) -> None:
    """
    A body that binds a method or a descriptor at the name of a field of
    its class, one it declared itself or one the class inherits, declares
    two things at one name, and the class would keep both: the field in
    every instance, the other on the class. An instance then hides the
    method behind the value of the field, a property at the name refuses
    the value the constructor stores, and a box or a property with a
    setter takes that value and loses it again to the default, so every
    instance holds the default whatever it was given. The line binding
    the method or the descriptor must fail instead, as a field bound
    twice does. A subclass that declares the name again as a field is
    not meant: it gives the inherited field a new default or type.

    Implementation
    --------------

    A name among the fields of the class, own and inherited, raises
    'DuplicateError'. 'setItemPhase' asks before it lets a function or a
    descriptor through to the namespace. The other order in one body, a
    field bound at a name the namespace stores, is refused by
    'EZSpace.registerEZField'.

    Parameters
    ----------

    key : str
      The name bound in the class body.

    Raises
    ------

    DuplicateError
      'key' is a field of the class, declared in the body before or
      inherited.
    """
    if key in self.space.getFields():
      raise DuplicateError(key, self.space)

  @staticmethod
  def _isDescriptor(value: Any) -> bool:
    """
    A value bound in a dataclass body is either a part of the class, left
    in place as a class attribute, or a default, which becomes a field, and
    the hook must tell the two apart. A descriptor is a part of the class.
    But every 'Object' has the three methods of a descriptor, and most are
    meant as values: an EZData instance or a 'SymbolicName' in a body is a
    default, while an 'Alias' or a box is a part of the class.

    Implementation
    --------------

    A value that is no 'Object' is a descriptor when its type defines
    '__get__', '__set__' or '__delete__', which is how Python tells a
    descriptor. Every 'Object' defines all three, EZData instances and
    'SymbolicName' included, so an 'Object' is a descriptor only when its
    type overrides one of them, as 'Alias', 'Dispatcher' and a descriptor a
    project writes directly do, or one of '__instance_get__',
    '__instance_set__' and '__instance_delete__', where a descriptor built
    on 'Object' the documented way does its work. Each name is read off the
    type with 'type.__getattribute__', past any '__class_getattr__' of a
    worktoy class, and compared with what 'Object' holds by identity.

    Parameters
    ----------

    value : Any
      The value bound in the class body.

    Returns
    -------

    bool
      Whether the value stays a class attribute.
    """
    valueType = type(value)
    if isinstance(value, Object):
      return EZHook._overridesObjectProtocol(valueType)
    for name in ('__get__', '__set__', '__delete__'):
      if EZHook._typeDefines(valueType, name):
        return True
    return False

  @staticmethod
  def _overridesObjectProtocol(valueType: type) -> bool:
    """
    An 'Object' serves as a descriptor through six methods, and a class
    based on 'Object' is a descriptor class exactly when it overrides one
    of them; see '_isDescriptor'.

    Implementation
    --------------

    '__get__', '__set__', '__delete__', '__instance_get__',
    '__instance_set__' and '__instance_delete__' are each read off the
    class and off 'Object' with 'type.__getattribute__' and compared by
    identity.

    Parameters
    ----------

    valueType : type
      A class based on 'Object'.

    Returns
    -------

    bool
      Whether the class overrides one of the six.
    """
    names = (
      '__get__',
      '__set__',
      '__delete__',
      '__instance_get__',
      '__instance_set__',
      '__instance_delete__',
    )
    for name in names:
      own = type.__getattribute__(valueType, name)
      base = type.__getattribute__(Object, name)
      if own is not base:
        return True
    return False

  @staticmethod
  def _typeDefines(valueType: type, name: str) -> bool:
    """
    Whether a class holds a name must be asked of the class itself, since a
    metaclass with a '__getattr__' answers for names its classes lack.

    Implementation
    --------------

    'type.__getattribute__' walks the resolution order of the class and
    raises 'AttributeError' for a name no class along it holds.

    Parameters
    ----------

    valueType : type
      The class asked.

    name : str
      The name.

    Returns
    -------

    bool
      Whether a class along the resolution order holds the name.
    """
    try:
      type.__getattribute__(valueType, name)
    except AttributeError:
      return False
    return True

  def _assertCompleteField(self, key: str, field: EZField) -> None:
    """
    A field without a type, 'EZField(1)', or without its parentheses,
    'EZField[int]', is valid Python and cannot supply a default. The class
    body must fail at the line binding it, rather than when the class is
    compiled or first instantiated. A field of a subclass of 'EZField'
    can lack its arguments with the parentheses written out, when the
    '__init__' of the subclass does not hand them on, and the refusal
    must then point at that '__init__' as well.

    Implementation
    --------------

    A field whose '__field_type__' is 'None', or whose '__pos_args__' and
    '__key_args__' are both 'None', raises 'IncompleteFieldException'
    saying which half is missing. For a field whose class is not
    'EZField' itself, the text for missing arguments names the class of
    the field and its '__init__' as the other possible cause.

    Parameters
    ----------

    key : str
      The name the field is bound to in the class body.

    field : EZField
      The field.

    Raises
    ------

    IncompleteFieldException
      The field has no type, or was never called.
    """
    clsName = self.space.getClassName()
    if field.__field_type__ is None:
      missing = 'no field type was set'
      raise IncompleteFieldException(clsName, key, missing)
    noPos = field.__pos_args__ is None
    noKey = field.__key_args__ is None
    if noPos and noKey:
      if type(field) is EZField:
        missing = 'no construction arguments were given'
      else:
        infoSpec = """no construction arguments were given, or the
        '__init__' of '%s' did not hand them on to 'EZField.__init__'"""
        missing = textFmt(infoSpec % type(field).__name__)
      raise IncompleteFieldException(clsName, key, missing)

  def _optionalFactories(
      self,
      ezFields: dict[str, EZField],
      isKwOnly: bool,
  ) -> dict[str, Callable[[], Any]]:
    """
    The optional names are generated only where a class has none, so each
    needs a way to be made on demand, and a subclass of the hook must be
    able to add a name or make one differently.

    Implementation
    --------------

    A dict from each optional name to a callable that generates it:
    '__field_pairs__', 'asDict', 'asTuple', 'replace', '__repr__',
    '__str__' and '__match_args__'. The last needs the fields and the
    keyword-only option, which its callable closes over.

    Parameters
    ----------

    ezFields : dict[str, EZField]
      The fields of the class, in declaration order.

    isKwOnly : bool
      Whether the class is keyword-only.

    Returns
    -------

    dict[str, Callable[[], Any]]
      The factory of each optional name.
    """
    return {
      '__field_pairs__': self.fieldPairsFactory,
      'asDict'         : self.asDictFactory,
      'asTuple'        : self.asTupleFactory,
      'replace'        : self.replaceFactory,
      '__repr__'       : self.reprFactory,
      '__str__'        : self.strFactory,
      '__match_args__' : lambda: self.matchArgsFactory(ezFields, isKwOnly),
    }

  @staticmethod
  def _findHandWritten(name: str, lookupOrder: list[type]) -> tuple:
    """
    An optional name a base wrote by hand must win over one EZData
    generated, whichever base holds it, a dataclass or a plain mixin.
    Python's own lookup cannot decide that: a generated method on a nearer
    class would hide a hand-written one on a farther class.

    Implementation
    --------------

    The first class along 'lookupOrder' holding 'name' in its own
    dictionary as something EZData did not generate answers. 'object' is
    skipped, whose defaults such as '__repr__' are no one's choice, and so
    are the names an EZData class lists in its '__ez_generated__'.

    Parameters
    ----------

    name : str
      The optional name.

    lookupOrder : list[type]
      The classes after the class under construction in its resolution
      order.

    Returns
    -------

    tuple[bool, Any]
      '(True, value)' for the hand-written value found, or
      '(False, None)' when the bases supply none.
    """
    for klass in lookupOrder:
      if klass is object:
        continue
      own = vars(klass)
      if name not in own:
        continue
      try:
        generated = own['__ez_generated__']
      except KeyError:
        #  This branch is reached by the following:
        #  - The class is a plain base, built by no 'EZMeta', so it lists
        #    no generated names and everything it holds is hand-written
        generated = ()
      if name in generated:
        continue
      return True, own[name]
    return False, None

  @classmethod
  def _settleOptional(
      cls,
      compiledSpace: dict,
      factories: dict[str, Callable[[], Any]],
      lookupOrder: list[type],
  ) -> frozenset:
    """
    Each optional name of a class under construction must end up as one
    thing: what the class body wrote, else what a base wrote by hand, else
    what EZData generates. And the class must remember which names were
    generated for it, so that its subclasses look past them.

    Implementation
    --------------

    A name already in 'compiledSpace' is left as it is, the body's own
    definition or the 'Dispatcher' its '@overload' declarations built.
    Failing that, the first hand-written one along the bases is installed
    on the class itself. Failing that, the factory is called and the name
    recorded.

    Parameters
    ----------

    compiledSpace : dict
      The dictionary the class is created from, changed in place.

    factories : dict[str, Callable[[], Any]]
      The factory of each optional name.

    lookupOrder : list[type]
      The classes after the class under construction in its resolution
      order.

    Returns
    -------

    frozenset[str]
      The names EZData generated, which the class records in
      '__ez_generated__'.
    """
    generated = []
    for name, factory in factories.items():
      if name in compiledSpace:
        continue
      found, value = cls._findHandWritten(name, lookupOrder)
      if found:
        compiledSpace[name] = value
        continue
      compiledSpace[name] = factory()
      generated.append(name)
    return frozenset(generated)

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    """
    Once the class body has ended and its names are merged into the
    dictionary the class is created from, the class must receive what a
    dataclass is owed: its fields on record, its options resolved, the
    optional names settled and the generated methods installed, each named
    after the class as a method written in its body is. The shapes of the
    fields were checked as the body ran, so every field is complete by now.

    Implementation
    --------------

    A hook standing down for another returns the dictionary untouched; see
    '_standsDown'. Otherwise the phase does four jobs.

    1. It records '__ez_fields__' on the class, the ordered mapping from
       name to 'EZField'. The class keyword arguments are on the class
       already, at '__keyword_arguments__', where the namespace puts them
       for every worktoy class.

    2. It resolves the three options, '__is_frozen__', '__is_ordered__'
       and '__kw_only__', from the class keywords through 'parseKwargs',
       under any of the spellings in the '__*_keys__' tuples. The first
       spelling present wins, and its value counts by its truth. 'frozen'
       and 'kwOnly' are 'False' when none of their spellings is present;
       'ordered' is then taken from the nearest 'EZData' class along the
       resolution order through '_inheritedFlag', so the subclasses of an
       ordered class compare unless one says 'ordered=False'. A class that
       is not frozen while an 'EZData' class along its resolution order
       is, is refused through '_refuseThawing'; 'kwOnly' is per class.

    3. It settles the optional names, '__field_pairs__', 'asDict',
       'asTuple', 'replace', '__repr__', '__str__' and '__match_args__',
       through '_settleOptional': the class body's own wins, then the
       first hand-written one along the bases, then a generated one. The
       generated names are recorded in '__ez_generated__', so that a
       subclass looks past them to a hand-written one further along. The
       generated '__match_args__' is empty for a keyword-only class, which
       takes nothing by position, so no positional pattern can bind.

    4. It installs the generated methods. '__init__', '__iter__',
       '__len__', '__eq__', '__delattr__' and '__setattr__' are installed
       on the class itself, so they take precedence over a plain base
       defining any of them. Before anything else, a class body that
       overloaded one of the installed names is refused with
       'ReservedMethodError' through '_refuseOverloadedReserved', since
       the namespace claims an '@overload' binding before 'setItemPhase'
       could refuse it, and one that overloaded a method at the name of
       an inherited field with 'DuplicateError' through
       '_refuseOverloadedFields'. The '__delattr__' of a class that is
       not frozen refuses deleting a field, since every declared field
       holds a value of its type, and lets any other attribute go; that of
       a frozen class refuses every deletion. For the same reason the
       '__setattr__' of a class that is not frozen casts each field
       assignment through 'castField', while that of a frozen class
       refuses every assignment. A frozen class also receives '__hash__';
       any other has '__hash__' set to 'None', so the interpreter refuses
       hashing. An ordered class receives '__lt__', '__le__', '__gt__' and
       '__ge__' through 'orderingFactory'; any other has the four set to
       '_unorderable', which returns 'NotImplemented', so the interpreter
       raises its standard 'TypeError', and which shadows the ordering
       methods of an ordered base in a class declared 'ordered=False'.

    Every method generated here is named after the class and itself, as
    'Point.asDict', through '_qualify'. The class declares no '__slots__':
    the values of the fields live in the instance '__dict__', which is
    what lets several EZData classes with fields combine as bases. A field
    whose name a data descriptor further along the resolution order would
    take over receives an 'EZStore' through 'storeFactory'. The guard in
    'EZSpace.registerEZField' keeps the names of the optional methods from
    being used as fields.

    Parameters
    ----------

    compiledSpace : dict
      The dictionary the class is created from, changed in place.

    Returns
    -------

    dict
      'compiledSpace', with the entries above set.
    """
    if self._standsDown():
      return compiledSpace
    self._refuseOverloadedReserved()
    self._refuseOverloadedFields()
    ezFields = self.space.getFields()
    kwargs = self.space.getKwargs()
    compiledSpace['__ez_fields__'] = ezFields

    lookupOrder = self.space._getLookupOrder()
    isFrozen, _ = self.parseKwargs(*self.__frozen_keys__, **kwargs)
    isOrdered, _ = self.parseKwargs(*self.__ordered_keys__, **kwargs)
    isKwOnly, _ = self.parseKwargs(*self.__kw_only_keys__, **kwargs)
    if isOrdered is None:
      isOrdered = self._inheritedFlag(lookupOrder, '__is_ordered__')
    compiledSpace['__is_frozen__'] = True if isFrozen else False
    compiledSpace['__is_ordered__'] = True if isOrdered else False
    compiledSpace['__kw_only__'] = True if isKwOnly else False

    if not compiledSpace['__is_frozen__']:
      self._refuseThawing(lookupOrder)
    factories = self._optionalFactories(
        ezFields,
        compiledSpace['__kw_only__']
    )
    generated = self._settleOptional(compiledSpace, factories, lookupOrder)
    compiledSpace['__ez_generated__'] = generated
    compiledSpace['__init__'] = self.initFactory(ezFields)
    compiledSpace['__iter__'] = self.iterFactory()
    compiledSpace['__len__'] = self.lenFactory()
    compiledSpace['__eq__'] = self.eqFactory()
    compiledSpace.update(self.storeFactory(ezFields, lookupOrder))
    if compiledSpace['__is_frozen__']:
      compiledSpace['__hash__'] = self.hashFactory()
      compiledSpace['__setattr__'] = self.badSetAttrFactory()
      compiledSpace['__delattr__'] = self.badDelAttrFactory()
    else:
      compiledSpace['__hash__'] = None
      compiledSpace['__setattr__'] = self.setAttrFactory(ezFields)
      compiledSpace['__delattr__'] = self.delAttrFactory(ezFields)
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
    try:
      owner = compiledSpace['__qualname__']
    except KeyError:
      #  This branch is reached by the following:
      #  - The class is built by calling the metaclass, or 'types.new_class',
      #    with a dictionary the compiler never wrote, so no qualified name
      #    was recorded in it
      owner = self.space.getClassName()
    self._qualify(compiledSpace, owner, *generated, *self.__installed__)
    return compiledSpace

  def _refuseThawing(self, lookupOrder: list[type]) -> None:
    """
    Freezing is a promise of the base: its instances refuse assignment and
    hash by their values. A subclass declared without the keyword would
    take assignment and refuse hashing while comparing equal to the frozen
    instances, so the class statement must be refused instead, as
    'dataclasses' refuses a non-frozen dataclass based on a frozen one. A
    frozen subclass of a mutable class is allowed.

    Implementation
    --------------

    The flag '__is_frozen__' of each class along 'lookupOrder' is read
    with 'type.__getattribute__', and a true one refuses the class. A base
    built by no 'EZMeta', as 'Object' or a plain mixin, carries no flag
    and is passed over. 'ordered' is inherited through '_inheritedFlag';
    'kwOnly' stays per class.

    Parameters
    ----------

    lookupOrder : list[type]
      The classes after the class under construction in its resolution
      order.

    Raises
    ------

    TypeError
      A class along 'lookupOrder' is a frozen 'EZData' class.
    """
    for base in lookupOrder:
      try:
        frozen = type.__getattribute__(base, '__is_frozen__')
      except AttributeError:
        #  This branch is reached by the following:
        #  - The base was built by no 'EZMeta', as 'Object' or a plain
        #    mixin, so it carries no frozen flag
        continue
      if frozen:
        infoSpec = """'%s' is based on the frozen class '%s' and does
        not declare 'frozen=True' itself. A class based on a frozen
        'EZData' class is frozen too: its instances would otherwise take
        assignment and refuse hashing while comparing equal to the frozen
        ones."""
        info = infoSpec % (self.space.getClassName(), base.__name__)
        raise TypeError(textFmt(info))

  @staticmethod
  def _inheritedFlag(lookupOrder: list[type], name: str) -> bool:
    """
    A class declared without the 'ordered' keyword must take the choice
    of the nearest 'EZData' class it is based on, so a subclass of an
    ordered class compares as its base does unless it says
    'ordered=False' itself.

    Implementation
    --------------

    The first class along the order carrying the flag answers, read with
    'type.__getattribute__' past any class-level attribute hook; a plain
    base carries no flag and is passed over. 'EZData' itself carries
    'False', so a class with no ordered ancestor stays unordered.

    Parameters
    ----------

    lookupOrder : list[type]
      The classes after the class under construction in its resolution
      order.

    name : str
      The flag to read, '__is_ordered__'.

    Returns
    -------

    bool
      The flag of the nearest class carrying it, or 'False'.
    """
    for base in lookupOrder:
      try:
        return type.__getattribute__(base, name)
      except AttributeError:
        #  This branch is reached by the following:
        #  - The base was built by no 'EZMeta', as 'Object' or a plain
        #    mixin, so it carries no flag
        continue
    return False

  def _refuseOverloadedReserved(self) -> None:
    """
    A class body overloading a method EZData generates and keeps for
    itself must be refused as a plain definition of it is. The line itself
    cannot be refused as it runs: 'LoadSpaceHook' comes before this hook
    and claims every '@overload' binding, so the binding never reaches
    'setItemPhase'.

    Implementation
    --------------

    As the class is compiled, each name of
    'EZSpace.__reserved_ez_methods__' is asked of 'hasOverloads'. The
    namespace records the overloads of the body alone, so a plain base
    overloading '__init__' still gives way to the generated one, as
    documented.

    Raises
    ------

    ReservedMethodError
      The class body overloaded one of the reserved methods.
    """
    for name in self.space.__reserved_ez_methods__:
      if self.space.hasOverloads(name):
        raise ReservedMethodError(name, self.space)

  def _refuseOverloadedFields(self) -> None:
    """
    A class body overloading a method at the name of a field the class
    inherits must be refused as a plain definition there is; see
    '_refuseAtFieldName'. The dispatcher of the overloads would stand at
    the name and refuse every value the constructor stores, so the class
    would be created and no instance of it could be. The line itself
    cannot be refused as it runs: 'LoadSpaceHook' comes before this hook
    and claims every '@overload' binding, so the binding never reaches
    'setItemPhase'.

    Implementation
    --------------

    As the class is compiled, each field name of the class is asked of
    'hasOverloads', which answers for the overloads of the body alone. A
    body overloading at the name of a field it declares itself never gets
    this far: the namespace refuses that line with 'OverloadConflict'.

    Raises
    ------

    DuplicateError
      The class body overloaded a method at the name of a field the class
      inherits.
    """
    for name in self.space.getFields():
      if self.space.hasOverloads(name):
        raise DuplicateError(name, self.space)

  @staticmethod
  def _qualify(compiledSpace: dict, owner: str, *names: str) -> None:
    """
    A traceback through a generated method should name the class and the
    method, as 'Point.asDict', and not the factory that made it.

    Implementation
    --------------

    Each function among 'names' takes 'owner' and its own name as its
    '__qualname__', as a method written in the class body is named. The
    comparison every unordered class shares keeps its own name, and what
    is no function, as '__match_args__' or a '__hash__' of 'None', is
    passed over.

    Parameters
    ----------

    compiledSpace : dict
      The dictionary the class is created from.

    owner : str
      The qualified name of the class.

    *names : str
      The names of the generated methods.
    """
    for name in names:
      method = compiledSpace[name]
      if isinstance(method, FunctionType) and method is not _unorderable:
        method.__qualname__ = '%s.%s' % (owner, name)

  @staticmethod
  def _isDataDescriptor(value: Any) -> bool:
    """
    Python gives a data descriptor, one whose type defines '__set__' or
    '__delete__', precedence over the instance '__dict__', where a
    descriptor defining neither yields to it. Whether a field needs a store
    turns on that difference.

    Implementation
    --------------

    Both names are asked of the type of the value through '_typeDefines',
    past any class hook.

    Parameters
    ----------

    value : Any
      What a class holds at the name of a field.

    Returns
    -------

    bool
      Whether the value is a data descriptor.
    """
    valueType = type(value)
    hasSet = EZHook._typeDefines(valueType, '__set__')
    hasDelete = EZHook._typeDefines(valueType, '__delete__')
    return True if hasSet or hasDelete else False

  @classmethod
  def _needsStore(cls, key: str, lookupOrder: list[type]) -> bool:
    """
    A field is read from the instance '__dict__' unless a data descriptor
    of the same name sits further along the resolution order, which Python
    would ask first. Only then would a read of the attribute miss the value
    the instance holds.

    Implementation
    --------------

    The first class in 'lookupOrder' holding 'key' in its own dictionary
    decides: a data descriptor there calls for a store, anything else does
    not, and neither does a name no class holds.

    Parameters
    ----------

    key : str
      The field name.

    lookupOrder : list[type]
      The classes after the class under construction in its resolution
      order.

    Returns
    -------

    bool
      Whether the field needs an 'EZStore'.
    """
    for klass in lookupOrder:
      if key in klass.__dict__:
        return cls._isDataDescriptor(klass.__dict__[key])
    return False

  @classmethod
  def storeFactory(
      cls,
      ezFields: dict[str, EZField],
      lookupOrder: list[type],
  ) -> dict[str, EZStore]:
    """
    A field whose name a data descriptor further along the resolution order
    would take over, such as 'Object.directory' or a property on a mixin,
    must still read and write the instance '__dict__' as any other field
    does.

    Implementation
    --------------

    An 'EZStore' is made for every such field. It stands ahead of that
    descriptor in the lookup and defines '__get__' alone, so the instance
    '__dict__' answers every populated read and takes every write. Every
    other field gets no class attribute at all and is read as a plain
    instance attribute.

    Parameters
    ----------

    ezFields : dict[str, EZField]
      The fields of the class, in declaration order.

    lookupOrder : list[type]
      The classes after the class under construction in its resolution
      order.

    Returns
    -------

    dict[str, EZStore]
      The stores to install on the class, by field name.
    """
    stores = dict()
    for key in ezFields:
      if cls._needsStore(key, lookupOrder):
        stores[key] = EZStore(key)
    return stores

  @staticmethod
  def castField(key: str, value: Any, fieldType: type) -> Any:
    """
    Assignment must accept and refuse exactly the values construction
    does, and a refusal must name the field.

    Implementation
    --------------

    'typeCast' converts the value to the field type. The generated
    '__init__' and the generated '__setattr__' both go through this one
    method for every value whose class is not the field type itself; a
    value whose class is the field type 'typeCast' hands back as it is,
    so both store it without the call. A 'TypeCastException' is raised
    again as a 'TypeException' naming the field, chained.

    Parameters
    ----------

    key : str
      The name of the field receiving the value.

    value : Any
      The value.

    fieldType : type
      The declared type of the field.

    Returns
    -------

    Any
      The value as an instance of 'fieldType'.

    Raises
    ------

    TypeException
      'typeCast' refuses the value.
    """
    try:
      return typeCast(fieldType, value)
    except TypeCastException as typeCastException:
      raise TypeException(key, value, fieldType) from typeCastException

  @classmethod
  def setAttrFactory(cls, ezFields: dict[str, EZField]) -> SETATTR:
    """
    A dataclass that is not frozen takes assignment, and every field must
    go on holding a value of its type afterwards, as it does after
    construction. A name that is no field is the instance's own business.

    Implementation
    --------------

    The returned '__setattr__' casts a value assigned to a field through
    'castField' before storing it, and stores a value assigned to any other
    name as given. A value whose class is the field type itself is stored
    without the call, since 'typeCast' would hand it back as it is. The
    field types are resolved once, here, as the class is created.

    Parameters
    ----------

    ezFields : dict[str, EZField]
      The fields of the class, own and inherited.

    Returns
    -------

    SETATTR
      A 'Callable[..., None]' called as '(self, key, value)': the
      '__setattr__' of the class.
    """
    fieldTypes = {key: field.fieldType for key, field in ezFields.items()}
    castField = cls.castField

    def __setattr__(self: Any, key: str, value: Any) -> None:
      if key in fieldTypes:
        fieldType = fieldTypes[key]
        if type(value) is not fieldType:
          value = castField(key, value, fieldType)
      object.__setattr__(self, key, value)

    return __setattr__

  @classmethod
  def matchArgsFactory(
      cls,
      ezFields: dict[str, EZField],
      isKwOnly: bool,
  ) -> tuple[str, ...]:
    """
    A 'match' statement binds positional patterns through
    '__match_args__', which must name the fields in the order the
    constructor takes them, and name none for a keyword-only class, which
    takes nothing by position.

    Implementation
    --------------

    The field names in declaration order, or an empty tuple for a
    keyword-only class, as 'dataclasses.dataclass' leaves keyword-only
    fields out so that 'case Cls(a, b):' does not bind against them.
    '__match_args__' is one of the optional names, so the tuple built here
    is used only where neither the class body nor a base sets one; see
    '_settleOptional'. A tuple set by hand is kept as it is, unchecked, as
    'dataclasses', 'attrs' and 'typing.NamedTuple' keep one, and a subclass
    whose body sets none uses the one its parent set by hand.

    Parameters
    ----------

    ezFields : dict[str, EZField]
      The fields of the class, in declaration order.

    isKwOnly : bool
      Whether the class is keyword-only.

    Returns
    -------

    tuple[str, ...]
      The field names, or an empty tuple.
    """
    if isKwOnly:
      return ()
    return (*ezFields,)

  @classmethod
  def initFactory(cls, ezFields: dict) -> INIT:
    """
    The constructor of a dataclass takes its fields by position, in
    declaration order, and by keyword. It converts each value as 'typeCast'
    does, or refuses it; refuses a keyword naming no field and a field
    given twice; gives every field left out a default of its own; and then
    lets the class finish itself in '__post_init__'. A keyword-only class
    takes no positional argument. A field may be named anything, 'self'
    included, and must still arrive by keyword.

    Implementation
    --------------

    The types of the fields and a recipe for each default are resolved
    once, here, as the class is created, so a construction never reads them
    back through an 'EZField'. The recipe still builds a new value at every
    call, through 'EZField._construct', so mutable defaults stay unshared
    and a field type whose constructor returns something that is no
    instance of it raises 'TypeException'.

    The returned '__init__' assigns the positional arguments to the fields
    in declaration order, unless the class is keyword-only, which raises
    'KwargsOnlyException' for any. More positional arguments than fields
    raise 'ExtraPositionalException', a keyword naming none of the fields
    'ExtraKeywordException', and a field given both by position and by
    keyword 'RepeatedFieldException'. The keywords are assigned by name,
    and every field still unset takes its default. A field counts as unset
    when the instance '__dict__' holds no value under its name; a class
    attribute of the same name, on a mixin for example, does not count.

    The common construction pays for no more than it uses. The three
    passes over the keywords run only when a keyword is given, since each
    of them does nothing without one. A value whose class is the field
    type itself is stored as it is, without asking 'castField', which
    would hand it back unchanged.

    Then '__post_init__' is looked up on 'type(self)' with
    'type.__getattribute__' and called with the instance if a class along
    the resolution order defines it. A subclass without one of its own
    inherits that of its parent, and no '__class_getattr__' hook of the
    class is asked. It is the place for validation, normalization and
    derived state. The lookup runs at every construction, so a
    '__post_init__' put on a class after it is created is found, and so
    is one of a mixin listed after 'EZData'. A class that defines none
    answers with the 'None' its metaclass 'EZMeta' holds at the name,
    which the constructor reads as no hook; raising and catching an
    'AttributeError' there cost every such construction about a fifth of
    its time. A class built by a metaclass that is no 'EZMeta' has no
    'None' to answer with, and for it the 'AttributeError' is caught.

    The helpers take the keywords of the caller as one dict, and the
    receiver of '__init__' is named '__ez_self__', so that a field named as
    a parameter of the generated code, 'self' or 'argCount', is free to
    arrive as a keyword, as 'dataclasses' arranges for a field named
    'self'.

    Parameters
    ----------

    ezFields : dict[str, EZField]
      The fields of the class, own and inherited, in declaration order.

    Returns
    -------

    INIT
      A 'Callable[..., None]' called as '(self, *args, **kwargs)': the
      '__init__' of the class.
    """
    specs = []
    construct = EZField._construct
    for key, field in ezFields.items():
      fieldType = field.fieldType
      posArgs = field.posArgs
      keyArgs = field.keyArgs

      def makeDefault(t=fieldType, n=key, a=posArgs, k=keyArgs) -> Any:
        return construct(t, n, a, k)

      specs.append((key, fieldType, makeDefault))
    specs = (*specs,)
    fieldCount = len(specs)
    fieldNames = (*(key for key, _, __ in specs),)
    castField = cls.castField

    def _assignField(self: Any, key: str, val: Any, type_: type) -> None:
      if type(val) is not type_:
        val = castField(key, val, type_)
      object.__setattr__(self, key, val)

    #  The helpers take the keywords of the caller as one argument, and
    #  the receiver of '__init__' is not named 'self': a field named as
    #  a parameter of these functions, 'self' or 'argCount', must be
    #  free to arrive as a keyword, as 'dataclasses' arranges for a field
    #  named 'self'.

    def _refuseUnknown(self: Any, kwargs: dict) -> None:
      for key in kwargs:
        if key not in fieldNames:
          raise ExtraKeywordException(type(self), key, *fieldNames)

    def _refuseRepeated(self: Any, argCount: int, kwargs: dict) -> None:
      for key in fieldNames[:argCount]:
        if key in kwargs:
          raise RepeatedFieldException(type(self), key)

    def _applyKwargs(self: Any, kwargs: dict) -> None:
      for key, type_, _ in specs:
        if key in kwargs:
          _assignField(self, key, kwargs[key], type_)

    def _applyArgs(self: Any, *args) -> None:
      if len(args) > fieldCount:
        raise ExtraPositionalException(type(self), fieldCount, len(args))
      for (key, type_, _), arg in zip(specs, args):
        _assignField(self, key, arg, type_)

    def _applyDefaults(self: Any) -> None:
      values = self.__dict__
      for key, _, makeDefault in specs:
        if key not in values:
          object.__setattr__(self, key, makeDefault())

    def __init__(__ez_self__: Any, *args, **kwargs) -> None:
      self = __ez_self__
      if not self.__kw_only__:
        _applyArgs(self, *args)
      elif args:
        raise KwargsOnlyException(type(self), len(args))
      if kwargs:
        _refuseUnknown(self, kwargs)
        _refuseRepeated(self, len(args), kwargs)
        _applyKwargs(self, kwargs)
      _applyDefaults(self)
      try:
        postInit = type.__getattribute__(type(self), '__post_init__')
      except AttributeError:
        #  This branch is reached by the following:
        #  - A metaclass that is no 'EZMeta' built the class, so the
        #    lookup has no 'None' to land on, and neither the class body
        #    nor a base defines '__post_init__'; a '__class_getattr__'
        #    hook of the class is not asked for it
        return
      if postInit is None:
        #  This branch is reached by the following:
        #  - Neither the class body nor a base defines '__post_init__',
        #    and the lookup landed on the 'None' that 'EZMeta' holds
        return
      postInit(self)

    return __init__

  @classmethod
  def iterFactory(cls, ) -> ITER:
    """
    An instance iterates and unpacks as its values, in declaration order,
    so that 'x, y = point' works, 'tuple(instance)' gives what
    'instance.asTuple()' gives, and 'list(instance)' holds each value once.

    Implementation
    --------------

    The returned '__iter__' yields the value of each field of
    '__ez_fields__', read with 'getattr'.

    Returns
    -------

    ITER
      A 'Callable[..., Iterator]' called as '(self)': the '__iter__' of the
      class.
    """

    def __iter__(self: Any) -> Iterator:
      for name, desc in self.__ez_fields__.items():
        yield getattr(self, name)

    return __iter__

  @classmethod
  def lenFactory(cls, ) -> Callable[..., int]:
    """
    The length of an instance is the number of its fields, own and
    inherited, which is the number of values iterating it yields, so
    'len(instance)' equals 'len(instance.asTuple())'. A class without a
    '__bool__' of its own is then true exactly when it has fields.

    Implementation
    --------------

    The returned '__len__' measures '__ez_fields__'.

    Returns
    -------

    Callable[..., int]
      Called as '(self)': the '__len__' of the class.
    """

    def __len__(self: Any) -> int:
      return len(self.__ez_fields__)

    return __len__

  @classmethod
  def asDictFactory(cls, ) -> Callable[..., dict]:
    """
    A caller wants the values of an instance by name, in a dict of its own
    that may be changed freely without touching the instance.

    Implementation
    --------------

    The returned 'asDict' builds a new dict from each field name to its
    current value, in declaration order, at every call.

    Returns
    -------

    Callable[..., dict]
      Called as '(self)': the 'asDict' of the class.
    """

    def asDict(self: Any) -> dict:
      return {name: getattr(self, name) for name in self.__ez_fields__}

    return asDict

  @classmethod
  def asTupleFactory(cls, ) -> Callable[..., tuple]:
    """
    The values of an instance in declaration order are what
    'tuple(instance)' gives, and a caller who prefers a named method
    beside 'asDict' should have one.

    Implementation
    --------------

    The returned 'asTuple' unpacks the instance into a tuple.

    Returns
    -------

    Callable[..., tuple]
      Called as '(self)': the 'asTuple' of the class.
    """

    def asTuple(self: Any) -> tuple:
      return (*self,)

    return asTuple

  @classmethod
  def replaceFactory(cls, ) -> Callable[..., Any]:
    """
    A changed copy of an instance, the named fields replaced and every
    other value taken from the instance, is the way to derive a new value
    from a frozen one, as 'dataclasses.replace' is. A misspelled name must
    be reported, not dropped. And a class writing its own 'asDict', to nest
    or to add a key, must keep a working 'replace'.

    Implementation
    --------------

    The returned 'replace' reads the values off the fields themselves and
    calls the class with them and the changes. The generated '__init__'
    therefore converts each value, refuses a keyword that names no field
    with 'ExtraKeywordException', as 'dataclasses.replace' leaves the
    refusal to '__init__', and runs '__post_init__' again. The receiver is
    named '__ez_self__', so a field named 'self' may be among the changes.

    Returns
    -------

    Callable[..., Any]
      Called as '(self, **changes)': the 'replace' of the class, returning
      a new instance of the class of 'self'.
    """

    #  The receiver is not named 'self', so a field of that name may be
    #  among the changes. The values are read off the fields themselves,
    #  not through 'asDict', which a class body may write its own way.
    def replace(__ez_self__: Any, **changes) -> Any:
      self = __ez_self__
      values = {name: getattr(self, name) for name in self.__ez_fields__}
      return type(self)(**{**values, **changes})

    return replace

  @classmethod
  def fieldPairsFactory(cls, ) -> Callable[..., list[str]]:
    """
    The two texts of an instance both show its fields as 'name=value', and
    a class wanting them shown another way should have one place to say
    so.

    Implementation
    --------------

    The returned '__field_pairs__' gives one 'name=value' string per field,
    the value by its 'repr', in declaration order. The generated '__str__'
    and '__repr__' read it, so a class changes both by writing
    '__field_pairs__' alone.

    Returns
    -------

    Callable[..., list[str]]
      Called as '(self)': the '__field_pairs__' of the class.
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
    The text of an instance for a reader names the class and shows each
    field with its value, in declaration order.

    Implementation
    --------------

    The returned '__str__' gives '<Class: name=value, ...>', the pairs
    taken from '__field_pairs__', so a class changes the text by writing
    that method alone.

    Returns
    -------

    Callable[..., str]
      Called as '(self)': the '__str__' of the class.
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
    The 'repr' of an instance should be an expression that builds an equal
    instance when evaluated, in the call shape the class accepts.

    Implementation
    --------------

    For a class taking positional arguments the returned '__repr__' gives
    the values as such, 'Foo(3.0, 4.0)'; for a keyword-only class it gives
    'name=value' pairs through '__field_pairs__', 'Foo(x=3.0, y=4.0)'.

    Returns
    -------

    Callable[..., str]
      Called as '(self)': the '__repr__' of the class.
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
    Two instances are equal when they hold equal values and their classes
    are congruent: one class, or a class and a subclass holding the same
    fields. Anything that is no dataclass is left to the other operand. The
    common comparison, two instances of one class, must not pay for the
    general question.

    Implementation
    --------------

    The returned '__eq__' answers 'NotImplemented' when the class of
    'other' was built by no metaclass of this kind, and 'False' when it is
    another class that is not congruent. 'isCongruent' is asked only when
    the classes differ: two instances of one class are congruent by
    definition. Otherwise the tuples of the values are compared.

    Returns
    -------

    Callable[..., bool]
      Called as '(self, other)': the '__eq__' of the class.
    """

    def __eq__(self: Any, other: Any) -> bool:
      selfCls, otherCls = type(self), type(other)
      if not isinstance(otherCls, type(selfCls)):
        return NotImplemented
      if otherCls is not selfCls:
        if not selfCls.isCongruent(otherCls):
          return False
      selfValues = (*self,)
      otherValues = (*other,)
      return True if selfValues == otherValues else False

    return __eq__

  @classmethod
  def hashFactory(cls, ) -> Callable[..., int]:
    """
    Instances of a frozen class are hashable, equal ones alike. An
    instance that can change must not be.

    Implementation
    --------------

    The returned '__hash__' hashes the tuple of the values in declaration
    order. It is installed on frozen classes only; any other class sets
    '__hash__' to 'None', so the interpreter refuses 'hash(instance)'.

    Returns
    -------

    Callable[..., int]
      Called as '(self)': the '__hash__' of a frozen class.
    """

    def __hash__(self: Any) -> int:
      return hash((*self,))

    return __hash__

  @classmethod
  def orderingFactory(cls, op: Callable[..., bool]) -> Callable[..., bool]:
    """
    An ordered class compares its instances field by field, in declaration
    order, with another instance of the same class, and leaves anything
    else to the other operand.

    Implementation
    --------------

    The returned function applies 'op' to the tuples of the values of both
    instances, and answers 'NotImplemented' for an instance of another
    class. Its '__name__' is set to '__<op>__', so that tracebacks and
    introspection report the operator.

    Parameters
    ----------

    op : Callable[..., bool]
      A comparison from 'operator': 'operator.lt', 'operator.le',
      'operator.gt' or 'operator.ge'.

    Returns
    -------

    Callable[..., bool]
      Called as '(self, other)': the ordering method of the class.
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
  def badSetAttrFactory(cls, ) -> SETATTR:
    """
    An instance of a frozen class stays as it was built: every assignment
    is refused, to a field or to any other name.

    Implementation
    --------------

    The returned '__setattr__' raises 'AttributeError'. The generated
    '__init__' writes the fields with 'object.__setattr__' and is not
    affected.

    Returns
    -------

    SETATTR
      A 'Callable[..., None]' called as '(self, key, value)': the
      '__setattr__' of a frozen class.
    """

    # noinspection PyUnusedLocal
    def __setattr__(self: Any, key: str, value: Any) -> None:
      clsName = type(self).__name__
      infoSpec = """'%s' is frozen; cannot assign to attribute '%s'!"""
      raise AttributeError(infoSpec % (clsName, key))

    return __setattr__

  @classmethod
  def delAttrFactory(cls, ezFields: dict[str, EZField]) -> DELATTR:
    """
    Every declared field of a dataclass always holds a value of its type,
    and deleting one would break that. Any other attribute the instance
    took beside its fields may go again, as on a dataclass that is not
    frozen.

    Implementation
    --------------

    The returned '__delattr__' raises 'AttributeError' for a field and
    hands any other name to 'object.__delattr__'.

    Parameters
    ----------

    ezFields : dict[str, EZField]
      The fields of the class, own and inherited.

    Returns
    -------

    DELATTR
      A 'Callable[..., None]' called as '(self, key)': the '__delattr__'
      of a class that is not frozen.
    """
    fieldNames = (*ezFields,)

    def __delattr__(self: Any, key: str) -> None:
      if key in fieldNames:
        clsName = type(self).__name__
        infoSpec = """EZData class '%s' does not allow deleting field
        '%s': every field holds a value of its declared type."""
        raise AttributeError(textFmt(infoSpec % (clsName, key)))
      object.__delattr__(self, key)

    return __delattr__

  @classmethod
  def badDelAttrFactory(cls, ) -> DELATTR:
    """
    A frozen instance stays as it was built: every deletion is refused, of
    a field or of any other attribute, as every assignment is.

    Implementation
    --------------

    The returned '__delattr__' raises 'AttributeError'.

    Returns
    -------

    DELATTR
      A 'Callable[..., None]' called as '(self, key)': the '__delattr__'
      of a frozen class.
    """

    def __delattr__(self: Any, key: str) -> None:
      clsName = type(self).__name__
      infoSpec = """'%s' is frozen; cannot delete attribute '%s'!"""
      raise AttributeError(infoSpec % (clsName, key))

    return __delattr__
