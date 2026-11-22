"""
ABCMeta is the metaclass of the classes that declare abstract methods.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..waitaminute.meta import MissingImplementation
from . import BaseMeta
from . import ABCSpace

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, TypeAlias

  Types: TypeAlias = tuple[type, ...]


class ABCMeta(BaseMeta):
  """
  Some classes exist to be completed: they declare methods with
  '@abstract' that the classes based on them have to write. Such a class
  and its subclasses have more to do with each other than plain classes
  have. The class says what is to be written. A subclass may write any
  of it or none, and may add declarations of its own, so it may be
  abstract in turn. What a subclass does write is held to what was
  declared. And no object is made of a class while anything it declares
  or inherits is left unwritten. A class is never declared abstract: it
  is so for as long as it lacks an implementation.

    class Model(BaseObject, metaclass=ABCMeta):

      @abstract
      def rowCount(self) -> int: ...

      @overload(str, int)
      @abstract
      def data(self, index: str, role: int) -> Any: ...

  Python's own 'abc.ABCMeta', which this metaclass is named after and is
  no relative of, knows a method only by its name, so it cannot hold a
  class to one signature of an overloaded name: such a name holds a
  dispatcher in every class, written or not. It also checks nothing an
  implementation takes, and leaves a class based on 'int', 'dict' or a
  class of another library unchecked.

  Implementation
  --------------

  'ABCMeta' is 'BaseMeta' with 'ABCSpace' as the namespace, which works
  out as each class is created what the class still lacks and writes it
  on the class under '__missing_implementations__'; see 'ABCSpace'.
  '__call__' reads it and raises 'MissingImplementation' while anything
  is left, before '__new__' and '__init__' run and whatever the class
  is based on. A whole class is then called as any class of 'BaseMeta'
  is, so a class this metaclass builds may write the class hook
  '__class_call__': the metaclass only acts ahead of the call, and says
  so in '__chained_hooks__'.

  Attributes
  ----------

  __chained_hooks__ : tuple
    The class hooks whose operation this metaclass implements and hands
    on, '__class_call__' alone. 'NamespaceHook' reads it, and does not
    refuse such a hook with 'ShadowedClassHook'.
  """

  __chained_hooks__: tuple = ('__class_call__',)

  @classmethod
  def __prepare__(mcls, name: str, bases: Types, **kwargs) -> ABCSpace:
    return ABCSpace(mcls, name, bases, **kwargs)

  def __call__(cls, *args, **kwargs) -> Any:
    """
    Making an object of a class that still lacks an implementation must
    be refused, naming what is left, so the author of a subclass sees
    what remains to be written.

    Implementation
    --------------

    What is left is read off the class past any attribute hook, with
    'type.__getattribute__'. With nothing left, the call is handed on to
    'AbstractMetaclass.__call__'.

    Raises
    ------

    MissingImplementation
      The class is abstract.
    """
    missing = type.__getattribute__(cls, '__missing_implementations__')
    if missing:
      raise MissingImplementation(cls, *missing)
    return super().__call__(*args, **kwargs)
