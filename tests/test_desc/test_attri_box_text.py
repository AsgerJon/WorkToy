"""
TestAttriBoxText subclasses 'DescTest' from the 'tests.test_desc' package
and pins how 'AttriBox' builds a text field, one of field type 'str',
'bytes' or 'bytearray', from a single value. The value goes through
'resolveText', which defers to 'typeCast', instead of through the field
type's constructor, which would accept almost anything: 'str(None)' is
'None', and 'bytes(5)' is five zero bytes. So a text field takes any of
the three text types, converted as UTF-8, and refuses everything else
with 'TypeException', for the default as for an assignment. Several
arguments still go to the constructor, which is how an encoding is
named.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, FixBox
from worktoy.waitaminute import TypeException

from . import DescTest


class TestAttriBoxText(DescTest):
  """
  TestAttriBoxText provides tests for text field types on 'AttriBox' and
  on 'FixBox', which shares its build.
  """

  def test_assigned_non_text_refused(self) -> None:
    """Assigning anything but text to a text field raises
    'TypeException', and the field keeps its value."""

    class Foo:
      name = AttriBox[str]('x')
      data = AttriBox[bytes](b'x')
      buffer = AttriBox[bytearray](bytearray(b'x'))

    foo = Foo()
    for fieldName in ('name', 'data', 'buffer'):
      before = getattr(foo, fieldName)
      for value in (None, 5, [1, 2], object()):
        with self.subTest(field=fieldName, value=repr(value)):
          with self.assertRaises(TypeException):
            setattr(foo, fieldName, value)
          self.assertEqual(getattr(foo, fieldName), before)

  def test_several_arguments_use_the_constructor(self) -> None:
    """Several arguments, or keyword arguments, as in naming an encoding,
    still go to the field type's constructor for the default. An assigned
    tuple is a tuple, not an argument list, and is refused."""

    class Foo:
      name = AttriBox[str](b'\xe6', 'latin-1')
      word = AttriBox[str](b'\xe5', encoding='latin-1')

    foo = Foo()
    self.assertEqual(foo.name, 'æ')
    self.assertEqual(foo.word, 'å')
    with self.assertRaises(TypeException):
      foo.name = (b'\xf8', 'latin-1')
    self.assertEqual(foo.name, 'æ')

  def test_mutable_default_owned_per_instance(self) -> None:
    """A 'bytearray' default already of the field type is still copied
    for each instance rather than shared."""

    class Foo:
      buffer = AttriBox[bytearray](bytearray(b'x'))

    one, two = Foo(), Foo()
    one.buffer.extend(b'y')
    self.assertEqual(two.buffer, bytearray(b'x'))
    self.assertIsNot(one.buffer, two.buffer)

  def test_fix_box_refuses_non_text(self) -> None:
    """A 'FixBox' text field refuses non-text the same way, and the
    refusal does not use up its single write."""

    class Foo:
      name = FixBox[str]()

    foo = Foo()
    with self.assertRaises(TypeException):
      foo.name = None
    foo.name = b'abc'
    self.assertEqual(foo.name, 'abc')
