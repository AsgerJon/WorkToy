"""
TestInlineLink tests the InlineLink class from the 'worktoy.markwork'
package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import Index, Chapter, Block
from worktoy.markwork import InlineLorem, InlineLink, Badge
from worktoy.waitaminute.desc import ProtectedError
from . import MarkworkTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Iterator

  InlineLinks: TypeAlias = Iterator[InlineLink]


class Linkable(Chapter):
  """
  Linkable subclasses 'Chapter' and provides a linkable chapter for testing
  the 'InlineLink' class.
  """
  risitas = Badge(
    """etc/assets/images/risitas.jpg""",
    """Risitas Meme""",
    )
  lorem1 = InlineLorem(120)
  lorem2 = InlineLorem(120)
  lorem3 = InlineLorem(120)
  lorem4 = InlineLorem(120)
  lorem5 = InlineLorem(120)


class LoremBlock(Block):
  """
  LoremBlock subclasses 'Block' and provides a block of lorem ipsum text for
  testing the 'InlineLink' class.
  """
  i1 = InlineLorem(120)
  i2 = InlineLorem(120)
  i3 = InlineLorem(120)
  i4 = InlineLorem(120)
  i5 = InlineLorem(120)

  def markdown(self) -> str:
    """
    The markdown simply concatenates the Markdown of each inline
    component, separated by space.
    """
    return str.join(' ', (*(i.text for i in self.inlines),), )


class LongText(Index):
  """
  LongText subclasses 'Index' and provides a long text for testing the
  'InlineLink' class.
  """

  __fallback_dir__ = None

  i1 = InlineLink('LongText.never', 'Never')
  i2 = InlineLink('LongText.gonna', 'gonna')
  i3 = InlineLink('LongText.give', 'give')
  i4 = InlineLink('LongText.you', 'you')
  i5 = InlineLink('LongText.up', 'up')

  never = Linkable('Never')
  gonna = Linkable('gonna')
  give = Linkable('give')
  you = Linkable('you')
  up = Linkable('up')

  lorem1 = InlineLorem(600)
  lorem2 = InlineLorem(600)

  block1 = LoremBlock()
  block2 = LoremBlock()
  block3 = LoremBlock()


class TestInlineLink(MarkworkTest):
  """
  TestInlineLink tests the InlineLink class from the 'worktoy.markwork'
  package.
  """

  def test_init(self, ) -> None:
    """
    This method tests each overloaded constructor of the 'InlineLink' class.

    Overloaded Constructors
    -----------------------
    @overload(THIS)
    def __init__(self, other: Self) -> None:

    @overload(str, str, str)
    def __init__(self, url: str, linkText: str, tip: str) -> None: ...

    @overload(str, str)
    def __init__(self, url: str, linkText: str) -> None: ...

    @overload(str)
    def __init__(self, url: str) -> None: ...

    @overload()
    def __init__(self) -> None: ...
    """
    url = 'https://example.com'
    linkText = 'Example Link'
    toolTip = 'This is an example link.'
    linkStr3 = InlineLink(url, linkText, toolTip)
    linkStr2 = InlineLink(url, linkText)
    linkStr1 = InlineLink(url)
    linkStr0 = InlineLink()
    linkOther = InlineLink(linkStr3)
    self.assertEqual(linkStr3.url, url)
    self.assertEqual(linkStr3.linkText, linkText)
    self.assertEqual(linkStr3.toolTip, toolTip)
    self.assertEqual(linkStr2.url, url)
    self.assertEqual(linkStr2.linkText, linkText)
    self.assertEqual(linkStr2.toolTip, linkText)
    self.assertEqual(linkStr1.url, url)
    self.assertEqual(linkStr1.linkText, url)
    self.assertEqual(linkStr1.toolTip, url)
    self.assertFalse(linkStr0.url)
    self.assertFalse(linkStr0.linkText)
    self.assertFalse(linkStr0.toolTip)
    self.assertEqual(linkOther.url, url)
    self.assertEqual(linkOther.linkText, linkText)
    self.assertEqual(linkOther.toolTip, toolTip)

  def test_descriptors(self, ) -> None:
    """
    Testing the attributes of the 'InlineLink' class, which are defined as
    follows:

    Class Descriptors
    ----------
    url: StrBox = AttriBox[str]()
    linkText: StrField = Field()
    toolTip: StrField = Field()
    """

    #  Get operations
    for inlineLink in self.randomInlineLinks():
      url = inlineLink.url
      linkText = inlineLink.linkText
      toolTip = inlineLink.toolTip
      inlineStr = str(inlineLink)
      self.assertIn(url, inlineStr)
      self.assertIn(linkText, inlineStr)
      self.assertIn(toolTip, inlineStr)

    #  Set operations
    baseURL = """https://www.youtube.com/watch?v=dQw4w9WgXcQ"""
    baseLinkText = """Schoolwork"""
    baseTip = """Trust me bro!"""
    persistentLink = InlineLink(baseURL, baseLinkText, baseTip)
    for inlineLink in self.randomInlineLinks():
      persistentLink.url = inlineLink.url
      persistentLink.linkText = inlineLink.linkText
      persistentLink.toolTip = inlineLink.toolTip
      self.assertEqual(persistentLink.url, inlineLink.url)
      self.assertEqual(persistentLink.linkText, inlineLink.linkText)
      self.assertEqual(persistentLink.toolTip, inlineLink.toolTip)

    #  Deleters are not supported, so should raise 'ProtectedError'
    for inlineLink in self.randomInlineLinks():
      oldURL = inlineLink.url
      oldLinkText = inlineLink.linkText
      oldTip = inlineLink.toolTip
      with self.assertRaises(ProtectedError) as context:
        del inlineLink.url
      e = context.exception
      self.assertIs(e.instance, inlineLink)
      self.assertIs(e.desc, InlineLink.url)
      self.assertEqual(e.oldVal, oldURL)

      with self.assertRaises(ProtectedError) as context:
        del inlineLink.linkText
      e = context.exception
      self.assertIs(e.instance, inlineLink)
      self.assertIs(e.desc, InlineLink.linkText)
      self.assertEqual(e.oldVal, oldLinkText)

      with self.assertRaises(ProtectedError) as context:
        del inlineLink.toolTip
      e = context.exception
      self.assertIs(e.instance, inlineLink)
      self.assertIs(e.desc, InlineLink.toolTip)
      self.assertEqual(e.oldVal, oldTip)

  def test_dev_null(self) -> None:
    self.assertTrue(True)
    longText = LongText()
    longText.save("""inline_link.md""")
