"""
PhantomBoxError is raised when a class-body subscript produced a type
alias instead of a box, and the resulting attribute is read.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import DescriptorException
from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class PhantomBoxError(DescriptorException):
  """
  PhantomBoxError is raised when reading an attribute whose class-body
  declaration produced a type alias rather than a box.

  A box claims its subscript only when the subscript names a plain
  'type'. Anything else, a 'TypeVar' or a parametrized generic such as
  'list[int]', is handed to the generic machinery instead, which answers
  with a type alias. That alias is the object the class body stores, and
  it is a creature of the annotation world: it belongs in a type hint or
  a base-class list, and it carries none of the descriptor behaviour the
  attribute needs. The class body therefore looks like it holds a box
  while nothing stands behind the name, which is what the exception is
  named for.

  The subscript itself cannot be refused, because a 'TypeVar' argument
  is a legitimate request at that moment: 'class Sub(AttriBox[T])' wants
  exactly that alias. What settles the intent is the alias landing in a
  class body as an attribute, which is where this is raised from.

  Attributes
  ----------
  alias : Any
    The type alias the class body stored in place of a box.
  owner : Any
    The class the alias was declared in, or 'None' when the raising
    context did not supply one.
  fieldName : Any
    The attribute name the alias was bound to, or 'None' when the
    raising context did not supply one. Attribute reads cannot name it,
    since the alias never received a name to begin with.
  """

  __slots__ = ('alias', 'owner', 'fieldName')

  def __init__(
      self,
      alias: Any,
      owner: Any = None,
      fieldName: Any = None,
  ) -> None:
    self.alias = alias
    self.owner = owner
    self.fieldName = fieldName
    DescriptorException.__init__(self, )

  def _getBoxName(self) -> str:
    """The name of the box class the subscript was written against."""
    origin = getattr(self.alias, '__origin__', None)
    return getattr(origin, '__name__', 'Box')

  @staticmethod
  def _renderArg(arg: Any) -> str:
    """Render one subscript argument the way it was written.

    A plain class renders as its bare name, while everything else falls
    back to the rendering 'typing' gives it. The '__origin__' test does
    the sorting rather than 'isinstance(arg, type)', because a builtin
    parametrized generic such as 'list[int]' answers 'True' to that on
    Python 3.9 and 3.10 alone, and then forwards '__name__' to its
    origin, quietly reducing 'list[int]' to 'list'.
    """
    if getattr(arg, '__origin__', None) is None:
      if isinstance(arg, type):
        return getattr(arg, '__name__', None) or str(arg)
    return str(arg)

  def _getSubscript(self) -> str:
    """The subscript rendered as it was written in the class body."""
    args = getattr(self.alias, '__args__', ())
    names = [self._renderArg(arg) for arg in args]
    return '%s[%s]' % (self._getBoxName(), ', '.join(names))

  def __str__(self) -> str:
    infoSpec = """The declaration '%s'%s produced a type alias rather
    than a '%s', because a box claims its subscript only when the
    subscript names a plain 'type'. An attribute needs the completed
    form, for example '%s%s[int](0)'."""
    boxName = self._getBoxName()
    subscript = self._getSubscript()
    binding = '' if self.fieldName is None else '%s = ' % (self.fieldName,)
    ownerName = getattr(self.owner, '__name__', None)
    ownerStr = '' if ownerName is None else """ in class '%s'""" % ownerName
    info = infoSpec % (
        '%s%s' % (binding, subscript), ownerStr, boxName, binding, boxName,
    )
    return textFmt(info)

  __repr__ = __str__
