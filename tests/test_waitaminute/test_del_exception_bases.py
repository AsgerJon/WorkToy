"""
TestDelExceptionBases subclasses 'WaitAMinuteTest' and pins that the
message of 'DelException' quotes the name of the metaclass alone. The
bases were joined into the quoted name, as in "from the metaclass
'BaseMeta with bases: (BaseObject)'".
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject, BaseMeta
from worktoy.waitaminute.meta import DelException

from . import WaitAMinuteTest


class TestDelExceptionBases(WaitAMinuteTest):
  """
  TestDelExceptionBases provides tests for how the message of
  'DelException' names the metaclass and the bases.
  """

  def test_bases_outside_quotes(self) -> None:
    """The bases follow the quoted metaclass name."""
    with self.assertRaises(DelException) as context:
      class Sus(BaseObject):  # noqa: F841
        def __del__(self) -> None:
          """A '__del__' without 'trustMeBro'."""
    message = str(context.exception)
    self.assertIn("metaclass 'BaseMeta' with bases: (BaseObject)", message)

  def test_no_bases(self) -> None:
    """Without bases the metaclass name stands alone."""
    with self.assertRaises(DelException) as context:
      class Bare(metaclass=BaseMeta):  # noqa: F841
        def __del__(self) -> None:
          """A '__del__' without 'trustMeBro'."""
    message = str(context.exception)
    self.assertIn("metaclass 'BaseMeta',", message)
    self.assertNotIn('with bases', message)
