"""
TestNamespaceSelfReference subclasses 'CoreTest' and pins that a class
built by 'MetaType' from a plain class-body dict keeps that dict under
'__namespace__' without the dict holding itself. 'MetaType.__new__' writes
the namespace into itself under '__namespace__' so that 'type.__new__'
copies the entry into the class, and used to leave the entry behind, so
the dict of every plain 'Object' subclass contained itself.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.mcls import BaseObject, BaseSpace

from . import CoreTest


class TestNamespaceSelfReference(CoreTest):
  """
  TestNamespaceSelfReference provides tests for the '__namespace__' entry
  of a class built from a plain dict.
  """

  def test_plain_dict_not_self_referential(self) -> None:
    """The class-body dict of a plain 'Object' subclass is stored on the
    class and no longer contains itself."""

    class Plain(Object):
      pass

    space = Plain.__dict__['__namespace__']
    self.assertIsInstance(space, dict)
    self.assertNotIn('__namespace__', space)
    self.assertIn('__module__', space)

  def test_namespace_object_kept(self) -> None:
    """A class built through a namespace object keeps that object, whose
    compiled dict names the namespace as before."""

    class Framed(BaseObject):
      pass

    space = Framed.__namespace__
    self.assertIsInstance(space, BaseSpace)
    self.assertIs(space.__compiled_space__['__namespace__'], space)
