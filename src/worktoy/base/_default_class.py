"""WorkToy - Core - Default
This class provides utility as static methods.
Classes in the package subclass this class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from warnings import warn

from icecream import ic

from worktoy.base import GuardClass
from worktoy.core import Function

ic.configureOutput(includeContext=True)


class DefaultClass(GuardClass):
  """WorkToy - DefaultClass
  This class provides utility as static methods.
  Classes in the package subclass this class.
  """

  __core_instance__ = None

  def __init__(self, *args, **kwargs) -> None:
    GuardClass.__init__(self, *args, **kwargs)

  def monoSpace(self, text: str, newLine: str = None) -> str:
    """Convert text to monospaced format with consistent spacing and line
    breaks.

    Args:
      text (str): The input text to be modified.
      newLine (str, optional):
        The string representing the line break. If not provided,
        the default value '<br>' is used. Defaults to None.

    Returns:
      str: The modified text with consistent spacing and line breaks.

    Raises:
      None

    Examples:
      >>> self.monoSpace('Hello   World')
      'Hello World'
      >>> self.monoSpace('Hello<br>World', '<br>')
      'Hello\nWorld'

    The `monoSpace` function takes a string `text` and an optional string
    `newLine`, and returns a modified version of the input text with
    consistent
    spacing and line breaks. If the `newLine` argument is not provided, the
    default value '<br>' is used as the line break string.

    The function performs the following steps:
    1. Replaces all occurrences of '\n' and '\r' characters with a space '
    ' in
       the input `text`.
    2. Repeatedly replaces multiple consecutive spaces with a single space
       until no more consecutive spaces are found in the `text`.
    3. Replace the `newLine` string (or the default '<br>' if not provided)
       with a line break '\n' character in the modified `text`.
    4. Returns the modified `text`.

    Note:
    - The `newLine` string is treated as a literal string, so make sure to
      provide the exact string to be replaced as the line break.
    - The `newLine` string is case-sensitive. If the provided `newLine`
    string
      does not match the exact case in the input `text`, it will not be
      replaced with a line break."""
    newLine = str(self.maybe(newLine, '<br>'))
    text = text.replace('\n', ' ').replace('\r', ' ')
    while '  ' in text:
      text = text.replace('  ', ' ')
    return text.replace(newLine, '\n')

  def stringList(self, *args, **kwargs) -> list[str]:
    """The stringList function provides an easier way to write lists of
    strings. Instead of wrapping each item in ticks, write on long string
    with
    consistent separators, and stringList will convert it to a list of
    strings.
    Instead of: numbers = ['one', 'two', 'three', 'four']
    Use stringList: numbers = stringList('one, two, three, four')
    Please note that all white space around each separator will be removed.
    For example: ', ' and ',' will produce the same outcome when used as
    separators on the same text.
    #  MIT Licence
    #  Copyright (c) 2023 Asger Jon Vistisen"""

    strArgs = self.pad(self.maybeTypes(str, *args, ), 3)
    sourceKeys = ['source', 'src', 'txt']
    sourceKwarg = self.maybeKey(str, *sourceKeys, **kwargs)
    separatorKeys = ['separator', 'splitHere']
    separatorKwarg = self.maybeKey(str, *separatorKeys, **kwargs)
    sourceArg, separatorArg, ignoreArg = strArgs
    sourceDefault, separatorDefault = None, ', '
    source = self.maybe(sourceKwarg, sourceArg, sourceDefault)
    separator = self.maybe(separatorKwarg,
                           separatorArg,
                           separatorDefault, )
    if source is None:
      msg = 'stringList received no string!'
      raise ValueError(msg)
    if not isinstance(source, str):
      raise TypeError
    out = source.split(str(separator))
    out = [self.monoSpace(arg) for arg in out]
    return [self.trimWhitespace(arg) for arg in out]

  def justify(self,
              text: str,
              charLimit: int = None,
              *spaceLike: str) -> str:
    """The justify function works similarly to monoSpace, except for
    ignoring all new-line indicators and instead splits the string into
    lines separated by new-line at given intervals. """
    if not text:
      return ''
    text = text.replace(' %', '¤¤')
    text = self.monoSpace(text)
    charLimit = int(self.maybe(charLimit, 77))
    spaceLike = [' ', *spaceLike]
    allWords = [text.split(space) for space in spaceLike]
    wordList = []
    for words in allWords:
      wordList = [*wordList, *words]
    words = wordList
    lines = []
    line = []
    for (i, word) in enumerate(words):
      if sum([len(w) for w in line]) + len(word) + len(line) + 1 < charLimit:
        line.append(word)
      else:
        lines.append(line)
        line = [word, ]
    lines.append(line)
    lineList = []
    for line in lines:
      lineList.append(' '.join(line))
    out = '\n'.join(lineList)
    out = out.replace('¤¤', ' %')
    return out

  def extractBetween(self, text: str, before: str, after: str) -> list:
    """
    Extracts substrings from the text that are enclosed between the specified
    characters, before, and after. If before and after are the same
    character,
    the function will correctly handle this case and extract the text between
    each pair of those characters.

    :param text: The text to search within can be a multiline string.
    :param before: The character or substring that precedes the text to be
                   extracted. If multiline, can be a newline character.
    :param after: The character or substring that follows the text to be
                  extracted. If multiline, can be a newline character.
    :return: A list of substrings found between the specified characters.
             If no such substrings are found, it will return an empty list.
    :example: extractBetween("a(b(c)d)e", '(', '(') returns ['b(c']
              extractBetween("Line 1\nLine 2\nLine 3", '\n', '\n') returns
              ['Line 2']
    """
    result = []
    start = text.find(before)
    while start != -1:
      if before == after:
        end = text.find(after, start + 2)
      else:
        end = text.find(after, start + 1)
      if end != -1:
        result.append(text[start + 1:end])
      start = text.find(before, end + 1)
    return result

  def trimWhitespace(self, text: str) -> str:
    """
    Removes the leading and trailing whitespace from the input text.

    Args:
      text (str): the input text string.

    Returns:
      str: the text string without leading and trailing whitespace.
    """
    return text.strip()

  def parseFactory(self, type_: type, *keys) -> Function:
    """Creates a factory for parsing based on keys and type"""

    def parseKeyType(instance: DefaultClass, *args, **kwargs) -> object:
      """Parses by key and type"""
      itemKwarg = instance.maybeKey(type_, *keys, **kwargs)
      itemArg = instance.maybeType(type_, *args)
      item = instance.maybe(itemKwarg, itemArg)
      if isinstance(item, type_):
        return item

    return parseKeyType

  def typeName(self, cls: object) -> str:
    """Returns the name of the given type. If the argument is not a type,
    the type of the argument is used instead."""
    if not isinstance(cls, type):
      msg = """Expected argument to be of type 'type', but received: %s"""
      warn(msg % type(cls))
    if cls is None:
      return 'NoneClass'
    qualName = getattr(cls, '__qualname__', None)
    name = getattr(cls, '__name__', None)
    strRep = '%s' % (cls)
    out = self.maybe(qualName, name, strRep)
    if isinstance(out, str):
      return out
