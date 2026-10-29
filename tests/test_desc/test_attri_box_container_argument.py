"""
TestAttriBoxContainerArgument subclasses 'DescTest' from the
'tests.test_desc' package and pins how 'AttriBox' builds a builtin
container field, 'list', 'tuple', 'set', 'frozenset' or 'dict'. No rule
stands between the author and the constructor: a lone default argument
that is not already of the field type is the one argument of the
constructor, so 'AttriBox[list](range(3))' holds '[0, 1, 2]' and
'AttriBox[list]('abc')' holds what 'list('abc')' is, several arguments
are refused as the constructor refuses them, and an assigned value is an
instance of the field type or is refused, since containers are no cast
targets. The build used to take several arguments as the elements and to
refuse a lone text, and an assigned tuple used to be the argument list.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, FixBox
from worktoy.waitaminute import TypeException

from . import DescTest

_CONTAINERS = (list, tuple, set, frozenset, dict)


class TestAttriBoxContainerArgument(DescTest):
  """
  TestAttriBoxContainerArgument provides tests for container field types,
  through the default and through assignment, on 'AttriBox' and on
  'FixBox', which shares its build.
  """

  def test_default_single_argument(self) -> None:
    """
    A default given as one argument that is not already of the field type
    is the one argument of the constructor.
    """

    class Foo:
      items = AttriBox[list](range(3))
      pair = AttriBox[list]((1, 2))
      frozen = AttriBox[tuple]([1, 2])
      tags = AttriBox[set]([1, 2])
      marks = AttriBox[frozenset]([1, 2])
      mapping = AttriBox[dict]([('a', 1)])

    foo = Foo()
    self.assertEqual(foo.items, [0, 1, 2])
    self.assertEqual(foo.pair, [1, 2])
    self.assertEqual(foo.frozen, (1, 2))
    self.assertEqual(foo.tags, {1, 2})
    self.assertEqual(foo.marks, frozenset({1, 2}))
    self.assertEqual(foo.mapping, {'a': 1})

  def test_assigned_value_must_be_an_instance(self) -> None:
    """
    An assigned value is stored only as an instance of the field type.
    Another iterable, a 'range', a generator, a tuple for a 'list' or a
    tuple of pairs for a 'dict', is refused, and the field keeps its
    value.
    """

    class Foo:
      items = AttriBox[list]()
      mapping = AttriBox[dict]()

    foo = Foo()
    for value in (range(3), (n * n for n in range(3)), (1, 2)):
      with self.subTest(value=repr(value)):
        with self.assertRaises(TypeException):
          foo.items = value
    self.assertEqual(foo.items, [])
    with self.assertRaises(TypeException):
      foo.mapping = ('a', 1), ('b', 2)
    self.assertEqual(foo.mapping, {})
    foo.items = [1, 2]
    foo.mapping = {'a': 1}
    self.assertEqual((foo.items, foo.mapping), ([1, 2], {'a': 1}))

  def test_assigned_text_refused(self) -> None:
    """
    A 'str', 'bytes' or 'bytearray' assigned to a container field is
    refused with 'TypeException', and the field keeps its value.
    """
    for fieldType in _CONTAINERS:
      for text in ('abc', b'abc', bytearray(b'abc')):
        with self.subTest(fieldType=fieldType.__name__, text=text):
          class Foo:
            bar = AttriBox[fieldType]()

          foo = Foo()
          before = foo.bar
          with self.assertRaises(TypeException) as context:
            foo.bar = text
          self.assertIs(context.exception.actualObject, text)
          self.assertEqual(foo.bar, before)

  def test_fix_box_shares_the_build(self) -> None:
    """
    'FixBox' builds its value the way 'AttriBox' does.
    """

    class Foo:
      items = FixBox[list](range(3))
      text = FixBox[list]('abc')

    foo = Foo()
    self.assertEqual(foo.items, [0, 1, 2])
    self.assertEqual(foo.text, ['a', 'b', 'c'])
