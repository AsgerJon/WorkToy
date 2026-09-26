"""
TestFallbackPrecedence subclasses 'OverloadTest' and pins how the
fallback and the finalizer of an overloaded method pass to subclasses. A
subclass declaring its own fallback or finalizer replaces the inherited
one, while a subclass declaring neither keeps both.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from . import OverloadTest


class Handler(BaseObject):
  """Handler overloads 'handle' for an 'int', falls back to a fixed
  answer for anything else, and records in 'trail' which finalizer ran
  last."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  trail = AttriBox[str]('')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def handle(self, n: int) -> str:
    return 'int'

  @overload.fallback
  def handle(self, *args) -> str:
    return 'handler'

  @overload.finalize
  def handle(self, *args) -> None:
    self.trail = 'handler'


class SubHandler(Handler):
  """SubHandler replaces both the fallback and the finalizer of
  'Handler' and keeps its 'int' signature."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload.fallback
  def handle(self, *args) -> str:
    return 'sub'

  @overload.finalize
  def handle(self, *args) -> None:
    self.trail = 'sub'


class QuietHandler(Handler):
  """QuietHandler declares nothing and inherits everything 'Handler'
  registers under 'handle'."""


class TestFallbackPrecedence(OverloadTest):
  """
  TestFallbackPrecedence pins that an own fallback or finalizer replaces
  the inherited one, and that the inherited one applies otherwise.
  """

  def test_own_fallback_replaces_inherited(self) -> None:
    """
    Testing that an argument matching no signature reaches the fallback
    of the class itself, while the inherited 'int' signature still
    answers an 'int'.
    """
    self.assertEqual(Handler().handle('x'), 'handler')
    self.assertEqual(SubHandler().handle('x'), 'sub')
    self.assertEqual(SubHandler().handle(1), 'int')

  def test_fallback_inherited(self) -> None:
    """
    Testing that a class declaring no fallback uses the one it
    inherits.
    """
    self.assertEqual(QuietHandler().handle('x'), 'handler')

  def test_own_finalizer_replaces_inherited(self) -> None:
    """
    Testing that every call runs the finalizer of the class itself, for
    a matched signature and for the fallback alike.
    """
    handler = SubHandler()
    handler.handle(1)
    self.assertEqual(handler.trail, 'sub')
    handler.trail = ''
    handler.handle('x')
    self.assertEqual(handler.trail, 'sub')

  def test_finalizer_inherited(self) -> None:
    """
    Testing that a class declaring no finalizer runs the one it
    inherits.
    """
    handler = QuietHandler()
    handler.handle(1)
    self.assertEqual(handler.trail, 'handler')
