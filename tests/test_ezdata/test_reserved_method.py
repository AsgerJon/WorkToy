"""
TestReservedMethod subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that an 'EZData' class body may not define
'__setattr__'. EZData generates that method for every class, casting
each field assignment on a non-frozen class and refusing it on a frozen
one, and a replacement could break the guarantee that every field holds
a value of its declared type. The class body fails at the offending
line with 'ReservedMethodError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute.ezdata import ReservedMethodError

from . import EZTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestReservedMethod(EZTest):
  """
  TestReservedMethod provides tests for the refusal of a class-body
  '__setattr__' in 'EZData' classes.
  """

  def test_setattr_raises(self) -> None:
    """
    Defining '__setattr__' raises 'ReservedMethodError' while the class
    is being built. The exception names the method and the class, and it
    is an 'AttributeError', like 'ReservedFieldError'.
    """
    with self.assertRaises(ReservedMethodError) as context:
      class Holder(EZData):  # noqa: F841
        x = EZField[int](0)

        def __setattr__(self, key: str, value: Any) -> None: ...
    e = context.exception
    self.assertIsInstance(e, AttributeError)
    self.assertEqual(e.name, '__setattr__')
    self.assertEqual(e.space.getClassName(), 'Holder')
    self.assertIn('Holder', str(e))
    self.assertIn('__setattr__', str(e))
    self.assertEqual(str(e), repr(e))

  def test_setattr_raises_on_frozen(self) -> None:
    """
    A frozen class refuses a class-body '__setattr__' the same way, even
    though its generated '__setattr__' refuses every assignment anyway.
    """
    with self.assertRaises(ReservedMethodError):
      class Holder(EZData, frozen=True):  # noqa: F841
        x = EZField[int](0)

        def __setattr__(self, key: str, value: Any) -> None: ...

  def test_setattr_raises_for_any_value(self) -> None:
    """
    The name alone decides. Binding '__setattr__' to something other
    than a function defined in the body, such as 'object.__setattr__',
    raises as well.
    """
    with self.assertRaises(ReservedMethodError):
      class Holder(EZData):  # noqa: F841
        __setattr__ = object.__setattr__
