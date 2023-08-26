"""WorkToy – PrimitiveClass
This class provides various utilities."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import builtins
from typing import Union

Sample = type('Sample', (), dict(clsMethod=classmethod(lambda cls: cls)))
Map = Union[type(type('_', (), {}).__dict__), dict]
Keys = type({}.keys())
Values = type({}.values())
Items = type({}.items())
Bases = tuple[type, ...]
Type = type(type('_', (), {}))
Function = (type(getattr(type('_', (), {'_': lambda self: self}), '_')))
Method = (type(getattr(type('_', (), {'_': lambda self: self})(), '_')))
WrapperDescriptor = type(type('_', (), {}).__init__)
WrapperMethod = type(type('_', (), {}).__call__)
BuiltinFunction = type(print)
Functional = Union[WrapperDescriptor, WrapperMethod, Function, Method]
FunctionTuple = (Function, Method, WrapperDescriptor, WrapperMethod,
                 BuiltinFunction)
FunctionList = [*FunctionTuple, ]
Functions = Union[
  Function, Method, WrapperDescriptor, WrapperMethod, BuiltinFunction]


class PrimitiveClass:
  """WorkToy – PrimitiveClass
  This class provides various utilities."""

  @staticmethod
  def getBuiltinTypes() -> dict:
    """Getter-function for list of builtin types"""
    base = []
    for (key, val) in builtins.__dict__.items():
      test = isinstance(val, type)
      test = test and (not isinstance(val, BuiltinFunction))
      test = test and (not issubclass(val, BaseException))
      test = test and (not key.startswith('__'))
      if test:
        try:
          val.__new__(val)
          base.append((key, val))
        except TypeError as e:
          base.append((key, val, e))
    return {i[0]: i[1] for i in base if len(i) == 2}

  @staticmethod
  def resolveType(typeName: str) -> type:
    """Returns the type that matches the given name"""
    if typeName == 'type':
      return type
    builtInType = PrimitiveClass.getBuiltinTypes().get(typeName, None)
    localType = locals().get(typeName, None)
    globalType = globals().get(typeName, None)
    typesFound = [i for i in [builtInType, localType, globalType] if i]
    if not typesFound:
      raise NameError(typeName)
    if len(typesFound) == 1:
      return typesFound[-1]
    if len(typesFound) == 2:
      if typesFound[0] is typesFound[-1]:
        return typesFound[0]
    for foundType in typesFound:
      if foundType is not typesFound[0]:
        raise TypeError
    return typesFound[0]

  @staticmethod
  def createInstanceOf(type_: object) -> object:
    """Creator-function for sample of the type."""
    if type_ is type:
      return type('SampleClass', (), {})
    if isinstance(type_, type):
      try:
        return type_.__new__(type_, )
      except TypeError as e:
        msg = """Failed to create base sample of %s""" % type_
        raise TypeError(msg) from e
    if isinstance(type_, str):
      type_ = PrimitiveClass.resolveType(type_)
      return PrimitiveClass.createInstanceOf(type_)
    if not isinstance(type_, str):
      return PrimitiveClass.createInstanceOf(type(type_))

  @staticmethod
  def createInstanceFactory(type_: type,
                            callBack: Function = None) -> Function:
    """Creates a factory for instance of the given type. The factory is
    tested before being returned. If not callback function is provided,
    and the factory fails, the method will raise a TypeError. Otherwise,
    the method will invoke the callback in case of failure.

    The base function expects the type argument to be a type, but any
    object is acceptable. If 'type_' is a string, a type of the same name
    is resolved to a type, which is then passed to the base function. For
    all other types, the type of the provided argument is passed on.
    """

    if isinstance(type_, str):
      type_ = PrimitiveClass.resolveType(type_)
      return PrimitiveClass.createInstanceFactory(type_)
    if not isinstance(type_, type):
      return PrimitiveClass.createInstanceFactory(type(type_))

    def errorHandle(error: Exception) -> object:
      """Handles error"""
      if isinstance(callBack, FunctionTuple):
        return callBack(error)
      raise error

    def factory() -> object:
      """Factory function"""
      return type_.__new__(type_)

    try:
      factory()
      return factory
    except Exception as e:
      return errorHandle(e)

  def __init__(self, *args, **kwargs) -> None:
    self._args = args
    self._kwargs = kwargs

  def maybe(self, *args) -> object:
    """Returns the first argument different from None"""
    for arg in args:
      if arg is not None:
        return arg

  def maybeType(self, cls: type, *args) -> object:
    """Returns the first argument belonging to cls"""
    for arg in args:
      if isinstance(arg, cls):
        return arg

  def maybeTypes(self, cls: type, *args, **kwargs) -> list:
    """Returns all arguments belonging to cls"""
    out = []
    for arg in args:
      if isinstance(arg, cls):
        out.append(arg)
    while len(out) < kwargs.get('pad', 0):
      out.append(kwargs.get('padChar', None))
    return out

  def maybeKey(self, *args, **kwargs) -> object:
    """Finds the first object in kwargs that matches a given key. Provide
    keys as positional arguments of stringtype. Optionally provide a
    'type' in the positional arguments to return only an object of that
    type."""
    type_ = self.maybeType(type, *args)
    if not isinstance(type_, type):
      type_ = object
    keys = self.maybeTypes(str, *args)
    for key in keys:
      val = kwargs.get(key, None)
      if isinstance(val, type_) and val is not None:
        return val

  def maybeKeys(self, *args, **kwargs) -> list:
    """Same as maybeKey, but removes every value that matches a given key"""
    type_ = self.maybeType(type, *args)
    if not isinstance(type_, type):
      type_ = object
    keys = self.maybeTypes(str, *args)
    out = []
    for key in keys:
      val = self.maybeKey(self, type_, key, **kwargs)
      if val is not None:
        out.append(val)
    return out

  def applyPadding(self,
                   target: Union[int, list] = None,
                   char: object = None,
                   source: list = None, **kwargs) -> list:
    """Applies padding from source to target. Elements from source
    populate target. Provide a target list, or an integer specifying the
    length of the target filled with the object in char.
    If the source argument is longer than target, the method returns the
    source, unless the keyword argument allowCropping is True (default is
    False). Otherwise, the method truncates the source from the end.
    """
    if target is None:
      return source
    if isinstance(target, int):
      return self.applyPadding([char for _ in range(target)], None, source)
    if len(source) == len(target):
      return source
    if kwargs.get('allowCropping', False) and len(source) > len(target):
      return source[:len(target) - 1]
    while len(source) < len(target):
      source.append(None)
    out = []
    for (src, tgt) in zip(source, target):
      out.append(self.maybe(src, tgt))
    return out

  def empty(self, *args) -> bool:
    """Returns True if every positional argument is None. The method
    returns True when receiving no positional arguments. Otherwise, the
    method returns True."""
    if not args:
      return True
    for arg in args:
      if arg is not None:
        return False
    return True

  def plenty(self, *args) -> bool:
    """The method returns True if no positional argument is None.
    Otherwise, the method returns False. """
    if not args:
      return True
    for arg in args:
      if arg is None:
        return False
    return True

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
    Meaning that ', ' and ',' will produce the same outcome when used as
    separators on the same text.
    #  MIT Licence
    #  Copyright (c) 2023 Asger Jon Vistisen"""

    strArgs = self.applyPadding(3, None, self.maybeTypes(str, *args, ))
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
    return out

  def justify(self,
              text: str,
              charLimit: int = None,
              *spaceLike: str) -> (str):
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

    def parseKeyType(instance: PrimitiveClass, *args, **kwargs) -> object:
      """Parses by key and type"""
      itemKwarg = instance.maybeKey(type_, *keys, **kwargs)
      itemArg = instance.maybeType(type_, *args)
      item = instance.maybe(itemKwarg, itemArg)
      if isinstance(item, type_):
        return item

    return parseKeyType
