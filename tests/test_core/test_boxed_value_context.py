"""
TestBoxedValueContext subclasses 'CoreTest' and pins what 'instance' and
'owner' mean on a value an 'AttriBox' created. The box tags the value
with '__field_box__', '__field_name__' and '__field_owner__', so the
value is placed on no class yet carries a field name, which used to make
'Object.getContextInstance' take it for a placed descriptor and raise
'WithoutException' out of 'hasattr' and 'inspect.getmembers'. Inside the
frame of the box that made it, during a read, the value answers
'instance' and 'owner' through the box; outside any frame it is an
ordinary object holding no context, so it raises 'AttributeError',
'hasattr' answers False and 'inspect' walks it. A placed descriptor read
outside a frame still raises 'WithoutException', and a value no box made
is as it was.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import inspect

from worktoy.core import Object
from worktoy.desc import AttriBox, SymbolicName
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import WithoutException

from . import CoreTest


class Bare(Object):
  """Bare is a plain 'Object' subclass a box can build."""


class Owner(BaseObject):
  """Owner holds a box of 'Bare' and watches a read of it."""

  bare = AttriBox[Bare]()
  name = AttriBox[SymbolicName]('font', 'size')

  @bare.onGet
  def _onGetBare(self, value: Bare) -> None:
    self.insideInstance = value.instance
    self.insideOwner = value.owner


class TestBoxedValueContext(CoreTest):
  """
  TestBoxedValueContext provides tests for the context a boxed value
  answers with.
  """

  def test_inside_the_frame(self) -> None:
    """During the read that built or fetched it, the value answers through
    the box: the instance read from and the owner class."""
    owner = Owner()
    value = owner.bare
    self.assertIs(owner.insideInstance, owner)
    self.assertIs(owner.insideOwner, Owner)
    self.assertIs(value.__field_box__, Owner.__dict__['bare'])

  def test_outside_any_frame(self) -> None:
    """Held after the read, the value is an ordinary object: no context,
    'hasattr' answers False, 'inspect' walks it."""
    value = Owner().bare
    with self.assertRaises(AttributeError):
      _ = value.instance
    with self.assertRaises(AttributeError):
      _ = value.owner
    self.assertFalse(hasattr(value, 'instance'))
    self.assertFalse(hasattr(value, 'owner'))
    names = [name for name, _ in inspect.getmembers(value)]
    self.assertIn('getContextInstance', names)

  def test_boxed_symbolic_name(self) -> None:
    """Any 'Object' a box builds behaves the same, 'SymbolicName' included."""
    name = Owner().name
    self.assertEqual(name.snake, 'font_size')
    self.assertFalse(hasattr(name, 'instance'))

  def test_placed_descriptor_unchanged(self) -> None:
    """A placed descriptor read outside a frame still raises
    'WithoutException'."""
    with self.assertRaises(WithoutException):
      _ = Owner.__dict__['bare'].instance
    with self.assertRaises(WithoutException):
      _ = Owner.__dict__['bare'].owner

  def test_value_no_box_made(self) -> None:
    """A value no class holds and no box made answers as before."""
    self.assertFalse(hasattr(Bare(), 'instance'))
    self.assertFalse(hasattr(Bare(), 'owner'))
