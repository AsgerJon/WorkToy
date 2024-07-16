"""TesterClass01"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

ic.configureOutput(includeContext=True)


class SomeMeta(type):  # metaclass
  #  This metaclass tries to apply keyword arguments to the class after it
  #  is initialized.

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs):
    """This method is called before the class object is created."""
    print('__prepare__')
    return {}

  def __new__(mcls, name: str, bases: tuple, namespace: dict, **kwargs):
    """This method is called to create the class object."""
    print('__new__')
    return super().__new__(mcls, name, bases, namespace, **kwargs)

  def __init__(cls, name, bases, namespace, **kwargs):
    """This method is called after the class object has been created."""
    print('__init__')
    super().__init__(name, bases, namespace)
    for (key, val) in kwargs.items():
      setattr(cls, key, val)
