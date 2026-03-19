"""
Index subclasses 'Chapter' and provides the top level content container.
This is analogous to the 'index.tex' in a LateX project.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
import webbrowser
from subprocess import Popen, PIPE
from threading import Thread
from typing import TYPE_CHECKING

from ..utilities import maybe, textFmt
from ..desc import AttriBox, Field
from . import Chapter, HeaderNum, TitleStyle

try:
  import grip
except ImportError:  # pragma: no cover
  grip = None

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Iterator

  StyleBox: TypeAlias = Union[TitleStyle, AttriBox]

  MaybeStr: TypeAlias = Optional[str]
  StrField: TypeAlias = Union[str, Field]


class Index(Chapter):
  """
  Index subclasses 'Chapter' and provides the top level content container.
  This is analogous to the 'index.tex' in a LateX project.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __header_level__: HeaderNum = HeaderNum.TITLE
  __dir_env_var__: str = 'MARKWORK_INDEX_DIR'

  #  Fallback Variables
  __fallback_dir__: str = None
  __fallback_port__: int = 6419

  #  Private Variables
  __base_name__: MaybeStr = None

  #  Public Variables
  headerStyle: StyleBox = AttriBox[TitleStyle]()
  baseName: StrField = Field()

  #  Virtual Variables
  header: StrField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @header.GET
  def _getHeader(self, ) -> str:
    return self.headerStyle.apply(self.title)

  @baseName.GET
  def _getBaseName(self, ) -> str:
    return maybe(
      self.__base_name__,
      self.__field_name__,
      type(self).__name__,
      )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @baseName.SET
  def _setBaseName(self, value: str, ) -> None:
    self.__base_name__ = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def fileDir(self, ) -> str:
    """
    Getter-function for the directory where the file is saved.
    """
    envVar = self.__dir_env_var__
    try:
      dirPath = os.environ[envVar]
    except KeyError:
      if self.__fallback_dir__ is None:
        return os.path.abspath(os.path.dirname(__file__))
      dirPath = os.path.abspath(self.__fallback_dir__)
      if os.path.isdir(dirPath):
        return dirPath
      if os.path.isfile(dirPath):
        infoSpec = """Path '%s' is a file, not a directory."""
        raise NotADirectoryError(infoSpec % dirPath)
      infoSpec = """Fallback directory '%s' does not exist."""
      raise FileNotFoundError(infoSpec % dirPath)
    else:
      return os.path.abspath(dirPath)

  def nextFile(self, ) -> str:
    """
    Returns the file path for the next file to be generated. This is used by
    the 'save' method to determine where to save the content of this
    instance.
    """
    fileName = """%s_%%03d.md""" % self.baseName
    dirPath = self.fileDir()
    _c = 0
    out = os.path.join(dirPath, fileName % _c)
    while os.path.exists(out):
      _c += 1
      out = os.path.join(dirPath, fileName % _c)
    else:
      return out

  def save(self, fid: MaybeStr = None, ) -> str:
    """
    Saves the content of this instance to the given file or to the
    auto-generated filePath at 'fidGen'.
    """
    if fid is None:
      fid = self.nextFile()
    f = None
    try:
      f = open(fid, 'w')
    except Exception as exception:  # pragma: no cover
      raise exception
    else:
      f.write(self.markdown())
    finally:
      try:
        f.close()
      except AttributeError:  # pragma: no cover
        pass
    return fid

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self, ) -> Iterator[Chapter]:
    chapters = self.getBlocksTuple()
    for chapter in chapters:
      yield chapter.__get__(self, type(self))
