"""SingletonMetaclass provides a custom metaclass for creating singletons.
These are classes having only one instance, namely the class itself."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import BaseMetaclass, BaseObject


class SingletonMetaclass(BaseMetaclass):
  """SingletonMetaclass provides a custom metaclass for creating singletons.
  These are classes having only one instance, namely the class itself."""

  __singleton_instance__ = None

  def __call__(cls, *args, **kwargs) -> object:
    """The __call__ method is invoked when the class is called."""
    if kwargs.get('_reset', False):
      setattr(cls, '__singleton_instance__', None)
      return cls(*args, **{**kwargs, **dict(_reset=False)})
    if cls.__singleton_instance__ is None:
      cls.__singleton_instance__ = super().__call__(*args, **kwargs)
    cls.__init__(cls.__singleton_instance__, *args, **kwargs)
    return cls.__singleton_instance__


class Singleton(BaseObject, metaclass=SingletonMetaclass):
  """Baseclass for singleton classes."""
  pass
