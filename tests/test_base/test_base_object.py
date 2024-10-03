"""TestBaseobject tests that the BaseObject class functions correctly. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import BaseMetaclass
from worktoy.base import BaseObject
from unittest import TestCase


class SomeClass(BaseObject):
  """This class inherits BaseObject. """


class TestBaseobject(TestCase):
  """TestBaseobject tests that the BaseObject class functions correctly. """

  def test_init_methods(self, ) -> None:
    """Tests that the BaseObject class replaces the __init__ and
    __init_subclass__ on the 'object' class. """

    for (key, val) in object.__dict__.items():
      if not callable(val):
        continue
      if key in ['__init__', '__init_subclass__', '__subclasshook__']:
        self.assertNotEqual(val, getattr(BaseObject, key))
      elif key not in BaseMetaclass.__dict__:
        self.assertIs(val, getattr(BaseObject, key))
