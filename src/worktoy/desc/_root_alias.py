"""
_RootAlias is the type alias a box subscript returns for anything but a
plain class, clothed so that binding it in a class body is refused.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
# noinspection PyUnresolvedReferences, PyProtectedMember
from typing import _GenericAlias as GenAlias

from ..waitaminute.desc import PhantomBoxError

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Never, Optional


class _RootAlias(GenAlias, _root=True):
  """
  A box subscripted with a plain class, 'AttriBox[int]', is a box. A box
  subscripted with anything else, a 'TypeVar' as in
  'class Sub(AttriBox[T])' or a generic such as 'list[int]', must be a
  type alias, since that is what a type hint or a list of bases needs.
  Such an alias written in a class body as if it were a box would sit
  there silently and read back as itself, so the mistake must fail
  instead, without spoiling the alias where it belongs.

  Implementation
  --------------

  The alias 'typing' returns is rebuilt as a '_RootAlias', a subclass of
  'typing._GenericAlias' whose '__set_name__' refuses a place in a class
  body, whose '__call__' refuses the parentheses of a declaration, and
  whose '__get__' refuses a read of one installed later with 'setattr',
  all with 'PhantomBoxError'. A base is not a value of the class body,
  so 'class Sub(AttriBox[T])' never reaches any of them.
  """

  @classmethod
  def fromAlias(cls, alias: GenAlias) -> _RootAlias:
    """
    The alias 'typing' returns must become a '_RootAlias' without losing
    anything that decides how it renders or whether it may be called.

    Implementation
    --------------

    The origin, the arguments, the name and the instantiation setting are
    carried over. 'copy_with' cannot serve, since it builds an instance of
    the class of the alias it is called on, which is the plain alias.

    Parameters
    ----------

    alias : GenAlias
      The 'typing._GenericAlias' 'Generic.__class_getitem__' returned.

    Returns
    -------

    _RootAlias
      An equal alias of this class.
    """
    # noinspection PyProtectedMember
    aliasName, aliasInst = alias._name, alias._inst
    aliasOrigin, aliasArgs = alias.__origin__, alias.__args__
    return cls(aliasOrigin, aliasArgs, name=aliasName, inst=aliasInst, )

  def copy_with(self, args: tuple) -> _RootAlias:
    """
    'typing' copies an alias internally, as when it substitutes a
    'TypeVar', and the copy must stay a '_RootAlias'.

    Parameters
    ----------

    args : tuple
      The arguments of the copy.

    Returns
    -------

    _RootAlias
      The copy.
    """
    cls = type(self)
    return cls(self.__origin__, args, name=self._name, inst=self._inst, )

  def __set_name__(self, owner: type, name: str) -> Never:
    """
    The alias bound to a name in a class body is the moment the mistake is
    certain.

    Raises
    ------

    PhantomBoxError
      Always; on Python 3.7 to 3.11 it reaches the class statement wrapped
      in a 'RuntimeError'.
    """
    raise PhantomBoxError(self, owner, name)

  def __call__(self, *args, **kwargs) -> Never:
    """
    The alias called with parentheses, as 'AttriBox[list[int]]([])', is a
    box declared with a subscript the box does not claim, and the mistake
    must fail at that line with the error written for it. 'typing' would
    build a bare box of the origin instead, with no field type, refused
    only as the class is created and in other words.

    Raises
    ------

    PhantomBoxError
      Always. A generic subclass, 'class Sub(AttriBox[T])', takes the
      alias as a base and never calls it.
    """
    raise PhantomBoxError(self)

  def __get__(self, instance: Any, owner: Optional[type] = None) -> Never:
    """
    An alias installed on a finished class with 'setattr' must fail when
    read, as one in the class body fails when the class is created.

    Raises
    ------

    PhantomBoxError
      Always. It is not an 'AttributeError', so 'hasattr' raises too.
    """
    raise PhantomBoxError(self, owner)
