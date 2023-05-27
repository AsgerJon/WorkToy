"""CallMeMaybe represents callable types."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from abc import abstractmethod
import collections.abc
import typing

from icecream import ic

from worktoy.core import FlexUnPack, maybe
from worktoy.waitaminute import ProceduralError

ic.configureOutput(includeContext=True)

_HereIsMyNumber = getattr(typing, '_GenericAlias', None)
_ThisIsCrazy = getattr(typing, 'Callable', None)
_TryToChaseMe = getattr(collections.abc, 'Callable', None)


class _CallMeMaybe(_HereIsMyNumber, _root='F... da police!'):
  """Is this it?"""
  __baseclass__ = True
  __CallMeMaybe__ = True
  domain = False
  range_ = False

  @classmethod
  def __init_subclass__(cls, /, *args, **kwargs):
    """ClassFail"""

  def __init__(self, *args, **kwargs) -> None:
    _HereIsMyNumber.__init__(self, *args, **kwargs)

  @classmethod
  def __instancecheck__(cls, instance) -> bool:
    """Implementing instance check. Subclasses must reimplement this
    method!"""
    ic()
    baseCheck = getattr(cls, '__baseclass__', None)
    if baseCheck is None:
      raise ProceduralError('__baseclass__', bool, None)
    if not baseCheck:
      msg = """Base class instance check applied to class with base class 
      flag False. This indicates that the class %s has not properly 
      implemented the '__instancecheck__' class method.""" % cls.__name__
      from worktoy.stringtools import justify
      msg = justify(msg)
      raise ProceduralError('__baseclass__', bool, baseCheck, info=msg)
    insCls = getattr(instance, '__class__', None)
    if insCls is None:
      raise ProceduralError(insCls, type, None)
    if 'function' in [insCls.__name__, insCls.__qualname__]:
      ic(insCls)
      return True
    return True if insCls.__name__ == cls.__name__ else False

  def __str__(self, ) -> str:
    """String representation"""
    return 'CallMeMaybe'

  def __repr__(self, ) -> str:
    """Code representation"""
    return 'CallMeMaybe'


class NothingAtAll(_CallMeMaybe):
  """HereIsMeNumber!"""
  _instance = None

  def __new__(cls, *args, **kwargs) -> NothingAtAll:
    if not cls._instance:
      cls._instance = super().__new__(cls)
    return cls._instance

  @staticmethod
  def _validateType(cls, ) -> type:
    """This method validates the given class with comprehensive error
    handling. """
    baseCheck = getattr(cls, '__baseclass__', None)
    if baseCheck is None:
      msg = """Base class flag must be set to False for pseudo instances! 
      In this instance the flag is missing altogether."""
      from worktoy.stringtools import justify
      msg = justify(msg)
      raise ProceduralError(cls, bool, '__baseclass__', info=msg)
    if not baseCheck:
      msg = """Base class instance check applied to class with base class 
      flag False. This indicates that the class %s has not properly 
      implemented the '__instancecheck__' class method.""" % cls.__name__
      from worktoy.stringtools import justify
      msg = justify(msg)
      raise ProceduralError('__baseclass__', bool, baseCheck, info=msg)
    return cls

  @classmethod
  def __instancecheck__(cls, instance: typing.Any) -> bool:
    """Reimplementation"""
    return True if callable(instance) else False

  @classmethod
  def __eq__(cls, other) -> bool:
    """Compares the domain and range"""
    selfDomain = getattr(cls, 'domain', None)
    otherDomain = getattr(cls, 'domain', None)
    if selfDomain is None:
      raise ProceduralError(cls, tuple[type], 'domain')
    if otherDomain is None:
      raise ProceduralError(other, tuple[type], 'domain')
    if len(selfDomain) != len(otherDomain):
      return False
    for (a, b) in zip(selfDomain, otherDomain):
      if a != b:
        return False
    return True

  def __init__(self, *__, **_) -> None:
    _CallMeMaybe.__init__(self, _TryToChaseMe, (bool,))

  def _typeStrings(self) -> str:
    """Types as strings"""
    types = getattr(self, '__signature__', None)
    if types is None:
      return ''
    out = []
    for type_ in types:
      out.append(type_.__name__)
    return '[%s]' % ', '.join(out)

  def __str__(self) -> str:
    """String representation"""
    types = getattr(self, '__signature__', None)
    if types is None:
      return 'Base Class for CallMeMaybe'
    return """CallMeMaybe with signature: %s""" % self._typeStrings()

  def __repr__(self) -> str:
    """String representation"""
    types = getattr(self, '__signature__', None)
    if types is None:
      return 'CallMeMaybe'
    return """CallMeMaybe @ [%s]""" % self._typeStrings()

  from worktoy.core import TypeBag
  T = TypeBag(tuple[type], list[type])

  def __call__(self, domain: T = None, range_: T = None) -> NothingAtAll:
    setattr(_CallMeMaybe, '_typeStrings', NothingAtAll._typeStrings)
    setattr(_CallMeMaybe, '__str__', NothingAtAll.__str__)
    setattr(_CallMeMaybe, '__repr__', NothingAtAll.__repr__)
    setattr(_CallMeMaybe, '__baseclass__', False)
    setattr(_CallMeMaybe, '__CallMeMaybe__', True)
    setattr(_CallMeMaybe, 'domain', ())
    setattr(_CallMeMaybe, 'range_', ())
    domain = (*maybe(domain, ()),)
    range_ = (*maybe(range_, ()),)
    cls = type(getattr(self, '__name__', 'lol'),
               (),
               dict(NothingAtAll.__dict__))
    setattr(cls, 'domain', domain)
    setattr(cls, 'range_', range_)
    setattr(cls, '__baseclass__', False)
    ic(cls)
    print(cls)
    return cls


newCallMeMaybe = NothingAtAll()
CallMeMaybe = newCallMeMaybe
