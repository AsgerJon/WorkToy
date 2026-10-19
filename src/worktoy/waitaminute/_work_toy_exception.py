"""
WorkToyException is the common base of every exception in the
'worktoy.waitaminute' package, giving each of them 'pickle' and 'copy'
support in one place.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import pickle
from typing import TYPE_CHECKING

from . import Detached

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


def _rebuild(cls: type, args: tuple, kwargs: dict) -> Any:
  """
  The '_rebuild' function calls 'cls' with the captured arguments. It is
  the callable 'WorkToyException.__reduce__' hands to 'pickle', and
  lives at module level so that 'pickle' stores it by reference.
  """
  return cls(*args, **kwargs)


def _travels(arg: Any) -> bool:
  """
  The '_travels' function reports whether 'arg' can be pickled. There is
  no predicate for this; the only test is to try.
  """
  try:
    pickle.dumps(arg)
  except Exception:
    return False
  return True


class WorkToyException(Exception):
  """
  WorkToyException is the common base of every exception in the
  'worktoy.waitaminute' package, the control-flow signals aside. Each
  exception keeps the builtin it is based on, 'TypeError',
  'AttributeError', 'SyntaxError' and so on, by listing this class first
  and the builtin after it, so 'except TypeError' catches a
  'TypeException' as ever, and 'except WorkToyException' catches every
  exception of the library at once.

  What the class adds is 'pickle' and 'copy' support in one place. The
  exceptions define their own '__str__' and hand their base no
  arguments, so 'BaseException.__reduce__', which rebuilds an exception
  as 'type(self)(*self.args)', used to call each class with nothing, and
  an exception raised in a process-pool worker broke the pool on the
  way back. '__new__' here records the constructor call as it was made,
  positional and keyword arguments alike, and '__reduce__' rebuilds the
  exception by calling the class with them again, so no exception needs
  to know about pickling, and a class based on 'SyntaxError', whose own
  '__init__' reads a second argument as a location tuple, is rebuilt
  without ever passing through that parsing.

  An argument that cannot be pickled, such as a lambda, a class defined
  inside a function or a namespace object, travels as a 'Detached'
  stand-in carrying its type name and 'repr', so the rebuilt exception
  keeps its type and renders its message. Copying needs no pickling, so
  '__copy__' and '__deepcopy__' rebuild from the arguments themselves.

  The captured call lives in the instance dict, which every exception
  has, so a class declaring '__slots__' is not affected; the class
  itself declares empty slots so that it adds no layout of its own and
  may stand beside 'SyntaxError', whose layout is wider than that of
  'Exception'.
  """

  __slots__ = ()

  def __new__(cls, *args, **kwargs) -> Self:
    self = BaseException.__new__(cls, *args)
    self.__init_args__ = args
    self.__init_kwargs__ = kwargs
    return self

  def __reduce__(self) -> tuple:
    """
    The '__reduce__' method hands 'pickle' the class and the captured
    arguments, each argument that cannot be pickled replaced by a
    'Detached' stand-in.
    """
    args = []
    for arg in self.__init_args__:
      args.append(arg if _travels(arg) else Detached(arg))
    kwargs = dict()
    for key, value in self.__init_kwargs__.items():
      kwargs[key] = value if _travels(value) else Detached(value)
    return _rebuild, (type(self), (*args,), kwargs)

  def __copy__(self) -> Self:
    return _rebuild(type(self), self.__init_args__, self.__init_kwargs__)

  def __deepcopy__(self, memo: dict) -> Self:
    #  Local import: 'copy' is needed here alone.
    from copy import deepcopy
    args = deepcopy(self.__init_args__, memo)
    kwargs = deepcopy(self.__init_kwargs__, memo)
    return _rebuild(type(self), args, kwargs)
