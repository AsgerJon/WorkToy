"""
TestHeaderNum tests the 'HeaderNum' class from the 'worktoy.markwork'
package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import HeaderNum

from . import MarkworkTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class TestHeaderNum(MarkworkTest):
  """
  TestHeaderNum tests the 'HeaderNum' class from the 'worktoy.markwork'
  package.
  """

  def test_enumerations(self) -> None:
    """
    Test that the 'HeaderNum' class has the expected enumerations.
    """
    for i, member in enumerate(HeaderNum):
      self.assertIsInstance(member, HeaderNum)
      self.assertEqual(int(member), i)
