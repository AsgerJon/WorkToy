"""
TestAttriBoxStorageName subclasses 'DescTest' from the 'tests.test_desc'
package and pins where the box descriptors store the value of a field:
under the private name of the field, followed by the lower-case name of
the box class and '_field_object__', so an 'AttriBox' named 'fooBar'
stores at '__foo_bar__attribox_field_object__'. The storage name says
what put it there, and the double underscore inside keeps it apart from
every name written in the '__snake_case__' style, so a box field never
reads or overwrites a dunder Python uses, the state 'Object' keeps, or a
private class attribute of the owner.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, FixBox
from worktoy.keenum import KeeNum, Kee, KeeBox
from worktoy.mcls import BaseObject

from . import DescTest


class TestAttriBoxStorageName(DescTest):
  """
  TestAttriBoxStorageName provides tests for the storage names of the box
  descriptors.
  """

  def test_storage_name(self) -> None:
    """A box stores at its private name followed by the lower-case name
    of its class and '_field_object__'."""

    class Owner:
      fooBar = AttriBox[int](1)

    owner = Owner()
    self.assertEqual(owner.fooBar, 1)
    expected = {'__foo_bar__attribox_field_object__': 1}
    self.assertEqual(vars(owner), expected)

  def test_names_python_uses(self) -> None:
    """Fields named 'init' and 'dict' hold their own defaults instead of
    reading the instance's '__init__' and '__dict__'."""

    class Owner:
      init = AttriBox[str]('u mad bro?')
      dict = AttriBox[dict]({'a': 1})

    owner = Owner()
    self.assertEqual(owner.init, 'u mad bro?')
    self.assertEqual(owner.dict, {'a': 1})

  def test_state_object_keeps(self) -> None:
    """'posArgs' on a 'BaseObject' holds its own value and leaves the
    '__pos_args__' that 'Object' keeps alone."""

    class Args(BaseObject):
      posArgs = AttriBox[tuple]((1, 2))

    args = Args()
    self.assertEqual(args.posArgs, (1, 2))
    self.assertEqual(args.__pos_args__, ())

  def test_private_class_attribute(self) -> None:
    """A private class attribute at the private name of a field, as the
    'Field' pattern declares one, no longer hides the default of a box
    field of that name."""

    class Owner:
      __value__ = None
      value = AttriBox[int](69)

    self.assertEqual(Owner().value, 69)

  def test_fix_box_and_kee_box(self) -> None:
    """'FixBox' and 'KeeBox' store the same way, each under its own class
    name."""

    class Level(KeeNum):
      LOW = Kee[int](1)
      HIGH = Kee[int](2)

    class Owner:
      init = FixBox[str]('fixed')
      dict = KeeBox[Level]('HIGH')

    owner = Owner()
    self.assertEqual(owner.init, 'fixed')
    self.assertIs(owner.dict, Level.HIGH)
    owner.dict = 'LOW'
    self.assertIs(owner.dict, Level.LOW)
    expected = {
      '__init__fixbox_field_object__',
      '__dict__keebox_field_object__',
    }
    self.assertEqual(set(vars(owner)), expected)
