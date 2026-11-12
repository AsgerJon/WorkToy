"""
TestUnpack tests 'unpack' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys

from worktoy.utilities import unpack
from worktoy.waitaminute import UnpackException, RedundantKeyword
from . import UtilitiesTest, Refusing

HERE = sys._getframe().f_code.co_filename


class TestUnpack(UtilitiesTest):
  """
  'unpack' flattens whatever iterables its arguments hold into one
  tuple, so a function taking '*args' accepts its values one by one or
  in any nesting of lists and tuples alike. Text stays whole, an object
  that claims to iterate and refuses stays whole, a container holding
  itself stays whole, and the strict default refuses a call in which
  nothing iterated. The tests pin each of these, the shallow mode, and
  the warning given for a keyword that is no option.
  """

  def test_docstring_examples(self) -> None:
    self.assertEqual(unpack([1, 2], (3, [4, 5])), (1, 2, 3, 4, 5))
    self.assertEqual(unpack([1, [2, 3]], shallow=True), (1, [2, 3]))
    self.assertEqual(unpack('abc', [1, 2]), ('abc', 1, 2))

  def test_empty_call(self) -> None:
    with self.assertRaises(UnpackException) as context:
      unpack()
    self.assertEqual(context.exception.posArgs, ())
    self.assertIn('found no iterable argument', str(context.exception))
    self.assertEqual(unpack(strict=False), ())

  def test_nothing_iterable(self) -> None:
    with self.assertRaises(UnpackException) as context:
      unpack(1, 2)
    self.assertEqual(context.exception.posArgs, (1, 2))
    self.assertIn('from:\n  1\n  2\n', str(context.exception))
    self.assertEqual(unpack(1, 2, strict=False), (1, 2))

  def test_text_is_atomic(self) -> None:
    with self.assertRaises(UnpackException) as context:
      unpack('abc')
    self.assertEqual(context.exception.posArgs, ('abc',))
    self.assertIn("from:\n  'abc'\n", str(context.exception))
    self.assertEqual(unpack('abc', strict=False), ('abc',))
    out = unpack(b'ab', bytearray(b'c'), [0])
    self.assertEqual(out, (b'ab', bytearray(b'c'), 0))
    self.assertEqual(unpack(['ab', ['cd']]), ('ab', 'cd'))

  def test_deep_nesting(self) -> None:
    self.assertEqual(unpack([1, [2, [3, (4, [[5]])]]]), (1, 2, 3, 4, 5))
    self.assertEqual(unpack([[[]]]), ())

  def test_shallow(self) -> None:
    self.assertEqual(unpack([1, (2,)], [[3]], shallow=True), (1, (2,), [3]))

  def test_mixed_arguments(self) -> None:
    self.assertEqual(unpack(1, [2, 3], 4), (1, 2, 3, 4))

  def test_other_iterables(self) -> None:
    self.assertEqual(unpack(range(3)), (0, 1, 2))
    self.assertEqual(unpack({'a': 1}), ('a',))
    self.assertEqual(unpack((i * i for i in range(3))), (0, 1, 4))
    self.assertEqual(unpack({7}), (7,))

  def test_refusing_iterable_kept_whole(self) -> None:
    refusing = Refusing()
    with self.assertRaises(UnpackException) as context:
      unpack(refusing)
    self.assertEqual(context.exception.posArgs, (refusing,))
    self.assertIn('Refusing object', str(context.exception))
    self.assertEqual(unpack(refusing, strict=False), (refusing,))
    self.assertEqual(unpack([refusing, 1]), (refusing, 1))

  def test_self_containing_list_kept_whole(self) -> None:
    loop = [1]
    loop.append(loop)
    out = unpack(loop)
    self.assertEqual(len(out), 2)
    self.assertEqual(out[0], 1)
    self.assertIs(out[1], loop)
    nested = unpack([loop])
    self.assertEqual(len(nested), 2)
    self.assertIs(nested[1], loop)
    first = []
    first.append(first)
    first.append(2)
    out = unpack(first)
    self.assertEqual(len(out), 2)
    self.assertIs(out[0], first)
    self.assertEqual(out[1], 2)

  def test_result_is_tuple(self) -> None:
    self.assertIs(type(unpack([1])), tuple)
    self.assertIs(type(unpack(1, strict=False)), tuple)

  def test_unknown_keyword_warned(self) -> None:
    expected = """'worktoy.utilities.unpack' received the keyword
    'shalow', which it does not read, and went on without it! It reads:
    'shallow', 'strict'."""
    with self.assertWarns(RedundantKeyword) as context:
      line = sys._getframe().f_lineno + 1
      items = unpack([1, [2, 3]], shalow=True)
    self.assertEqual(items, (1, 2, 3))
    warning = context.warning
    self.assertIs(warning.receiver, unpack)
    self.assertEqual(warning.keyword, 'shalow')
    self.assertEqual(warning.options, ('shallow', 'strict'))
    self.assertEqual(str(warning), str.join(' ', expected.split()))
    self.assertEqual(context.filename, HERE)
    self.assertEqual(context.lineno, line)
    with self.assertWarns(RedundantKeyword):
      items = unpack(shalow=True, strict=False)
    self.assertEqual(items, ())
