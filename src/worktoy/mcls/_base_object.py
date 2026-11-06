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
  A class built with worktoy needs a base that gives it everything at
  once: overloads declared with '@overload', a class body checked for
  misspelled dunders and rebound reserved names, the class-level hooks
  of 'AbstractMetaclass', and the descriptor protocol of 'Object' for
  when an instance is placed in another class body. Arguments given to
  a class that has no initializer must still fail, as they do for a
  plain class, and a base listed after it, such as 'threading.Thread',
  must be initialized as in a plain class.

  Implementation
  --------------

  'BaseObject' is an 'Object' built by 'BaseMeta'. Its '__init__' refuses
  arguments when the class defines neither '__init__' nor '__new__'
  below 'BaseObject', with Python's own 'TypeError: Point() takes no
  arguments', and otherwise passes them to 'Object.__init__', which
  keeps them and calls the next '__init__' along the resolution order
  without them. A base whose '__init__' requires arguments is therefore
  listed before 'BaseObject'.

  Like every class built by 'AbstractMetaclass', a subclass is reported
  by 'collections.abc' as an 'Iterable', 'Iterator', 'Sized',
  'Container' and 'Collection', whether or not it defines
  '__class_iter__' or '__class_len__'. That report is wrong, and the
  fault is with 'collections.abc', whose checks look only at the
  metaclass and leave a class no way to answer for itself; see
  'AbstractMetaclass'. 'iter(cls)' and 'len(cls)' are the reliable
  tests.
  """

  def __init__(self, *args, **kwargs) -> None:
    cls = type(self)
    ownInit = cls.__init__ is not BaseObject.__init__
    ownNew = cls.__new__ is not object.__new__
    if (args or kwargs) and not (ownInit or ownNew):
      infoSpec = """%s() takes no arguments"""
      raise TypeError(infoSpec % cls.__name__)
    Object.__init__(self, *args, **kwargs)
