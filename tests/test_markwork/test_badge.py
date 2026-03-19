"""
TestBadge tests the functionality of the 'Badge' class from the
'worktoy.markwork' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING

from worktoy.lorem_ipsum import StochasticWord, Sentence
from worktoy.markwork import Badge
from worktoy.utilities import maybe

from . import MarkworkTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional

  InlineImages: TypeAlias = tuple[InlineImage, ...]


class TestBadge(MarkworkTest):
  """
  TestInlineImage tests the functionality of the InlineImage class from the
  'worktoy.markwork' package.
  """

  def test_init(self, ) -> None:
    """
    This method tests each overloaded constructor of the 'InlineImage'
    class, which provides the following constructor overloads:

    @overload(THIS)
    def __init__(self, other: Self) -> None: ...

    @overload(str, str)
    def __init__(self, url: str, alt: str) -> None: ...

    @overload(str)
    def __init__(self, url: str) -> None: ...

    @overload()
    def __init__(self) -> None: ...
    """
    initStrStr = Badge('assets/images/sample.jpg', 'Sample Image')
    self.assertEqual(initStrStr.imgUrl, 'assets/images/sample.jpg')
    self.assertEqual(initStrStr.altText, 'Sample Image')
    initStr = Badge('https://example.com/sample.png')
    self.assertEqual(initStr.imgUrl, 'https://example.com/sample.png')
    self.assertEqual(initStr.altText, 'https://example.com/sample.png')
    initEmpty = Badge()
    self.assertFalse(initEmpty.imgUrl)
    self.assertFalse(initEmpty.altText)
    initOther = Badge(initStrStr)
    self.assertEqual(initOther.imgUrl, 'assets/images/sample.jpg')
    self.assertEqual(initOther.altText, 'Sample Image')
