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

from ..utilities import NoPickle
from ..waitaminute.desc import PhantomBoxError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never, Optional


class _RootAlias(NoPickle, GenAlias, _root=True):
  """
  This class is returned when a box, 'AttriBox' or 'FastBox', is
  subscripted with anything but a plain class: a 'TypeVar', as in
  'class Sub(AttriBox[T])', or a parametrized generic such as 'list[int]'.

  The generic machinery hands back a plain 'typing._GenericAlias', which
  is the object a class body actually stores when a subscript is written
  without the trailing call. Its type carries no '__get__', so reading
  such an attribute quietly returns the alias itself. Re-clothing the
  alias in this subclass puts a '__get__' on the stored object, which is
  the only hook the descriptor protocol consults for it.
  """

  @classmethod
  def fromAlias(cls, alias: GenAlias) -> _RootAlias:
    """
    The 'fromAlias' constructor rebuilds 'alias' as an instance of this
    class, carrying over the origin, the arguments, and the two display
    settings that decide how the alias renders and whether it may be
    instantiated.

    Cloning through 'copy_with' does not work here: that method builds
    'self.__class__(...)', and 'self' is the plain alias the generic
    machinery returned, so the copy comes back the same plain class no
    matter which class the method is looked up on.

    Parameters
    ----------
    alias : GenAlias
        The alias handed back by the generic machinery.

    Returns
    -------
    _RootAlias
        A faithful copy of 'alias' whose type supplies '__get__'.
    """
    # noinspection PyProtectedMember
    aliasName, aliasInst = alias._name, alias._inst
    aliasOrigin, aliasArgs = alias.__origin__, alias.__args__
    return cls(aliasOrigin, aliasArgs, name=aliasName, inst=aliasInst, )

  def copy_with(self, args: tuple) -> _RootAlias:
    """
    The 'copy_with' method keeps this class through the copies the
    generic machinery makes internally, for instance while substituting
    a 'TypeVar'. Without the override those copies fall back to the
    plain alias class and silently lose '__get__' again.

    The name is snake_case because it overrides a CPython 'typing'
    internal, not because the surrounding convention changed.

    Parameters
    ----------
    args : tuple
        The replacement arguments for the copy.

    Returns
    -------
    _RootAlias
        A copy carrying 'args' and this class.
    """
    cls = type(self)
    return cls(self.__origin__, args, name=self._name, inst=self._inst, )

  def __set_name__(self, owner: type, name: str) -> Never:
    """
    Binding this alias to a name in a class body is refused as the class
    is created, which is the earliest moment the mistake is unambiguous.
    The subscript alone cannot be judged, since 'class Sub(AttriBox[T])'
    legitimately asks for the very same alias; a base-class entry is not
    a namespace value, so that declaration never reaches here.

    The interpreter looks '__set_name__' up on the type of each value in
    the class body, and the type of a stored alias is this class, so a
    plain method is all the hook requires.

    Note that Python 3.7 through 3.11 re-raise anything from
    '__set_name__' wrapped in a 'RuntimeError', with the original left
    on '__cause__'. From 3.12 onward it propagates unchanged.
    """
    raise PhantomBoxError(self, owner, name)

  def __get__(self, instance: Any, owner: Optional[type] = None) -> Never:
    """
    Reading an attribute that holds this alias is refused as well. The
    class-body route is already closed by '__set_name__', so what
    reaches here is an alias installed after the fact, by 'setattr' on a
    finished class, where no name was ever assigned to report.
    """
    raise PhantomBoxError(self, owner)
