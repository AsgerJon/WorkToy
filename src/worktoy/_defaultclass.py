"""WorkToy - DefaultClass
All classes created with metaclass AbstractMetaType inherits from this
class"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

Function = type(lambda: None)


class DefaultClass:
  """WorkToy - DefaultClass
  All classes created with metaclass AbstractMetaType inherits from this
  class"""

  @staticmethod
  def maybe(*args) -> object:
    """The None-aware 'maybe' implements the null-coalescence behaviour.
    #  MIT Licence
    #  Copyright (c) 2023 Asger Jon Vistisen"""
    for arg in args:
      if arg is not None:
        return arg

  @staticmethod
  def onlyIf(func: Function, *args) -> list[object, ...]:
    """Returns a list of the positional arguments that satisfy the given
    function """
    return [arg for arg in args if func(arg)]

  @staticmethod
  def maybeFirstIf(func: Function, *args, ) -> object:
    """Returns the first positional argument """
    return DefaultClass.onlyIf(func, *args)[0]

  @staticmethod
  def maybeAllIf(func: Function, *args, ) -> list[object]:
    """Returns the first positional argument """
    return DefaultClass.onlyIf(func, *args)

  @staticmethod
  def maybeType(type_: type, *args) -> object:
    """Getter-function for the first arg in the positional arguments that
    has the given type"""
    func = lambda item: True if isinstance(item, type_) else False
    return DefaultClass.maybeFirstIf(func, *args)

  @staticmethod
  def maybeTypes(type_: type, *args, **kwargs) -> list[object]:
    """Getter-function for each arg in the positional arguments that has the
    given type"""
    func = lambda item: True if isinstance(item, type_) else False
    out = DefaultClass.maybeAllIf(func, *args)
    padLen, padChar = kwargs.get('padLen', None), kwargs.get('padChar', None)
    if padLen is None:
      return out
    if not isinstance(padLen, int):
      raise TypeError
    while padLen > len(out):
      out.append(padChar)
    return out

  @staticmethod
  def empty(*args) -> bool:
    """Returns True unless one of the positional arguments (if any) is
    different from None. If no positional arguments are present this method
    returns True also"""
    func = lambda x: True if x is None else False
    return all(DefaultClass.maybeAllIf(func, (*args, None)))

  @staticmethod
  def some(*args) -> bool:
    """Returns True if at least one of the positional arguments is different
    from None. If no positional argument is present, this function returns
    False. """
    func = lambda x: False if x is None else True
    return any(DefaultClass.maybeAllIf(func, (*args, None)))

  @staticmethod
  def plenty(*args) -> bool:
    """Returns True if every positional argument is different from None.
    Please note that plenty also returns True if no positional arguments are
    found. Thus: empty() == plenty(), but some() is False."""
    func = lambda x: False if x is None else True
    return all(DefaultClass.maybeAllIf(func, (*args, None)))

  @staticmethod
  def _fromKeys(type_: type = None, one: bool = None, *keys,
                **kwargs) -> object:
    """Returns first value from recognized keys"""
    out = []
    for key in keys:
      val = kwargs.get(key, None)
      if val is not None:
        if not isinstance(type_, type) or isinstance(val, type_):
          if one is None:
            return val
          out.append(val)
    return out or None

  @staticmethod
  def allKeys(type_: type = None, *keys, **kwargs) -> object:
    """Returns all values matching any key"""
    return DefaultClass._fromKeys(type_, *keys, **kwargs)

  @staticmethod
  def firstKey(type_: type = None, *keys, **kwargs) -> object:
    """Returns all values matching any key"""
    return DefaultClass._fromKeys(type_, True, *keys, **kwargs)

  @staticmethod
  def monoSpace(text: str, newLine: str = None) -> str:
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
      >>> DefaultClass.monoSpace('Hello   World!')
      'Hello World!'
      >>> DefaultClass.monoSpace('Hello<br>World!', '<br>')
      'Hello\nWorld!'

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
    3. Replaces the `newLine` string (or the default '<br>' if not provided)
       with a line break '\n' character in the modified `text`.
    4. Returns the modified `text`.

    Note:
    - The `newLine` string is treated as a literal string, so make sure to
      provide the exact string to be replaced as the line break.
    - The `newLine` string is case-sensitive. If the provided `newLine`
    string
      does not match the exact case in the input `text`, it will not be
      replaced with a line break."""
    newLine = str(DefaultClass.maybe(newLine, '<br>'))
    text = text.replace('\n', ' ').replace('\r', ' ')
    while '  ' in text:
      text = text.replace('  ', ' ')
    return text.replace(newLine, '\n')

  @staticmethod
  def stringList(*args, **kwargs) -> list[str]:
    """The stringList function provides an easier way to write lists of
    strings. Instead of wrapping each item in ticks, write on long string
    with
    consistent separators, and stringList will convert it to a list of
    strings.
    Instead of: numbers = ['one', 'two', 'three', 'four']
    Use stringList: numbers = stringList('one, two, three, four')
    Please note that all white space around each separator will be removed.
    Meaning that ', ' and ',' will produce the same outcome when used as
    separators on the same text.
    #  MIT Licence
    #  Copyright (c) 2023 Asger Jon Vistisen"""

    strArgs = DefaultClass.maybeTypes(str, *args, padLen=3, padChar=None)
    sourceKeys = ['source', 'src', 'txt']
    sourceKwarg = DefaultClass.firstKey(str, *sourceKeys, **kwargs)
    separatorKeys = ['separator', 'splitHere']
    separatorKwarg = DefaultClass.firstKey(str, *separatorKeys, **kwargs)
    sourceArg, separatorArg, ignoreArg = strArgs
    sourceDefault, separatorDefault = None, ', '
    source = DefaultClass.maybe(sourceKwarg, sourceArg, sourceDefault)
    separator = DefaultClass.maybe(separatorKwarg,
                                   separatorArg,
                                   separatorDefault, )
    if source is None:
      msg = 'stringList received no string!'
      raise ValueError(msg)
    if not isinstance(source, str):
      raise TypeError
    out = source.split(str(separator))
    return out

  @staticmethod
  def justify(text: str, charLimit: int = None, *spaceLike: str) -> str:
    """The justify function works similarly to monoSpace, except for
    ignoring all new-line indicators and instead splits the string into
    lines separated by new-line at given intervals. """
    if not text:
      return ''
    text = text.replace(' %', '¤¤')
    text = DefaultClass.monoSpace(text)
    charLimit = int(DefaultClass.maybe(charLimit, 77))
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

  @staticmethod
  def extractBetween(text: str, before: str, after: str) -> list:
    """
    Extracts substrings from the text that are enclosed between the specified
    characters, before and after. If before and after are the same character,
    the function will correctly handle this case and extract the text between
    each pair of those characters.

    :param text: The text to search within, can be a multiline string.
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

  @staticmethod
  def trimWhitespace(text: str) -> str:
    """
    Removes the leading and trailing whitespace from the input text.

    Args:
      text (str): The input text string.

    Returns:
      str: The text string without leading and trailing whitespace.
    """
    return text.strip()
