"""
RecordingMeta is a metaclass of another library that records every class
it builds, with the class keywords.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations


class RecordingMeta(type):
  """
  'MetaType.__init__' hands every class on to the next '__init__' along
  the resolution order of the metaclass building it, with every class
  keyword, so a metaclass of another library combined with a worktoy one
  still does its work. 'RecordingMeta' is such a metaclass: its
  '__init__' appends the name of each class and its keywords to
  'records' and hands on in turn.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  records: list = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(cls, name: str, bases: tuple, space: dict, **kw) -> None:
    RecordingMeta.records.append((name, dict(kw)))
    super().__init__(name, bases, space)
