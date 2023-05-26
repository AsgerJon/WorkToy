"""SingletonClass is a class allowing subclasses to have soft singleton
behaviour. This means that after then first instance of the class is
created, future calls to create instances returns that first instance.
Alternatively, a hard singleton would raise an error."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from abc import ABCMeta


class _SingletonMeta(ABCMeta):
  """This class is an implement details. Just walk away..."""
  _instances = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super().__call__(*args, **kwargs)
    return cls._instances[cls]


class _SingletonMixin:
  """This class is an implement details. Just walk away..."""
  _instances = {}

  def __new__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super().__new__(cls)
    return cls._instances[cls]


class _SingletonClass(_SingletonMixin, metaclass=_SingletonMeta):
  """This singleton is a placeholder removing the need to set a metaclass
  with a keyword argument. Instead, singleton classes should just inherit
  from this class."""
  pass


class SingletonClass(_SingletonClass):
  """LOL"""
