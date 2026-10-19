"""
TestBlackList tests that explicitly blacklisted types correctly raise
'BlackListedType' when used in the class body of an EZData class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import Alias
from worktoy.dispatch import Dispatcher
from worktoy.ezdata import EZData, _BLACK_LISTED_TYPES, EZField
from worktoy.waitaminute.ezdata import BlackListedType

from . import EZTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestBlackList(EZTest):
  """
  TestBlackList tests that explicitly blacklisted types correctly raise
  'BlackListedType' when used in the class body of an EZData class.
  """

  def test_alias(self) -> None:
    """
    This method tests that 'Alias' is correctly blacklisted in the private
    '_BLACK_LISTED_TYPES' tuple, and that inclusion of it in the class body
    of an 'EZData' class raises a 'BlackListedType' exception.
    """

    self.assertIn(Alias, _BLACK_LISTED_TYPES)

    with self.assertRaises(BlackListedType) as context:
      class Foo(EZData):
        good = EZField[int](69)
        bad = Alias('good')
    e = context.exception
    self.assertEqual(e.clsName, 'Foo')
    self.assertEqual(e.key, 'bad')
    self.assertEqual(e.value.__real_name__, Alias('good').__real_name__)
    self.assertIn("'Foo'", str(e))
    self.assertIn("'bad'", str(e))
    self.assertIn("'Alias'", str(e))
    self.assertEqual(str(e), repr(e))

  def test_dispatcher(self) -> None:
    """
    This method tests that a hand-built 'Dispatcher' is blacklisted as
    well: in an 'EZData' class body it used to become a field, and its
    first decorator then failed as a duplicate field. The refusal names
    the class, the name and the type.
    """
    self.assertIn(Dispatcher, _BLACK_LISTED_TYPES)

    with self.assertRaises(BlackListedType) as context:
      class Scaled(EZData):
        k = EZField[int](1)
        scale = Dispatcher()
    e = context.exception
    self.assertEqual(e.clsName, 'Scaled')
    self.assertEqual(e.key, 'scale')
    self.assertIsInstance(e.value, Dispatcher)
    self.assertIn("'Dispatcher'", str(e))
