"""FidGen provides filename generator. Given a format specification and a
directory, it returns the next available filename of the given format."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os

from worktoy.attr import Field
from worktoy.mcls import BaseObject
from worktoy.parse import maybe
from worktoy.static import overload
from worktoy.text import stringList
from worktoy.waitaminute import TypeException, MissingVariable
from worktoy.work_io import validateExistingDirectory

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional


class FidGen(BaseObject):
  """
  FidGen provides filename generator. Given a format specification and a
  directory, it returns the next available filename of the given format.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables
  __fallback_extension__ = 'json'
  __fallback_name__ = 'untitled'
  __fallback_directory__ = Field()

  #  Private variables
  __base_name__ = None
  __file_extension__ = None
  __file_directory__ = None

  #  Public variables
  fileExtension = Field()
  fileDirectory = Field()
  baseName = Field()

  #  Virtual variables
  filePath = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  @__fallback_directory__.GET
  def _getFallbackDirectory(self, **kwargs) -> str:
    """
    Getter-function for the fallback directory.
    """
    return os.getcwd()

  @baseName.GET
  def _getBaseName(self, ) -> str:
    """Get the name of the file."""
    if isinstance(self.__base_name__, str):
      return self.__base_name__
    if isinstance(self.owner, type):
      return self.owner.__name__
    return self.__fallback_name__

  @fileExtension.GET
  def _getFileExtension(self, **kwargs) -> str:
    """Get the file extension."""
    return maybe(self.__file_extension__, self.__fallback_extension__, )

  @fileDirectory.GET
  def _getFileDirectory(self, **kwargs) -> str:
    """Get the file directory."""
    return maybe(self.__file_directory__, self.__fallback_directory__, )

  @filePath.GET
  def _getFilePath(self, **kwargs) -> str:
    """Getter-function for the file path. """
    n = kwargs.get('_n', 0)
    formatSpec = """%s_%03d"""
    fid = formatSpec % (self.baseName, n,)
    for item in os.listdir(self.fileDirectory):
      if item.startswith(fid):
        return self._getFilePath(_n=n + 1, )
    fidExt = """%s.%s""" % (fid, self.fileExtension)
    out = os.path.join(self.fileDirectory, fidExt)
    return str(out)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Setter methods
  @baseName.SET
  def _setBaseName(self, newName: str) -> None:
    """Set the name of the file."""
    if self.__base_name__ == newName:
      return
    if not isinstance(newName, str):
      raise TypeException('__name__', newName, str)
    if not newName:
      raise ValueError('__name__ must be a non-empty string')
    self.__base_name__ = newName

  @fileExtension.SET
  def _setFileExtension(self, value: str) -> None:
    """Set the file extension."""
    if not isinstance(value, str):
      raise TypeException('__file_extension__', value, str)
    if not value:
      raise ValueError('__file_extension__ must be a non-empty string')
    self.__file_extension__ = value

  @fileDirectory.SET
  def _setFileDirectory(self, value: str, **kwargs) -> None:
    """Set the file directory."""
    if not isinstance(value, str):
      raise TypeException('__file_directory__', value, str)
    if not value:
      raise ValueError('__file_directory__ must be a non-empty string')
    try:
      validateExistingDirectory(value)
    except FileNotFoundError as e:
      if kwargs.get('_recursion', False):
        raise RecursionError from e
      os.makedirs(value, exist_ok=True)
      return self._setFileDirectory(value, _recursion=True)
    else:
      self.__file_directory__ = value
    finally:
      pass  # NOQA

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(str)
  def __init__(self, fileName: str, **kwargs) -> None:
    """Initialize the FidGen object."""
    self.__base_name__ = fileName
    self.__init__(**kwargs)

  @overload(str, str, str)
  @overload(str, str)
  def __init__(self, *args, **kwargs) -> None:
    argDir = self._findDirectory(*args)
    argExt = self._findFileExtension(*args)
    for arg in args:
      if arg in [argDir, argExt]:
        continue
      self.baseName = arg
      break
    if argDir is not None:
      self.fileDirectory = argDir
    if argExt is not None:
      self.fileExtension = argExt
    self.__init__(**kwargs)

  @overload()  # kwargs
  def __init__(self, **kwargs) -> None:
    """Initialize the FidGen object."""
    nameKeys = stringList("""name, file, fileName, filename, file_name""")
    extKeys = stringList("""ext, extension, file_extension""")
    dirKeys = stringList("""dir, directory, file_directory""")
    KEYS = [nameKeys, extKeys, dirKeys]
    NAMES = stringList("""name, ext, dirPath""")
    TYPES = dict(name=str, ext=str, dirPath=str)
    VALUES = dict()
    for (keys, (name, type_)) in zip(KEYS, TYPES.items()):
      for key in keys:
        if key in kwargs:
          value = kwargs[key]
          if isinstance(value, type_):
            VALUES[name] = value
            break
          raise TypeException(key, value, type_)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _findDirectory(*args) -> Optional[str]:
    """Finds the directory in positional arguments. """
    for arg in args:
      if isinstance(arg, str):
        if os.path.isabs(arg):
          return arg
    return None  # pycharm, please!

  @staticmethod
  def _getCommonExtensions() -> list[str]:
    """Returns a list of common file extensions."""
    return stringList(
        """json, txt, csv, xml, html, pdf, doc, csv, py, 
        mkv, mp4, mp3, wav, jpg, png, gif, zip, tar, gz, bz2"""
    )

  @classmethod
  def _findFileExtension(cls, *args) -> Optional[str]:
    """Finds the file extension in positional arguments. """
    commonExtensions = cls._getCommonExtensions()
    for arg in args:
      if isinstance(arg, str):
        if str.startswith(arg, '*.'):
          return arg[2:]
        if arg in commonExtensions:
          return arg
    return None  # pycharm, please!
