"""
EZSpace is the namespace 'EZMeta' uses to build 'EZData' classes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import EZHook
from ..mcls import BaseSpace
from ..mcls import AbstractMetaclass as AMeta
from ..utilities import maybe
from ..waitaminute.ezdata import DuplicateError, ReservedFieldError

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Optional, TypeAlias
  from . import EZMeta, EZField

  Bases: TypeAlias = tuple[EZMeta, ...]


class EZSpace(BaseSpace):
  """
  The body of a dataclass runs in a namespace, and that namespace must
  keep the fields the body declares apart from the rest of the body, know
  the fields the class inherits, and refuse at its line a field that
  takes a name the dataclass needs for itself or a name the body bound
  before. A project building a dataclass base of its own must be able to
  keep further names from a body.

  Implementation
  --------------

  'EZMeta.__prepare__' returns an 'EZSpace'. Its hook, 'ezHook', claims
  the fields and hands them to 'registerEZField'. '__init__' gathers the
  fields of the bases, as clones, and 'getFields' merges both in the
  order the constructor takes them. Three tuples hold the names kept
  from a body. The hook reads each of them unmodified, so a subclass of
  'EZSpace' extends them to keep further names.

  Attributes
  ----------

  ezHook : EZHook
    The hook that takes the fields of the class body and generates the
    methods of the class.

  __reserved_ez_names__ : tuple[str, ...]
    The names of the methods EZData generates where a class has none of
    its own, 'asDict', 'asTuple', 'replace', '__field_pairs__',
    '__repr__' and '__str__', and '__post_init__'. A field may not take
    one of them and raises 'ReservedFieldError'; a method may be written
    at each.

  __reserved_ez_methods__ : tuple[str, ...]
    The names of the generated methods EZData keeps for itself, the ones
    installed after the class body is merged, which a definition in the
    body could not replace anyway. A class body binding one of them
    raises 'ReservedMethodError', whatever the value, and so does a class
    body overloading one of them, as the class is created. A plain base
    may define them, and the generated methods take precedence.

  __reserved_ez_attributes__ : tuple[str, ...]
    The names of the attributes EZData keeps for itself: those it sets on
    every class, the fields and the options the class keywords resolve
    to, and '__key_args__', under which 'Object' keeps the keyword
    arguments of its constructor. A class body binding one of them raises
    'ReservedAttributeError', whatever the value, where the binding would
    otherwise become a field of that name. '__slots__' is refused before
    this namespace sees it, by 'NamespaceHook' with 'SlotsRefused', as in
    every worktoy class body.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  ezHook = EZHook()
  __reserved_ez_names__: tuple = (
    '__field_pairs__',
    '__repr__',
    '__str__',
    '__post_init__',
    'asDict',
    'asTuple',
    'replace',
  )
  __reserved_ez_methods__: tuple = (
    '__init__',
    '__iter__',
    '__len__',
    '__eq__',
    '__hash__',
    '__lt__',
    '__le__',
    '__gt__',
    '__ge__',
    '__setattr__',
    '__delattr__',
  )
  __reserved_ez_attributes__: tuple = (
    '__ez_fields__',
    '__key_args__',
    '__is_frozen__',
    '__is_ordered__',
    '__kw_only__',
    '__ez_generated__',
  )

  #  Private Variables
  __ez_fields__: Optional[dict[str, EZField]] = None
  __base_fields__: Optional[dict[str, EZField]] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getEZFields(self, ) -> dict[str, EZField]:
    """
    The fields a class body declares itself must be told from the ones the
    class inherits: a subclass gathers the own fields of each base, and a
    name bound twice in one body is refused.

    Implementation
    --------------

    The mapping from name to field, in declaration order, empty before any
    field is registered.

    Returns
    -------

    dict[str, EZField]
      The own fields of the class body.
    """
    return maybe(self.__ez_fields__, dict())

  def getBaseFields(self, ) -> dict[str, EZField]:
    """
    The fields a class inherits must be objects of its own, so that binding
    them to the subclass leaves the fields of the bases as they were.

    Implementation
    --------------

    '__init__' fills the mapping with clones while walking the classes the
    class is based on, from the most general to the most specific.

    Returns
    -------

    dict[str, EZField]
      The inherited fields, each a clone.
    """
    return maybe(self.__base_fields__, dict())

  def getFields(self, ) -> dict[str, EZField]:
    """
    The constructor, the iteration and '__match_args__' of a class all need
    one ordered list of its fields: the inherited ones first, then its own,
    a field the body declares again taking the place of the inherited one.

    Implementation
    --------------

    A new dict of the base fields overlaid with the own ones. 'EZHook'
    compiles it into '__ez_fields__', '__match_args__' and the generated
    '__init__'.

    Returns
    -------

    dict[str, EZField]
      Every field of the class, in declaration order.
    """
    baseFields = self.getBaseFields()
    ezFields = self.getEZFields()
    out = dict()
    for name, field in baseFields.items():
      out[name] = field
    for name, field in ezFields.items():
      out[name] = field
    return out

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def registerEZField(self, key: str, field: EZField, ) -> None:
    """
    A field the class body binds must be taken for the class under its
    name, unless the name is one the dataclass needs for a method, or one
    the body bound before: two declarations at one name would leave one of
    them lost without a word. A field object bound before, to another name
    or in another class, must not end up shared between the two.

    Implementation
    --------------

    'EZHook.setItemPhase' calls this method for an 'EZField' and for a
    plain value wrapped by 'EZField.fromValue'. A reserved name raises
    'ReservedFieldError'. A name the body bound before raises
    'DuplicateError': one registered as a field, or one the namespace
    itself stores, which is where a method or a descriptor of the body is
    kept, since the hook claims every field. A field already carrying a
    name is cloned first, which keeps the second binding independent of
    the first. The field takes the name and is stored among the own
    fields.

    Parameters
    ----------

    key : str
      The name the field is bound to.

    field : EZField
      The field.

    Raises
    ------

    ReservedFieldError
      'key' is one of the names of '__reserved_ez_names__': 'asDict',
      'asTuple', 'replace', '__post_init__', '__repr__', '__str__' or
      '__field_pairs__'.

    DuplicateError
      'key' is registered as an own field already, or the body bound it
      to a method or a descriptor before; one class body may not bind the
      same name twice.
    """
    if key in self.__reserved_ez_names__:
      raise ReservedFieldError(key, self)
    if dict.__contains__(self, key):
      #  This branch is reached by the following:
      #  - The body bound the name before to a method or a descriptor,
      #    which the namespace stored, and now binds a field at it
      raise DuplicateError(key, self)
    existing = self.getEZFields()
    if key not in existing:
      if field.__field_name__ is not None:
        #  The field instance is already bound to another name, either
        #  earlier in this class body or in another class. Registering
        #  a clone keeps the alias independent instead of mutating the
        #  shared instance's name binding.
        field = field.clone()
      setattr(field, '__field_name__', key)
      existing[key] = field
      self.__ez_fields__ = existing
    else:
      raise DuplicateError(key, self)

  def registerBaseField(self, key: str, field: EZField, ) -> None:
    """
    An inherited field must be the subclass's own object. Where several
    classes along the resolution order declare one name, the nearest must
    decide the field, as attribute lookup would find it, while the field
    keeps the place the most general class gave it, the order 'dataclasses'
    uses.

    Implementation
    --------------

    The field is cloned, named and stored. Registering a name again
    replaces the field and keeps the position the name first took.
    '__init__' registers the classes from the far end of the resolution
    order, so the farthest class decides the position of a field and the
    nearest class the field itself.

    Parameters
    ----------

    key : str
      The name of the inherited field.

    field : EZField
      The field of the base, which is cloned.
    """
    existing = self.getBaseFields()
    cloned = field.clone()
    setattr(cloned, '__field_name__', key)
    existing[key] = cloned
    self.__base_fields__ = existing

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: AMeta, name: str, bases: Bases, **kw) -> None:
    """
    Before the body runs, the namespace must know the fields the class
    inherits: every dataclass along its resolution order contributes the
    fields of its own body. They must run from the most general class to
    the most specific, the order 'dataclasses' uses, each base keeping the
    order of its own fields.

    Implementation
    --------------

    After 'BaseSpace.__init__' has set the namespace up, the lookup order
    is walked from the far end, and each class whose namespace is an
    'EZSpace' has the fields of its own body registered as base fields. A
    base built by no worktoy metaclass, as 'object' or a plain mixin,
    carries no namespace and declares no field. When several classes
    declare one name, the nearest decides the field; see
    'registerBaseField'.

    Parameters
    ----------

    mcls : type
      The metaclass building the class, 'EZMeta' or a subclass.

    name : str
      The name of the class.

    bases : Bases
      A 'tuple[EZMeta, ...]' of the bases of the class statement.

    **kw
      The class keywords, among them the spellings of 'frozen', 'ordered'
      and 'kwOnly' that 'EZHook.postCompilePhase' reads later.
    """
    BaseSpace.__init__(self, mcls, name, bases, **kw)
    for base in reversed(self._getLookupOrder()):
      try:
        space = base.__dict__['__namespace__']
      except KeyError:
        #  This branch is reached by the following:
        #  - The base was built by no worktoy metaclass, as 'object' or a
        #    plain mixin, so it carries no namespace and declares no field
        continue
      if isinstance(space, EZSpace):
        for key, field in space.getEZFields().items():
          self.registerBaseField(key, field)
