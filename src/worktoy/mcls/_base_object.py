"""
BaseObject is the standard entry point for using the worktoy library.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import BaseMeta
from ..core import Object


class BaseObject(Object, metaclass=BaseMeta):
  """
  BaseObject combines the core functionality of Object with the
  hook-based metaclass behavior of BaseMeta.

  From Object, it inherits robust constructor handling, controlled
  descriptor mutation, and context-aware access to instance and owner
  information. From BaseMeta, it gains support for function overloading
  and other hook-based class construction features via BaseSpace.

  Subclass this when you want both: sane, safe object semantics and
  overload-aware metaclass support.

  Constructor arguments
  ---------------------
  A subclass that defines neither '__init__' nor '__new__' takes no
  constructor arguments, as a plain Python class takes none: 'Point(3,
  4)' raises 'TypeError: Point() takes no arguments'. 'Object.__init__'
  records whatever arguments it receives, which a descriptor needs for its
  deferred default, so such a class used to accept any arguments and drop
  them without a word. A subclass whose '__init__' hands its arguments on
  to 'super().__init__' still has them recorded, and so does every
  'Object' that is not a 'BaseObject'.

  Once 'Object.__init__' has recorded the arguments, it calls the next
  '__init__' along the resolution order without them. A base listed after
  'BaseObject', such as 'threading.Thread', 'logging.Handler' or a
  cooperative mixin, is therefore initialized as in a plain class. A base
  whose '__init__' requires arguments goes before 'BaseObject', where it
  receives them.
  """

  def __init__(self, *args, **kwargs) -> None:
    """
    The '__init__' method refuses arguments given to a class that defines
    neither '__init__' nor '__new__' below 'BaseObject', with the
    'TypeError' Python raises for a class without an initializer, and
    otherwise hands them on to 'Object.__init__', which records them.
    """
    cls = type(self)
    ownInit = cls.__init__ is not BaseObject.__init__
    ownNew = cls.__new__ is not object.__new__
    if (args or kwargs) and not (ownInit or ownNew):
      infoSpec = """%s() takes no arguments"""
      raise TypeError(infoSpec % cls.__name__)
    Object.__init__(self, *args, **kwargs)
