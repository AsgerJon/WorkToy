"""
PromiseQuickDesc promises 'QuickDesc' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import QuickDesc
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError


class PromiseQuickDesc(TestCase):
  """
  'QuickDesc(key)' is a read-only attribute that reads the private
  attribute 'key' of the instance. Writing it raises 'ReadOnlyError'
  and deleting it raises 'ProtectedError', both 'AttributeError'. A
  '__getattr__' of the class, asked when the private attribute is
  missing, is asked about the public name, never about the private key.
  Source: the 'QuickDesc' docstring and its example, and the 1.1.0
  changelog entry "QuickDesc reads its slot past '__getattr__'".
  """

  def test_reads(self) -> None:
    class Box:
      __value__ = 42
      value = QuickDesc('__value__')

    self.assertEqual(Box().value, 42)

  def test_write_refused(self) -> None:
    class Box:
      __value__ = 42
      value = QuickDesc('__value__')

    box = Box()
    with self.assertRaises(ReadOnlyError) as context:
      box.value = 7
    e = context.exception
    self.assertIsInstance(e, AttributeError)
    self.assertIs(e.instance, box)
    self.assertIs(e.desc, vars(Box)['value'])
    self.assertEqual(e.newVal, 7)
    self.assertEqual(box.value, 42)

  def test_delete_refused(self) -> None:
    class Box:
      __value__ = 42
      value = QuickDesc('__value__')

    box = Box()
    with self.assertRaises(ProtectedError) as context:
      del box.value
    e = context.exception
    self.assertIsInstance(e, AttributeError)
    self.assertIs(e.instance, box)
    self.assertIs(e.desc, vars(Box)['value'])
    #  'oldVal' holds the value only "if known".
    self.assertIn(e.oldVal, (None, 42))

  def test_getattr_asked_public_name(self) -> None:
    class Lazy:
      value = QuickDesc('__value__')

      def __getattr__(self, name: str) -> str:
        return 'asked about %s' % name

    self.assertEqual(Lazy().value, 'asked about value')
