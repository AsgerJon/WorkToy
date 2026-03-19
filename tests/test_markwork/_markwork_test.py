"""
MarkworkTest subclasses 'BaseTest' from the 'worktoy.work_test' package
and provides the base class for all tests of the 'worktoy.markdown' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from worktoy.utilities import maybe
from worktoy.lorem_ipsum import Sentence
from worktoy.markwork import (Badge,
  InlineText,
  InlineLink,
  InlineLorem)
from worktoy.work_test import BaseTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Iterator

  InlineTexts: TypeAlias = tuple[InlineText, ...]
  Badges: TypeAlias = tuple[Badge, ...]
  InlineLinks: TypeAlias = Iterator[InlineLink]


class MarkworkTest(BaseTest):
  """
  MarkworkTest subclasses 'BaseTest' from the 'worktoy.work_test' package
  and provides the base class for all tests of the 'worktoy.markdown'
  package.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __image_extensions__ = 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'
  __image_specs__ = (
    'https://example.com/%s.%s',
    'assets/images/%s.%s',
    'https://cdn.example.com/images/%s.%s',
    )

  #  Fallback Variables
  __fallback_lorem_count__: int = 80

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def randomInlineText(n: int = None, ) -> InlineText:
    """
    This method generates a random 'InlineText' instance using the
    'worktoy.lorem_ipsum' package.

    Parameters
    ----------
    n: int, default=80
      The number of characters to include in the generated text.

    Returns
    -------
    InlineText
      A random 'InlineText' instance.
    """
    n = maybe(n, 80)
    sentence = Sentence(n)
    return InlineText(str(sentence))

  @classmethod
  def randomInlineTexts(cls, n: int = None, N: int = None) -> InlineTexts:
    """
    This method generates a tuple of random 'InlineText' instances using the
    'worktoy.lorem_ipsum' package.

    Parameters
    ----------
    n: int, default=80
      The number of characters to include in each generated text.
    N: int, default=10
      The number of 'InlineText' instances to generate.

    Returns
    -------
    tuple[InlineText, ...]
      A tuple of random 'InlineText' instances.
    """
    n, N = maybe(n, 80), maybe(N, 10)
    return (*(cls.randomInlineText(n) for _ in range(maybe(N, 10))),)

  @classmethod
  def randomInlineLink(
      cls,
      spec: str = None,
      linkText: str = None,
      tip: str = None,
      ) -> InlineLink:
    """
    This method generates a random 'InlineLink' instance using the
    'worktoy.lorem_ipsum' package.

    Parameters
    ----------
    spec: str, optional
      The format specification for the link URL. It must accept exactly
      one 'str' component, for example: 'https://example.com/%s'.
    tip: str, optional
      The tooltip text for the link. If not provided, a random sentence will
      be generated.

    Returns
    -------
    InlineLink
      A random 'InlineLink' instance.
    """
    spec = maybe(spec, 'https://example.com/%s')
    url = spec % cls.stochWord.realize()
    linkText = maybe(linkText, str(Sentence(50)))
    tip = maybe(tip, str(Sentence(30)))
    return InlineLink(url, linkText, tip)

  @classmethod
  def randomInlineLinks(
      cls,
      N: int = None,
      spec: str = None,
      linkText: str = None,
      tip: str = None,
      ) -> InlineLinks:
    """
    This method generates a tuple of random 'InlineLink' instances using the
    'worktoy.lorem_ipsum' package.

    Parameters
    ----------
    N: int, default=10
      The number of 'InlineLink' instances to generate.
    spec: str, optional
      The format specification for the link URLs. It must accept exactly
      one 'str' component, for example: 'https://example.com/%s'.
    linkText: str, optional
      The link text for the links. If not provided, random sentences will be
      generated.
    tip: str, optional
      The tooltip text for the links. If not provided, random sentences will
      be generated.

    Returns
    -------
    InlineLinks
      A tuple of random 'InlineLink' instances.
    """
    for i in range(maybe(N, 10)):
      yield cls.randomInlineLink(spec, linkText, tip)

  @classmethod
  def randomInlineLorem(cls, n: int = None) -> InlineText:
    """
    This method generates a random 'InlineText' instance containing 'lorem
    ipsum' text using the 'worktoy.lorem_ipsum' package.

    Parameters
    ----------
    n: int, default=80
      The number of characters to include in the generated text.

    Returns
    -------
    InlineText
      A random 'InlineLorem' instance.
    """
    return InlineLorem(maybe(n, cls.__fallback_lorem_count__))

  @classmethod
  def randomInlineLorems(cls, n: int = None, N: int = None) -> InlineTexts:
    """
    This method generates a tuple of random 'InlineText' instances containing
    'lorem ipsum' text using the 'worktoy.lorem_ipsum' package.

    Parameters
    ----------
    n: int, default=80
      The number of characters to include in each generated text.
    N: int, default=10
      The number of 'InlineText' instances to generate.

    Returns
    -------
    tuple[InlineText, ...]
      A tuple of random 'InlineLorem' instances.
    """
    n, N = maybe(n, cls.__fallback_lorem_count__), maybe(N, 10)
    return (*(cls.randomInlineLorem(n) for _ in range(N)),)

  @classmethod
  def setUpClass(cls, ) -> None:
    """
    Sets environment variable 'MARKWORK_TEST_DIR' to the directory of this
    file.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    cls.dirEnvVar = 'MARKWORK_TEST_DIR'
    super().setUpClass()
    os.environ[cls.dirEnvVar] = here

  @classmethod
  def tearDownClass(cls, ) -> None:
    """
    Unsets environment variable 'MARKWORK_TEST_DIR'.
    """
    super().tearDownClass()
    del os.environ[cls.dirEnvVar]
