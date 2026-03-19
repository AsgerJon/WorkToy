"""
TestStyle subclasses 'MarkworkTest' and provides tests for the 'Style'
class in the 'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import operator
from typing import TYPE_CHECKING

from worktoy.markwork import Style, ParagraphBlock, Block
from worktoy.waitaminute import TypeException
from . import MarkworkTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class Foo(Block):
  """
  Foo subclasses 'Paragraph' and provides an example of how one might use
  'Paragraph' in a test case.
  """

  bar = Style()


class TestStyle(MarkworkTest):
  """
  TestStyle subclasses 'MarkworkTest' and provides tests for the 'Style'
  class in the 'worktoy.markwork' package.
  """

  def setUp(self, ) -> None:
    """
    Populates the 'styles' attribute with all possible flag combinations.
    """
    super().setUp()
    self.styles4Bool = []
    self.styles3Bool = []
    self.styles2Bool = []
    self.styles1Bool = []
    for i in range(16):
      args = (*(bool(i & (1 << j)) for j in range(4)),)
      self.styles4Bool.append(Style(*args))
      if i < 8:
        self.styles3Bool.append(Style(*args[:3]))
      if i < 4:
        self.styles2Bool.append(Style(*args[:2]))
      if i < 2:
        self.styles1Bool.append(Style(*args[:1]))
    self.styles = (
      *self.styles4Bool,
      *self.styles3Bool,
      *self.styles2Bool,
      *self.styles1Bool,
      )

  def test_init_bool(self, ) -> None:
    """
    Testing the four 'bool' overload constructor.
    """
    keys = (*Style.__key_groups__.keys(),)
    for i, style in enumerate(self.styles4Bool):
      self.assertIsInstance(style, Style)
      for j, key in enumerate(keys):
        expectedFlag = bool(i & (1 << j))
        actualFlag = getattr(style, key)
        self.assertEqual(expectedFlag, actualFlag)

    for i, style in enumerate(self.styles3Bool):
      self.assertIsInstance(style, Style)
      for j, key in enumerate(keys[:3]):
        expectedFlag = bool(i & (1 << j))
        actualFlag = getattr(style, key)
        self.assertEqual(expectedFlag, actualFlag)

    for i, style in enumerate(self.styles2Bool):
      self.assertIsInstance(style, Style)
      for j, key in enumerate(keys[:2]):
        expectedFlag = bool(i & (1 << j))
        actualFlag = getattr(style, key)
        self.assertEqual(expectedFlag, actualFlag)

    for i, style in enumerate(self.styles1Bool):
      self.assertIsInstance(style, Style)
      for j, key in enumerate(keys[:1]):
        expectedFlag = bool(i & (1 << j))
        actualFlag = getattr(style, key)
        self.assertEqual(expectedFlag, actualFlag)

  def test_init_empty(self) -> None:
    """
    Testing the empty constructor.
    """
    style = Style()
    self.assertIsInstance(style, Style)
    for key in Style.__key_groups__.keys():
      actualFlag = getattr(style, key)
      self.assertFalse(actualFlag)

  def test_init_other(self) -> None:
    """
    Testing the 'other' constructor.
    """
    for other in self.styles:
      style = Style(other)
      self.assertIsInstance(style, Style)
      for key in Style.__key_groups__.keys():
        expectedFlag = getattr(other, key)
        actualFlag = getattr(style, key)
        self.assertEqual(expectedFlag, actualFlag)

  def test_init_kwargs(self) -> None:
    """
    Testing the constructor with keyword arguments.
    """
    keys = (*Style.__key_groups__.keys(),)
    for i in range(16):
      kwargs = dict()
      for j, key in enumerate(keys):
        kwargs[key] = bool(i & (1 << j))
      style = Style(**kwargs)
      self.assertIsInstance(style, Style)
      for key in keys:
        expectedFlag = kwargs[key]
        actualFlag = getattr(style, key)
        self.assertEqual(expectedFlag, actualFlag)
      if i < 8:
        style = Style(**{k: kwargs[k] for k in keys[:3]})
        self.assertIsInstance(style, Style)
        for key in keys[:3]:
          expectedFlag = kwargs[key]
          actualFlag = getattr(style, key)
          self.assertEqual(expectedFlag, actualFlag)
      if i < 4:
        style = Style(**{k: kwargs[k] for k in keys[:2]})
        self.assertIsInstance(style, Style)
        for key in keys[:2]:
          expectedFlag = kwargs[key]
          actualFlag = getattr(style, key)
          self.assertEqual(expectedFlag, actualFlag)
      if i < 2:
        style = Style(**{k: kwargs[k] for k in keys[:1]})
        self.assertIsInstance(style, Style)
        for key in keys[:1]:
          expectedFlag = kwargs[key]
          actualFlag = getattr(style, key)
          self.assertEqual(expectedFlag, actualFlag)

  def test_init_mix(self, ) -> None:
    """
    Testing the constructor with a mix of 'other' and keyword arguments.
    """
    keys = (*Style.__key_groups__.keys(),)
    for i in range(16):
      kwargs = dict()
      args = []
      for j, key in enumerate(keys):
        kwargs[key] = bool(i & (1 << j))
        args.append(kwargs[key])
      argsOnly = Style(*args)
      kwargsOnly = Style(**kwargs)
      for key in keys:
        expectedFlag = kwargs[key]
        actualFlagArgsOnly = getattr(argsOnly, key)
        actualFlagKwargsOnly = getattr(kwargsOnly, key)
        self.assertEqual(expectedFlag, actualFlagArgsOnly)
        self.assertEqual(expectedFlag, actualFlagKwargsOnly)

    mix1 = Style(True, underline=True)
    self.assertEqual(mix1.italic, True)
    self.assertEqual(mix1.bold, False)
    self.assertEqual(mix1.underline, True)
    self.assertEqual(mix1.strikethrough, False)

    mix2 = Style(True, False, strikethrough=True)
    self.assertEqual(mix2.italic, True)
    self.assertEqual(mix2.bold, False)
    self.assertEqual(mix2.underline, False)
    self.assertEqual(mix2.strikethrough, True)

    mix3 = Style(True, False, False, strikethrough=True)
    self.assertEqual(mix3.italic, True)
    self.assertEqual(mix3.bold, False)
    self.assertEqual(mix3.underline, False)
    self.assertEqual(mix3.strikethrough, True)

  def test_bad_init(self, ) -> None:
    """
    This method covers the branch where a keyword argument tries to assign
    a value of wrong type. A 'bool' object is expected.
    """

    with self.assertRaises(TypeException) as context:
      _ = Style(italic='breh')
    e = context.exception
    self.assertEqual(e.varName, 'italic')
    self.assertEqual(e.actualObject, 'breh')
    self.assertIs(e.actualType, str)
    self.assertIn(bool, e.expectedTypes, )

  def test_eq(self, ) -> None:
    """
    This method tests the implementation of the equality operator when
    comparing between 'Style' objects.
    """
    for i, left in enumerate(self.styles4Bool):
      for j, right in enumerate(self.styles4Bool):
        if i == j:
          self.assertEqual(left, right)
          continue
        self.assertNotEqual(left, right)

  def test_binary_ops(self, ) -> None:
    """
    This method test the implementation of the bitwise operations:
    '__and__', '__or__' and '__xor__'.
    """
    bitWiseOps = operator.and_, operator.or_, operator.xor
    for left in self.styles4Bool:
      for right in self.styles4Bool:
        for op in bitWiseOps:
          italic = op(left.italic, right.italic)
          bold = op(left.bold, right.bold)
          underline = op(left.underline, right.underline)
          strikethrough = op(left.strikethrough, right.strikethrough)
          expected = Style(italic, bold, underline, strikethrough)
          actual = op(left, right)
          self.assertEqual(expected, actual)

  def test_binary_not_implemented(self, ) -> None:
    """
    This method tests the binary options between 'Style' objects and
    objects of other types that should not implement a reflection of the
    operation.
    """
    notStyles = object, object(), print, 'breh'
    style = Style()
    bitWiseNames = '__and__', '__or__', '__xor__', '__eq__'
    bitWiseOps = (*(getattr(Style, name) for name in bitWiseNames),)
    for notStyle in notStyles:
      for op in bitWiseOps:
        with self.subTest(notStyle=notStyle, op=op):
          result = op(style, notStyle)
          self.assertIs(result, NotImplemented)

  def test_apply(self, ) -> None:
    """
    This method tests the 'apply' method of 'Style' objects.
    """
    self.randomWord.colCount = 4
    self.randomWord.charCount = 80
    contents = self.randomWord._getRow()
    for style in self.styles:
      for content in contents:
        styledContent = style.apply(content)
        self.assertIsInstance(styledContent, str)

  def test_fallback_header_level(self, ) -> None:
    """
    This method tests the fallback header level of 'Style' objects when
    applying to a header.
    """

    self.randomLorem.charCount = 80
    self.randomLorem.colCount = 4

    class Foo:
      style = Style()

    contents = (
      *self.randomLorem._getRow(),
      *self.randomWord._getRow(),
      )

    for content in contents:
      styledContent = Foo.style.apply(content)
      self.assertIsInstance(styledContent, str)

  def test_str_repr(self, ) -> None:
    """
    This method tests the '__str__' and '__repr__' methods of 'Style'
    objects.
    """
    for style in self.styles:
      for key in Style.__key_groups__.keys():
        flag = getattr(style, key)
        kwarg = """%s=%s""" % (key, 'True' if flag else 'False')
        self.assertIn(kwarg, str(style))
        self.assertIn(kwarg, repr(style))

  def test_getitem(self, ) -> None:
    """
    This method tests the '__getitem__' method of 'Style' objects.
    """
    keys = (*Style.__key_groups__.keys(),)
    for style in self.styles:
      for key in keys:
        expectedFlag = getattr(style, key)
        actualFlag = style[key]
        self.assertEqual(expectedFlag, actualFlag)

  def test_setitem(self, ) -> None:
    """
    This method tests the '__setitem__' method of 'Style' objects.
    """
    keys = (*Style.__key_groups__.keys(),)
    for style in self.styles4Bool:
      newStyle = Style()
      for key in keys:
        newStyle[key] = getattr(style, key)
      self.assertEqual(style, newStyle)

  def test_get_set_item_bad_key(self, ) -> None:
    """
    This method covers the branches of '__getitem__' and '__setitem__'
    where a 'KeyError' is raised due to an invalid key.
    """
    self.randomWord.colCount = 69
    keys = (*Style.__key_groups__.keys(),)
    words = (*(w for w in self.randomWord._getRow() if w not in keys),)
    style = Style()
    for word in words:
      with self.subTest(word=word):
        with self.assertRaises(KeyError) as context:
          _ = style[word]
        e = context.exception
        self.assertEqual(e.args[0], word)
        with self.assertRaises(KeyError) as context:
          style[word] = True
        e = context.exception
        self.assertEqual(e.args[0], word)

  def test_setitem_bad_type(self, ) -> None:
    """
    This method covers the branch of '__setitem__' where a 'TypeException' is
    raised due to an invalid value type.
    """
    keys = (*Style.__key_groups__.keys(),)
    notBools = object, object(), print, 'breh'
    style = Style()
    for key in keys:
      for notBool in notBools:
        with self.subTest(key=key, notBool=notBool):
          with self.assertRaises(TypeException) as context:
            style[key] = notBool
          e = context.exception
          self.assertEqual(e.varName, key)
          self.assertEqual(e.actualObject, notBool)
          self.assertIs(e.actualType, type(notBool))
          self.assertIn(bool, e.expectedTypes, )
