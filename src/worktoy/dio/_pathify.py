"""Pathify provides class methods for locating directories, ensuring their
existence or safely creating them. """
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import os
from typing import Never, Any

from icecream import ic

from worktoy.core import maybe, extractArg, empty, CallMeMaybe
from worktoy.field import Field
from worktoy.stringtools import stringList, justify
from worktoy.waitaminute import ExceptionCore, typeGuard

ic.configureOutput(includeContext=True)


class Pathify:
  """Pathify provides class methods for locating directories, ensuring their
  existence or safely creating them.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  _defaultEnv = 'WORKTOYPATH'
  _tempPath = None
  _recursionFlags = {
    '_tempPathVar' : False,
    '_tempPathFile': False,
  }

  @classmethod
  def _proceduralError(cls) -> Never:
    """Handles procedural errors"""
    raise ExceptionCore('Procedural error!')

  @classmethod
  def _createPath(cls) -> bool:
    """Creates the temporary path if it does not already exist."""
    if cls._tempPath is None:
      return cls._proceduralError()
    if os.path.isfile(cls._tempPath):
      raise NotADirectoryError
    if os.path.isdir(cls._tempPath):
      return True
    os.makedirs(cls._tempPath)
    return cls._createPath()

  @classmethod
  def _pathExists(cls) -> bool:
    """Checks if temporary path exists"""
    tempPath = cls._getPath()
    if tempPath is None:
      return False
    if os.path.isfile(tempPath):
      raise NotADirectoryError
    if os.path.isdir(tempPath):
      return True
    return False

  @classmethod
  def _location(cls, **kwargs) -> str:
    """This method specifies the desired location of the path. Subclasses
    should override this method to specify an alternate location. By
    default, the method tries to find an environment variable called
    'WORKTOYPATH' and then defaults to the current running directory. This
    environment variable name can be specified by the keyword argument
    'env'. Once the location is determined, it should be set at the
    _tempPath private class variable. """
    environmentVariable = kwargs.get('env', cls._defaultEnv)
    here = os.getcwd()
    cls._tempPath = maybe(os.getenv(environmentVariable), here)
    return cls._tempPath

  @classmethod
  def _getPath(cls) -> str:
    """Getter-function for the path name. This method provides collects
    the checks and possibly creates the path."""
    if cls._tempPath is None:
      if cls._recursionFlags['_tempPathVar']:
        raise RecursionError
      cls._recursionFlags['_tempPathVar'] = True
      cls._location()
      return cls._getPath()
    cls._recursionFlags['_tempPathVar'] = False
    if cls._pathExists():
      cls._recursionFlags['_tempPathFile'] = False
      return cls._tempPath
    if cls._recursionFlags['_tempPathFile']:
      raise RecursionError
    cls._recursionFlags['_tempPathFile'] = True
    cls._createPath()
    return cls._getPath()

  @classmethod
  def _parseArguments(cls, *args, **kwargs) -> tuple[str, str]:
    """Parses given arguments to environment name and path name"""
    envKeys = stringList('environment, env, var')
    env, a, k = extractArg(str, envKeys, *args, **kwargs)
    pathKeys = stringList('directory, dir, folder, path')
    pathName, a, k = extractArg(str, pathKeys, *a, **k)
    _envName = None
    _pathName = None
    envPath = None
    pathNameEnv = None
    #  Is 'env' an environment variable pointing to an existing path?
    if env is not None:
      envPath = os.getenv(env)
    if envPath is not None:
      if os.path.isdir(envPath):
        _envName = env
        _pathName = envPath
      elif os.path.isdir(env):
        _pathName = env
    else:
      if pathName is not None:
        pathNameEnv = os.getenv(pathName)
      if pathNameEnv is not None:
        if os.path.isdir(pathNameEnv):
          _envName = pathName
          _pathName = pathNameEnv
        elif os.path.isdir(pathName):
          _pathName = pathName
    if empty(_pathName, _envName):
      _envName = cls._defaultEnv
      _envPath = os.getenv(cls._defaultEnv)
    if empty(_pathName, _envName):
      msg = """Tried to instantiate Pathify, but could not parse arguments 
      to name of environment variable and class default environment 
      variable also failed. """
      raise ValueError(justify(msg))
    if _pathName is None:
      _pathName = os.getenv(_envName)
      if not os.path.isdir(_pathName):
        raise NotADirectoryError
    ic(_envName)
    ic(_pathName)
    return (_envName, _pathName)

  def __init__(self, *args, **kwargs) -> None:
    self._envName, self._pathName = self._parseArguments(*args, **kwargs)
    self._func = None

  def __call__(self, cls: type, *__, **_) -> type:
    """This method decorates classes such that instances have direct
    access to the path through the property 'here'. """
    typeGuard(cls, type)
    setattr(cls, '__pathified__', True)
    pathField = Field(fieldName='pathName', type_=str, allowGet=True,
                      allowSet=True, allowDel=False, defVal=self._pathName)
    envField = Field(fieldName='envName', type_=str, allowGet=True,
                     allowSet=False, allowDel=False, defVal=self._envName)
    cls = pathField(envField(cls))
    setattr(cls, '__pos__', self._parentDirFactory())
    return cls

  @staticmethod
  def _parentDirFactory() -> CallMeMaybe:
    """Creates a function which moves the path to the parent directory"""

    def func(instance: Any) -> Any:
      """Parent directory"""
      flag = getattr(getattr(instance, '__class__'), '__pathified__', False)
      if not flag:
        msg = """Object %s is not an instance of a pathified class!"""
        raise AttributeError(msg % instance)
      prevPath = getattr(instance, '_pathName', False)
      if not prevPath:
        msg = """Failed to find _pathName attribute on object %s!"""
        raise AttributeError(msg % instance)
      setattr(instance, '_pathName', os.path.dirname(prevPath))
      return instance

    funcDoc = """This method changes the current path pointed to by the 
    decorated instance to its parent directory."""
    funcAnnotations = {'return': 'Any'}
    func.__doc__ = funcDoc
    func.__annotations__ = funcAnnotations
    return func

  def _childDirFactory(self) -> CallMeMaybe:
    """Creates a function which change directory of the instance to the
    child folder of the given name. """

    def func(instance: Any) -> Any:
      """Parent directory"""
      flag = getattr(getattr(instance, '__class__'), '__pathified__', False)
      if not flag:
        msg = """Object %s is not an instance of a pathified class!"""
        raise AttributeError(msg % instance)
      prevPath = getattr(instance, '_pathName', False)
      if not prevPath:
        msg = """Failed to find _pathName attribute on object %s!"""
        raise AttributeError(msg % instance)
      setattr(instance, '_pathName', os.path.dirname(prevPath))
      return instance

    funcDoc = """This method changes the current path pointed to by the 
    decorated instance to its parent directory."""
    funcAnnotations = {'return': 'Any'}
    func.__doc__ = funcDoc
    func.__annotations__ = funcAnnotations
    return func
