"""WorkToy as a class is an abstract baseclass"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import json
import os
from typing import Any, Optional, NoReturn, Never
import webbrowser

from icecream import ic

from worktoy import searchKeys, maybeType, maybe, Args, Kwargs, Value, \
  WorkDict, Field, monoSpace

ic.configureOutput(includeContext=True)


class WorkToy(type):
  """WorkToy as a class is an abstract baseclass
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @classmethod
  def __prepare__(mcs, name: str, bases: tuple = None) -> dict:
    """Returns the mapping"""
    return WorkDict()

  def __new__(mcs, name: str, bases: Any, nameSpace: Any, **kwargs) -> Any:
    """Creates a new class"""

    space = {}

    def fmtSpec() -> str:
      """Defines a formatting specification used when trying to create a
      generic filename. In subclasses, this can be overwritten. In that
      case, the new method must define a filename as a function of a
      positive integer such that no two integers produces the same
      filename. Subclasses must ensure this requirement as no validation
      is applied."""
      return 'untitled%02d.json'

    space |= {'fmtSpec': fmtSpec}

    def _genPath(self, ) -> NoReturn:
      """Ensures the existing of a proper path to a save directory when
      one is not explicitly defined"""
      last = os.path.dirname(os.path.abspath(__file__))
      there = os.getenv('APPDATA')
      here = os.getenv('WORKTOYPATH')
      if here is None:
        if there is not None:
          dirName = os.path.join(there, 'worktoy')
          try:
            os.mkdir(dirName, )
          except FileExistsError as fileExistsError:
            msg = """Encountered %s when looking for worktoy path in 
            directory at environment variable 'APPDATA'. This is fine."""
            self._log(monoSpace(msg) % fileExistsError)
          except FileNotFoundError as fileNotFoundError:
            msg = """Encountered %s when looking for worktoy path in 
            directory at environment variable 'APPDATA'. This is NOT fine!"""
            self._log(monoSpace(msg) % fileNotFoundError)
            there = None
      if here is None:
        if there is None:
          self._path = last
        else:
          self._path = there
      else:
        self._path = here

    space |= {'_genPath': _genPath}

    def _getPath(self, ) -> str:
      """Getter-function for path to save directory"""
      if self._path is None:
        self._genPath()
        return self._getPath()
      return self._path

    space |= {'_getPath': _getPath}

    def _setPath(self, path: str) -> NoReturn:
      """Setter-function for path to save directory"""
      self._path = path

    space |= {'_setPath': _setPath}

    def _delPath(self, ) -> Never:
      """Illegal deleter function"""
      raise TypeError('Read Only Error')

    space |= {'_delPath': _delPath}

    def _getFileName(self, ) -> str:
      """Getter-function for file name"""
      c = 0
      fileName = self.fmtSpec % c
      basePath = self._getPath()
      while os.path.exists(os.path.join(basePath, fileName)):
        fileName = self.fmtSpec % c
        c += 1
      return fileName

    space |= {'_getFileName': _getFileName}

    def _getFid(self, ) -> NoReturn:
      """Tries to create a file named 'untitled00.json' at the location of
      the standard directory incrementing at each attempt. This behaviour
      is defined by the fmtSpec static method. Overwrite in a subclass to
      change to a custom style."""
      return os.path.join(self._getPath(), self._getFileName())

    space |= {'_getFid': _getFid}

    def saveInstance(self, ) -> NoReturn:
      """Saves the instance fields to disk"""
      fieldJson = {}
      for field in self._fields:
        fieldJson |= {field.name: field.value}
      data = json.dumps(fieldJson)
      with open(self.fid, 'w') as f:
        f.write(data)

    space |= {'saveInstance': saveInstance}

    @classmethod
    def newInstanceFromFile(self, saveFile: str) -> Any:
      """Creates a new instance and populates fields with data found in
      the saveFile"""
      raise NotImplementedError('Not yet implemented')

    space |= {'newInstanceFromFile': newInstanceFromFile}

    def loadFileInPlace(self, saveFile: str) -> Any:
      """Loads the file and overwrites existing field values."""
      raise NotImplementedError('Not yet implemented')

    space |= {'loadFileInPlace': loadFileInPlace}

    baseInit = nameSpace.get('__init__', None)

    space |= {'baseInit': baseInit}

    def newInit(self, *args, **kwargs_) -> None:
      """This init augments the class init function"""
      self._fields = []
      self._dirPath = os.getenv('WORKTOYPATH')
      self._fid = 'untitled.json'
      for field in nameSpace.fields:
        name_ = field.name
        Name = name_[0].upper() + name_[1:]
        getName = '_get%s' % Name
        setName = '_set%s' % Name
        delName = '_del%s' % Name
        setattr(self, field.name, property(
          getattr(field, '_getVal'),
          getattr(field, '_setVal'),
          getattr(field, '_delVal'),
        ))
        setattr(self, getName, getattr(field, '_getVal'), )
        setattr(self, setName, getattr(field, '_setVal'), )
        setattr(self, delName, getattr(field, '_delVal'), )
        self._fields.append(field)
      Field.clearSlots()
      if baseInit is not None:
        baseInit(self, *args, **kwargs_)

    nameSpace['__init__'] = newInit
    for (name, func) in space.items():
      if nameSpace.get(name, None) is None:
        nameSpace[name] = func

    return super().__new__(mcs, name, bases, nameSpace, **kwargs)
