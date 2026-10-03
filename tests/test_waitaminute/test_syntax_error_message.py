"""
TestSyntaxErrorMessage subclasses 'WaitAMinuteTest' from the
'tests.test_waitaminute' package and pins that the exceptions deriving
from 'SyntaxError', 'DelException', 'QuestionableSyntax',
'UnboundClassHook' and 'ShadowedClassHook', show their message in a
traceback. For a
'SyntaxError' the 'traceback' module prints the 'msg' attribute rather
than 'str()' of the exception, and falls back to '<no detail available>'
when 'msg' is 'None'. Pytest renders exceptions through that module on
every version, and so does the default exception hook from Python 3.13
on, so the message has to be in 'msg'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from traceback import format_exception_only

from worktoy.keenum import KeeNum, Kee
from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import DelException, QuestionableSyntax
from worktoy.waitaminute.meta import UnboundClassHook, ShadowedClassHook

from . import WaitAMinuteTest


class TestSyntaxErrorMessage(WaitAMinuteTest):
  """
  TestSyntaxErrorMessage provides tests for the message a traceback shows
  for each of the exceptions deriving from 'SyntaxError', each raised by
  the class body it explains.
  """

  def _assertShown(self, exception: SyntaxError) -> None:
    """Asserts that 'msg' holds the message of 'exception', and that the
    last line of its traceback shows that message."""
    lastLine = format_exception_only(type(exception), exception)[-1]
    self.assertEqual(exception.msg, str(exception))
    self.assertIn(str(exception), lastLine)
    self.assertNotIn('<no detail available>', lastLine)

  def test_del_exception(self) -> None:
    """
    A class body defining '__del__' without 'trustMeBro' raises a
    'DelException' whose traceback shows its message.
    """
    with self.assertRaises(DelException) as context:
      class Foo(BaseObject):
        __del__ = lambda self: None
    self._assertShown(context.exception)

  def test_questionable_syntax(self) -> None:
    """
    A class body binding the near miss '__set_item__' raises a
    'QuestionableSyntax' whose traceback shows its message.
    """
    with self.assertRaises(QuestionableSyntax) as context:
      class Foo(BaseObject):
        __set_item__ = None
    self._assertShown(context.exception)

  def test_unbound_class_hook(self) -> None:
    """
    A class body binding '__class_str__' to a plain function raises an
    'UnboundClassHook' whose traceback shows its message.
    """
    with self.assertRaises(UnboundClassHook) as context:
      class Foo(BaseObject):
        __class_str__ = lambda cls: 'Foo'
    self._assertShown(context.exception)

  def test_shadowed_class_hook(self) -> None:
    """
    A 'KeeNum' body binding '__class_len__', which 'KeeMeta' never calls,
    raises a 'ShadowedClassHook' whose traceback shows its message.
    """
    with self.assertRaises(ShadowedClassHook) as context:
      class Num(KeeNum):
        A = Kee[int](1)

        @classmethod
        def __class_len__(cls) -> int:
          return 1  # pragma: no cover
    self._assertShown(context.exception)
