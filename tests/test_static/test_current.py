"""
TestCurrent test the special 'current' descriptors used in the
'worktoy.static' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.static import _CurrentInstance, _InstanceAddress  # NOQA
from worktoy.static import _CurrentOwner, _OwnerAddress  # NOQA
from worktoy.static import _CurrentClass, _CurrentModule  # NOQA
from worktoy.waitaminute import _Attribute  # NOQA
from worktoy.static import AbstractObject
from worktoy.waitaminute import ReadOnlyError, ProtectedError

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class Foo(AbstractObject):
  """
  Foo is a simple class to test the 'Current' class.
  """
  bar = AbstractObject()


class TestCurrent(TestCase):
  """
  TestCurrent test the special 'current' descriptors used in the
  'worktoy.static' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_ad_hoc(self) -> None:
    """
    Tests that the 'Current' class can be instantiated and iterated over.
    """

  def test_from_class(self) -> None:
    """
    Tests accessing the 'current' classes directly from the owning class.
    """

    self.assertIsInstance(Foo.instance, _CurrentInstance)
    self.assertIsInstance(Foo.instanceId, _InstanceAddress)
    self.assertIsInstance(Foo.owner, _CurrentOwner)
    self.assertIsInstance(Foo.ownerId, _OwnerAddress)
    self.assertIsInstance(Foo.cls, _CurrentClass)
    self.assertIsInstance(Foo.module, _CurrentModule)

  def test_from_instance(self) -> None:
    """
    Tests accessing the 'current' classes from an instance of the owning
    class.
    """
    foo = Foo()
    self.assertIsNone(foo.instance)
    self.assertIsInstance(foo.instanceId, int)
    self.assertIsNone(foo.owner)
    self.assertIsInstance(foo.ownerId, int)
    self.assertIs(foo.cls, Foo)
    self.assertIs(foo.module, Foo.__module__)

  def test_from_descriptor(self) -> None:
    """
    Tests accessing the 'current' classes from a descriptor of the owning
    class.
    """
    foo = Foo()
    self.assertIsInstance(foo.bar, AbstractObject)
    self.assertIsInstance(foo.bar.instance, Foo)
    self.assertIs(foo.bar.owner, Foo)
    self.assertIsInstance(foo.bar.instanceId, int)
    self.assertIsInstance(foo.bar.ownerId, int)
    self.assertIs(foo.bar.cls, AbstractObject)
    self.assertIs(foo.bar.module, AbstractObject.__module__)

  def test_set_del(self) -> None:
    """
    Tests that the '_CurrentInstance' descriptor correctly raises
    'ReadOnlyError' and 'ProtectedError' when trying to set and delete
    respectively.
    """
    foo = Foo()
    with self.assertRaises(ReadOnlyError) as context:
      foo.instance = 42
    e = context.exception
    self.assertIsInstance(e, ReadOnlyError)
    self.assertEqual(e.owningInstance, foo)
    self.assertEqual(e.descriptorObject, Foo.instance)
    self.assertIsNone(e.existingValue)

    with self.assertRaises(ProtectedError) as context:
      del foo.instance
    e = context.exception
    self.assertIsInstance(e, ProtectedError)
    self.assertEqual(e.owningInstance, foo)
    self.assertEqual(e.descriptorObject, Foo.instance)
    self.assertIsNone(e.existingValue)

    class Bar:
      """
      Bar is a simple class to test the 'Current' class.
      """
      curIns = _CurrentInstance()
      curOwn = _CurrentOwner()

    bar = Bar()
    with self.assertRaises(ReadOnlyError) as context:
      bar.curIns = 42
    e = context.exception
    self.assertIsInstance(e, ReadOnlyError)
    self.assertEqual(e.owningInstance, bar)
    self.assertEqual(e.descriptorObject, Bar.curIns)
    self.assertIsNone(e.existingValue)
    with self.assertRaises(AttributeError) as context:
      del bar.curIns
    e = context.exception
    expected = """object has no attribute"""
    self.assertIn(expected, str(e))

  def test_descriptor_only_from_free(self) -> None:
    """
    Tests the exceptions raised when calling descriptor relevant methods
    on an 'AbstractObject' object when it is free.
    """
    foo = Foo()
    self.assertIsNone(foo.instance)
    self.assertIsNone(foo.owner)
    with self.assertRaises(ReadOnlyError) as context:
      foo.instance = 'breh'
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, ReadOnlyError)
    self.assertEqual(e.owningInstance, foo)
    self.assertEqual(e.descriptorObject, Foo.instance)
    self.assertIsNone(e.existingValue)

    with self.assertRaises(ProtectedError) as context:
      del foo.instance
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, ProtectedError)
    self.assertEqual(e.owningInstance, foo)
    self.assertEqual(e.descriptorObject, Foo.instance)
    self.assertIsNone(e.existingValue)

    with self.assertRaises(ReadOnlyError) as context:
      foo.owner = 'breh'
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, ReadOnlyError)
    self.assertEqual(e.owningInstance, foo)
    self.assertEqual(e.descriptorObject, Foo.owner)
    self.assertIsNone(e.existingValue)

    with self.assertRaises(ProtectedError) as context:
      del foo.owner
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, ProtectedError)
    self.assertEqual(e.owningInstance, foo)
    self.assertEqual(e.descriptorObject, Foo.owner)
    self.assertIsNone(e.existingValue)

  def test_current_owner(self) -> None:
    """
    Tests setting a '_CurrentOwner' descriptor to a class that is not a
    subclass of 'AbstractObject'.
    """

    class Bar:
      """
      Bar is a simple class to test the 'Current' class.
      """
      curOwn = _CurrentOwner()

    setattr(Bar, '__current_owner__', None)
    bar = Bar()
    setattr(Bar, '__field_owner__', object)
    self.assertIsNotNone(bar.curOwn)
    setattr(Bar, '__field_owner__', None)
    bar = Bar()
    self.assertIsNone(bar.curOwn)

    with self.assertRaises(ReadOnlyError) as context:
      bar.curOwn = 'breh'
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, ReadOnlyError)
    self.assertEqual(e.owningInstance, bar)
    self.assertEqual(e.descriptorObject, Bar.curOwn)
    self.assertIsNone(e.existingValue)

    with self.assertRaises(ProtectedError) as context:
      del bar.curOwn
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, ProtectedError)
    self.assertEqual(e.owningInstance, bar)
    self.assertEqual(e.descriptorObject, Bar.curOwn)
    self.assertIsNone(e.existingValue)

    try:
      delattr(bar, '__current_owner__', )
    except AttributeError:
      if """object has no attribute""" in str(e):
        pass
    with self.assertRaises(ReadOnlyError) as context:
      bar.curOwn = 420
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, ReadOnlyError)
    self.assertEqual(e.owningInstance, bar)
    self.assertEqual(e.descriptorObject, Bar.curOwn)
    self.assertIsNone(e.existingValue)

    with self.assertRaises(ProtectedError) as context:
      del bar.curOwn
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIsInstance(e, ProtectedError)
    self.assertEqual(e.owningInstance, bar)
    self.assertEqual(e.descriptorObject, Bar.curOwn)
    self.assertIsNone(e.existingValue)
