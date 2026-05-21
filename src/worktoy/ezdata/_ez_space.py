"""
EZSpace subclasses 'BaseSpace' from the 'worktoy.mcls' package and
provides the namespace class for the 'EZMeta' metaclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import EZHook
from ..mcls import BaseSpace
from ..utilities import maybe
from ..waitaminute.ezdata import DuplicateError, ReservedFieldError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Optional, TypeAlias, Type
  from . import EZMeta, EZField

  Meta: TypeAlias = Type[EZMeta]
  Bases: TypeAlias = tuple[EZMeta, ...]


class EZSpace(BaseSpace):
  """
  EZSpace is the namespace returned by 'EZMeta.__prepare__'. It
  collects the class body, separates own fields from inherited
  fields (cloned from parent EZData classes), and guards the
  reserved names that the generated method protocol claims for
  'asDict', 'asTuple', 'replace', '__post_init__', and the
  display dunders.

  Subclasses of EZSpace can extend '__reserved_ez_names__' to
  reserve additional names; the guard in 'registerEZField'
  consults that tuple unmodified.

  Attributes
  ----------
  ezHook : EZHook
    The space hook that drives EZField interception and code
    generation for the class under construction.
  __reserved_ez_names__ : tuple[str, ...]
    Names claimed by the generated method protocol that may not
    be used as EZField names. Method overrides at these names
    are still allowed; only EZField declarations are rejected.
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

  #  Private Variables
  __ez_fields__: Optional[dict[str, EZField]] = None
  __base_fields__: Optional[dict[str, EZField]] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getEZFields(self, ) -> dict[str, EZField]:
    """
    Return the mapping of own (non-inherited) field names to
    'EZField' instances, in declaration order. Empty when no own
    fields have been registered yet.

    Returns
    -------
    dict[str, EZField]
      The own-field mapping, in declaration order.
    """
    return maybe(self.__ez_fields__, dict())

  def getBaseFields(self, ) -> dict[str, EZField]:
    """
    Return the mapping of inherited field names to their cloned
    'EZField' instances, populated during '__init__' by walking
    the parent classes. Each entry is a clone of the parent's
    field, so subsequent owner binding on the subclass does not
    mutate the parent's namespace.

    Returns
    -------
    dict[str, EZField]
      The inherited-field mapping, in MRO-respecting order.
    """
    return maybe(self.__base_fields__, dict())

  def getFields(self, ) -> dict[str, EZField]:
    """
    Return the merged mapping of base fields followed by own
    fields, in declaration order. Own-field entries overwrite
    same-named inherited entries, so a subclass redeclaring a
    parent's field wins. The result is what 'EZHook' compiles
    into '__ez_fields__', '__slots__', and '__match_args__'.

    Returns
    -------
    dict[str, EZField]
      The merged base + own mapping, in declaration order.
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
    Bind an own field at the given attribute name. Called from
    'EZHook.setItemPhase' when the class body assigns either an
    'EZField' instance or a bare value that gets wrapped through
    'EZField.fromValue'. Stores 'field' in '__ez_fields__' and
    sets its '__field_name__' for later introspection.

    Parameters
    ----------
    key : str
      The attribute name the field is being bound to.
    field : EZField
      The EZField instance to register as an own field.

    Raises
    ------
    ReservedFieldError
      If 'key' is one of the names reserved by the generated
      method protocol ('asDict', 'asTuple', 'replace',
      '__post_init__', '__repr__', '__str__', '__field_pairs__').
    DuplicateError
      If 'key' has already been registered as an own field on
      this namespace; a single class body may not assign the
      same name twice.
    """
    if key in self.__reserved_ez_names__:
      raise ReservedFieldError(key, self)
    existing = self.getEZFields()
    if key not in existing:
      setattr(field, '__field_name__', key)
      existing[key] = field
      self.__ez_fields__ = existing
    else:
      raise DuplicateError(key, self)

  def registerBaseField(self, key: str, field: EZField, ) -> None:
    """
    Bind an inherited field at the given attribute name. Called
    from this namespace's '__init__' while walking the parent
    classes. The parent's 'EZField' is cloned so any later owner
    binding on the subclass leaves the parent's namespace
    untouched. Same-named entries from earlier-MRO bases are
    silently overwritten by later-MRO ones, mirroring Python's
    normal attribute-resolution rules for inherited classes.

    Parameters
    ----------
    key : str
      The attribute name the inherited field is being bound to.
    field : EZField
      The parent's EZField to clone and register on this
      namespace.
    """
    existing = self.getBaseFields()
    cloned = field.clone()
    setattr(cloned, '__field_name__', key)
    existing[key] = cloned
    self.__base_fields__ = existing

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: type, name: str, bases: Bases, **kw) -> None:
    """
    Build the namespace for an 'EZData' subclass under
    construction. After 'BaseSpace.__init__' sets up the standard
    namespace machinery, this constructor walks the parent
    classes in reverse MRO order, collects any fields they
    declared through their own 'EZSpace' namespaces, and
    registers each one as an inherited base field. Walking in
    reverse means later-MRO ancestors win on same-named entries,
    matching Python's normal attribute-resolution behavior.

    Parameters
    ----------
    mcls : type
      The metaclass building the class (always 'EZMeta' or a
      subclass).
    name : str
      The name of the class under construction.
    bases : Bases
      Spells out to 'tuple[EZMeta, ...]'. The base classes
      passed in the 'class Foo(...)' declaration.
    **kw
      Class keyword arguments, including the 'frozen', 'ordered',
      and 'kwOnly' build-option synonyms consumed later by
      'EZHook.postCompilePhase'.
    """
    BaseSpace.__init__(self, mcls, name, bases, **kw)
    cls = type(self)
    baseSpace = dict()
    for base in reversed(bases):
      try:
        space: Self = getattr(base, '__namespace__')
      except AttributeError:
        continue
      else:
        if isinstance(space, cls):
          for key, field in space.getFields().items():
            baseSpace[key] = field
    for key, field in baseSpace.items():
      self.registerBaseField(key, field)
