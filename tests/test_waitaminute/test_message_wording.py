"""
TestMessageWording subclasses 'WaitAMinuteTest' and pins the wording of
four messages. 'ExtraPositionalException' and 'KwargsOnlyException' put
every count in the plural, as in "has 1 fields"; 'KwargsOnlyException'
named the option 'kw_only=True', where the docstrings lead with 'kwOnly';
'PhantomBoxError' wrote "a 'AttriBox'"; and 'UnboundClassHook' called a
staticmethod a plain function.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import List

from worktoy.desc import AttriBox, FastBox
from worktoy.ezdata import EZData, EZField
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import PhantomBoxError
from worktoy.waitaminute.ezdata import ExtraPositionalException
from worktoy.waitaminute.ezdata import KwargsOnlyException
from worktoy.waitaminute.meta import UnboundClassHook

from . import WaitAMinuteTest


class One(EZData):
  """One has a single field."""
  x = EZField[int](0)


class Keyed(EZData, kwOnly=True):
  """Keyed takes its field by keyword only."""
  x = EZField[int](0)


class TestMessageWording(WaitAMinuteTest):
  """
  TestMessageWording provides tests for the wording of the messages.
  """

  def test_single_field(self) -> None:
    """One field is a field, two arguments are arguments."""
    with self.assertRaises(ExtraPositionalException) as context:
      One(1, 2)
    message = str(context.exception)
    self.assertIn('has 1 field but received 2 positional arguments', message)

  def test_no_fields(self) -> None:
    """No fields are fields, one argument is an argument."""
    message = str(ExtraPositionalException(One, 0, 1))
    self.assertIn('has 0 fields but received 1 positional argument.', message)

  def test_keyword_only_option(self) -> None:
    """The option is named 'kwOnly', and one argument is an argument."""
    with self.assertRaises(KwargsOnlyException) as context:
      Keyed(1)
    message = str(context.exception)
    self.assertIn("'kwOnly=True'", message)
    self.assertIn('received 1 positional argument.', message)

  def test_keyword_only_arguments(self) -> None:
    """Two arguments are arguments."""
    message = str(KwargsOnlyException(Keyed, 2))
    self.assertIn('received 2 positional arguments.', message)

  def test_box_article(self) -> None:
    """The article suits the name of the box."""
    attriAlias = AttriBox[List[int]]
    fastAlias = FastBox[List[int]]
    self.assertIn("than an 'AttriBox'", str(PhantomBoxError(attriAlias)))
    self.assertIn("than a 'FastBox'", str(PhantomBoxError(fastAlias)))

  def test_staticmethod_hook(self) -> None:
    """A staticmethod is not called a plain function."""
    with self.assertRaises(UnboundClassHook) as context:
      class Hooked(BaseObject):  # noqa: F841
        @staticmethod
        def __class_str__() -> str:
          """A class hook without '@classmethod'."""
    message = str(context.exception)
    self.assertNotIn('plain function', message)
    self.assertIn("'@classmethod'", message)
