"""
TestObjectNaming tests the placement and naming of 'Object' from
'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os

from worktoy.core import Object
from worktoy.core import _object
from worktoy.waitaminute import MissingVariable, TypeException
from . import CoreTest, Counted, Noisy


class TestObjectNaming(CoreTest):
  """
  A descriptor learns the class and name it is placed at, reports them,
  derives a private name from the field name, and knows the directory of
  its own source file. The tests pin the placement with its hook, the
  fallbacks of an unplaced object, the private name with its cache and
  its two refusals, and the directory.
  """

  def test_placement_recorded(self) -> None:
    Noisy.placements.clear()

    class Owner:
      n = Noisy()

    self.assertIs(Owner.n.getFieldOwner(), Owner)
    self.assertEqual(Owner.n.getFieldName(), 'n')
    self.assertEqual(Noisy.placements, [('Owner', 'n')])

  def test_set_name_by_hand(self) -> None:
    desc = Object()
    desc.__set_name__(int, 'k')
    self.assertIs(desc.getFieldOwner(), int)
    self.assertEqual(desc.getFieldName(), 'k')

  def test_unplaced_fallbacks(self) -> None:
    self.assertIsNone(Object().getFieldOwner())
    self.assertEqual(Object().getFieldName(), '<Object>')
    self.assertEqual(Counted().getFieldName(), '<Counted>')

  def test_private_name(self) -> None:
    class Owner:
      fooBar = Counted()
      plain = Counted()
      FooBar = Counted()
      a1B = Counted()

    self.assertEqual(Owner.fooBar.getPrivateName(), '__foo_bar__')
    self.assertEqual(Owner.plain.getPrivateName(), '__plain__')
    self.assertEqual(Owner.FooBar.getPrivateName(), '__foo_bar__')
    self.assertEqual(Owner.a1B.getPrivateName(), '__a1_b__')

  def test_private_name_cached(self) -> None:
    class Owner:
      fooBar = Counted()

    first = Owner.fooBar.getPrivateName()
    Owner.fooBar.__set_name__(Owner, 'other')
    self.assertEqual(Owner.fooBar.getPrivateName(), first)

  def test_private_name_unplaced_refused(self) -> None:
    desc = Object()
    with self.assertRaises(MissingVariable) as context:
      desc.getPrivateName()
    self.assertEqual(context.exception.varName, '__field_name__')
    self.assertIs(context.exception.instance, desc)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'Object.__field_name__: str'", str(context.exception))

  def test_private_name_cache_checked(self) -> None:
    desc = Object()
    desc.__set_name__(int, 'k')
    object.__setattr__(desc, '__private_name__', 42)
    with self.assertRaises(TypeException) as context:
      desc.getPrivateName()
    self.assertEqual(context.exception.varName, '__private_name__')
    self.assertEqual(context.exception.actualObject, 42)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'__private_name__'", str(context.exception))

  def test_directory(self) -> None:
    from . import _counted
    self.assertEqual(Object().directory,
                     os.path.dirname(os.path.abspath(_object.__file__)))
    self.assertEqual(Counted().directory,
                     os.path.dirname(os.path.abspath(_counted.__file__)))
