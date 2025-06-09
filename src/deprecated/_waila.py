"""
Waila provides a well formatted summary of positional and keyword
arguments. The following attributes specify the formatting:

- header: str
The header above the summary.

- lineLength=77: int
The length of each line in the summary.

- indent=2: int
The number of spaces to indent each line.

- lineSep=os.linesep: str
The separator between lines in the summary. Note the default value is left
up to the os.linesep.

- columnSep='|': str
The separator between columns in the summary.


"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os

from worktoy.parse import maybe

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Self, TypeAlias

  Words: TypeAlias = list[str]
  Mappings: TypeAlias = dict[str, Any]


class _Value:
  """
  Primitive, private descriptor class
  """

  __fallback_key__ = None
  __value_key__ = None

  def __init__(self, valueKey: str, fallbackKey: str = None, ) -> None:
    self.__value_key__ = valueKey
    self.__fallback_key__ = fallbackKey

  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    value = getattr(instance, self.__value_key__, None)
    fallback = getattr(instance, self.__fallback_key__, None)
    return maybe(value, fallback)


class Waila:
  """
  Waila provides a well formatted summary of positional and keyword
  arguments. The following attributes specify the formatting:

  - header: str
    The header above the summary.

  - lineLength=77: int
    The length of each line in the summary.

  - indent=2: int
    The number of spaces to indent each line.

  - lineSep=os.linesep: str
    The separator between lines in the summary. Note the default value is
    left
    up to the os.linesep.

  - columnSep='|': str
    The separator between columns in the summary.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables
  __fallback_length__ = 77
  __fallback_indent__ = '  '
  __fallback_line_sep__ = os.linesep
  __fallback_col_sep__ = ' | '
  __fallback_title__ = 'Arguments Summary'
  __fallback_entry__ = 'Index/Key'
  __fallback_type__ = 'type (__name__)'
  __fallback_arg__ = 'value (str)'

  #  Private variables
  __line_length__ = None
  __indent_spaces__ = None
  __line_sep__ = None
  __col_sep__ = None
  __title_text__ = None
  __pos_entry_header__ = None
  __pos_type_header__ = None
  __pos_arg_header__ = None
  __key_entry_header__ = None
  __key_type_header__ = None
  __key_arg_header__ = None
  __pos_args__ = None
  __key_args__ = None

  #  Public variables
  lineLength = _Value('__line_length__', '__fallback_length__', )
  indent = _Value('__indent_spaces__', '__fallback_indent__', )
  lineSep = _Value('__line_sep__', '__fallback_line_sep__', )
  columnSep = _Value('__col_sep__', '__fallback_col_sep__', )
  title = _Value('__title_text__', '__fallback_title__', )
  posEntryHeader = _Value('__pos_entry_header__', '__fallback_entry__', )
  posTypeHeader = _Value('__pos_type_header__', '__fallback_type__', )
  posArgHeader = _Value('__pos_arg_header__', '__fallback_arg__', )
  keyEntryHeader = _Value('__key_entry_header__', '__fallback_entry__', )
  keyTypeHeader = _Value('__key_type_header__', '__fallback_type__', )
  keyArgHeader = _Value('__key_arg_header__', '__fallback_arg__', )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getPositionalArgs(self) -> Words:
    """Get the positional arguments as a list of strings."""
    return maybe(self.__pos_args__, [])

  def _getKeywordArgs(self) -> Mappings:
    """Get the keyword arguments as a dictionary of strings."""
    return maybe(self.__key_args__, {})

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _addPositionalArgs(self, *args: str) -> None:
    """
    Adds positional arguments to the Waila instance.
    """
    existing = self._getPositionalArgs()
    self.__pos_args__ = [*existing, *args, ]

  def _addKeywordArgs(self, **kwargs: Any) -> None:
    """
    Adds keyword arguments to the Waila instance.
    """
    existing = self._getKeywordArgs()
    for key, value in kwargs.items():
      if key not in existing:
        existing[key] = value
        continue
      raise NotImplementedError('duplicate key: %s' % key)
    self.__key_args__ = existing

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getEntryHeaderWidth(self, ) -> int:
    """
    Returns the width required by the entry header.
    """
    return max(len(self.posEntryHeader), len(self.keyEntryHeader))

  def _getPosEntrySpec(self) -> str:
    """
    Get the format specification for the positional entry in the summary.
    """
    args = self._getPositionalArgs() or ['']
    spec = """Index: %%%dd""" % len(str(len(args)))
    sample = spec % len(args)
    if len(sample) < self._getEntryHeaderWidth():
      return spec.rjust(self._getEntryHeaderWidth())
    return spec

  def _getKeyEntrySpec(self) -> str:
    """
    Get the format specification for the key entry in the summary.
    """
    args, kwargs = self._getPositionalArgs(), self._getKeywordArgs()
    keys = sorted([k for k, v in kwargs.items()], key=len) or ['']
    spec = """Key: %%%ds""" % len(keys[-1])
    sample = spec % keys[-1]
    if len(sample) < self._getEntryHeaderWidth():
      return spec.rjust(self._getEntryHeaderWidth())
    return spec

  def _getTypeHeaderWidth(self) -> int:
    """
    Returns the width required by the type header.
    """
    return max(len(self.posTypeHeader), len(self.keyTypeHeader))

  def _getTypeSpec(self, ) -> str:
    """
    Get the format specification for the type of the value.
    """
    args, kwargs = self._getPositionalArgs(), self._getKeywordArgs()
    argTypes = [type(arg).__name__ for arg in args]
    keyTypes = [type(v).__name__ for k, v in kwargs.items()]
    types = sorted([*argTypes, *keyTypes, ], key=len) or ['']

  def __call__(self, *args, **kwargs) -> str:
    """
    Call the Waila instance to get a formatted summary of positional and
    keyword arguments.
    """
    posEntrySpec = """Index: %%%dd""" % len(str(len(args)))
    keys = [k for k, v in kwargs.items()]
    longestKey = max([len(str(k)) for k in keys], default=0)
    keyEntryLength = max(len(posEntrySpec % len(args)), longestKey)
    keyEntrySpec = """Key: %%%ds""" % keyEntryLength
