"""
TestAttriBoxContainerArgument subclasses 'DescTest' from the
'tests.test_desc' package and pins how 'AttriBox' builds a builtin
container field, 'list', 'tuple', 'set', 'frozenset' or 'dict', from a
single argument. The argument is converted as a whole, as the constructor
itself would convert it, so 'AttriBox[list](range(3))' holds '[0, 1, 2]'.
It used to become the one element of a new container, as '[range(0, 3)]'.
A 'str', 'bytes' or 'bytearray' is refused instead of being split into
characters or integers, since iterating one is rarely what was meant.
Several arguments remain the elements, and an assigned tuple remains the
argument list the container is built from.
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
  TestAttriBoxContainerArgument provides tests for container field types
  built from a single argument, through the default and through
  assignment, on 'AttriBox' and on 'FixBox', which shares its build.
  """

  def test_default_single_argument(self) -> None:
    """
    A default given as one argument that is not already of the field type
    is converted as a whole by the field type.
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

  def test_assigned_single_value(self) -> None:
    """
    An assigned value that the cast refuses, such as a 'range' or a
    generator, is converted as a whole by the field type.
    """

    class Foo:
      items = AttriBox[list]()

    foo = Foo()
    foo.items = range(3)
    self.assertEqual(foo.items, [0, 1, 2])
    foo.items = (n * n for n in range(3))
    self.assertEqual(foo.items, [0, 1, 4])

  def test_default_text_refused(self) -> None:
    """
    A 'str', 'bytes' or 'bytearray' default for a container field is
    refused with 'TypeException' on the first read.
    """
    for fieldType in _CONTAINERS:
      for text in ('abc', b'abc', bytearray(b'abc')):
        with self.subTest(fieldType=fieldType.__name__, text=text):
          class Foo:
            bar = AttriBox[fieldType](text)

          with self.assertRaises(TypeException) as context:
            _ = Foo().bar
          self.assertIs(context.exception.actualObject, text)

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

  def test_non_iterable_refused(self) -> None:
    """
    A single value the field type cannot convert, such as an 'int' for a
    'list', is refused with 'TypeException' instead of becoming the one
    element of a new container.
    """

    class Foo:
      bar = AttriBox[list](5)
      baz = AttriBox[list]()

    foo = Foo()
    with self.assertRaises(TypeException):
      _ = foo.bar
    with self.assertRaises(TypeException):
      foo.baz = 5
    self.assertEqual(foo.baz, [])

  def test_several_arguments_are_elements(self) -> None:
    """
    Several default arguments remain the elements of the container.
    """

    class Foo:
      items = AttriBox[list](1, 2, 3)
      tags = AttriBox[set](1, 2)

    foo = Foo()
    self.assertEqual(foo.items, [1, 2, 3])
    self.assertEqual(foo.tags, {1, 2})

  def test_assigned_tuple_is_argument_list(self) -> None:
    """
    A tuple assigned to a 'dict' field, which the cast does not convert,
    is the argument list the dict is built from, including a tuple
    holding a single pair.
    """

    class Foo:
      mapping = AttriBox[dict]()

    foo = Foo()
    foo.mapping = ('a', 1), ('b', 2)
    self.assertEqual(foo.mapping, {'a': 1, 'b': 2})
    foo.mapping = (('c', 3),)
    self.assertEqual(foo.mapping, {'c': 3})

  def test_fix_box_shares_the_build(self) -> None:
    """
    'FixBox' builds its value the way 'AttriBox' does, so it converts a
    single argument as a whole and refuses text.
    """

    class Foo:
      items = FixBox[list](range(3))
      text = FixBox[list]('abc')

    foo = Foo()
    self.assertEqual(foo.items, [0, 1, 2])
    with self.assertRaises(TypeException):
      _ = foo.text
