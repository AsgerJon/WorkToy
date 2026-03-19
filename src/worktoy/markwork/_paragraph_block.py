"""
Paragraph subclasses 'BaseObject' and provides the content container. The
structure of a project is 'Index' > 'Section' > 'Subsection' >
'Paragraph', but only paragraph will actually own content. The others will
only contain references to instances of their child classes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

from ..utilities import textFmt, wordWrap
from ..desc import Field
from . import Block, InlineText

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Iterable, Type

  from ..keenum import KeeNum as HeaderNum

  HeaderField: TypeAlias = Union[Field, HeaderNum]
else:
  from . import HeaderNum


class ParagraphBlock(Block):
  """
  Paragraph subclasses 'BaseObject' and provides the content container. The
  structure of a project is 'Index' > 'Section' > 'Subsection' >
  'Paragraph', but only paragraph will actually own content. The others will
  only contain references to instances of their child classes.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __header_level__: HeaderNum = HeaderNum.PARAGRAPH
  __line_width__: int = 77

  #  Fallback Variables

  #  Private Variables

  #  Public Variables

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  OPTIONAL METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  REQUIRED METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def wrapInline(cls, *inlines: InlineText, ) -> str:
    """
    This method concatenates the words found in the inline components and
    applies word wrapping to width specified by class variable
    '__line_width__'. New lines will appear only between words, and not
    within tags. It is used by the 'markdown' method to render the
    Markdown representation.
    """
    words = []
    # \__________________WEIRD IMPLEMENTATION ALERT__________________________
    #  In the following word wrapping implementation, tags include spaces
    #  but must not be split at those spaces. The placeholder tokens have
    #  no spaces but the same length as the tags, allowing the use of the
    #  normal word wrapping function provided by 'wordWrap' from the
    #  'worktoy.utilities' package. After wrapping, placeholders are
    #  substituted back for the original tags. The placeholder must match
    #  the tag's length exactly — a shorter or longer key would shift
    #  surrounding words and produce incorrect line breaks.
    # /¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    for inline in inlines:
      text = str.strip(inline.text, )

      if str.startswith(text, '<') and str.endswith(text, '>'):
        words.append(text)
      else:
        words.extend((*str.split(inline.text),))
    tmp = dict()
    for word in words:
      stripped = str.strip(word)
      if str.startswith(stripped, '<') and str.endswith(stripped, '>'):
        n = len(word)
        key = None
        while (key is None) or key in tmp:
          keyParts = []
          while sum(len(p) for p in keyParts) + 4 < n:
            keyParts.append("""%d""" % randint(0, 9999))
          key = """{{%s}}""" % str.join('', keyParts)[:n - 4]
        tmp[key] = word
    wrapped = wordWrap(cls.__line_width__, textFmt(str.join(' ', words)))
    for key, word in tmp.items():
      wrapped = str.replace(wrapped, key, """\n%s\n""" % word)
    return wrapped

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PUBLIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def markdown(self, ) -> str:
    """
    This method concatenates the words found in the inline components and
    applies word wrapping to width specified by class variable
    '__line_width__'. New lines will appear only between words, and not
    within tags.

    Returns
    -------
    str
      The Markdown representation of the paragraph.

    Examples
    --------
    >>> from worktoy.markwork import ParagraphBlock, InlineText
    >>> class Roll(ParagraphBlock):
    ...   i1 = InlineText('Never gonna give you up')
    ...   i2 = InlineText('Never gonna let you down')
    ...   i3 = InlineText('Never gonna run around and desert you')
    >>> print(Roll().markdown())
    Never gonna give you up Never gonna let you down Never gonna run (->)
    around and desert you
    """
    return self.wrapInline(*self.inlines)
