"""
ExtraKeywordException is raised when an 'EZData' class is called with a
keyword argument that names none of its fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt, NoPickle


class ExtraKeywordException(NoPickle, TypeError):
  """
  ExtraKeywordException is raised when an 'EZData' class is called with a
  keyword argument that names none of its fields, such as 'givenName' for
  a field named 'givenNames'. Such a keyword would otherwise be dropped
  without a word, leaving the field at its default. The message lists the
  field names the class accepts. It is the keyword counterpart of
  'ExtraPositionalException', and subclasses 'TypeError', as Python's own
  refusal of an unexpected keyword argument does.

  Attributes
  ----------
  cls : type
    The 'EZData' class that received the keyword.
  keyword : str
    The keyword that names none of the fields.
  fieldNames : tuple[str, ...]
    The names of the fields of the class.
  """

  __slots__ = ('cls', 'keyword', 'fieldNames')

  def __init__(self, cls: type, keyword: str, *fieldNames: str) -> None:
    self.cls = cls
    self.keyword = keyword
    self.fieldNames = fieldNames
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """EZData class '%s' received the keyword '%s', which names
    none of its fields. The fields are: %s."""
    fieldNames = ', '.join("""'%s'""" % name for name in self.fieldNames)
    info = infoSpec % (self.cls.__name__, self.keyword, fieldNames)
    return textFmt(info)

  __repr__ = __str__
