"""
ControlSpace provides the namespace object for the control flow
exceptions.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import maybe
from ...waitaminute.meta import ControlClassError

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Type, TypeAlias

  from . import MetaFlow

  Bases: TypeAlias = tuple[type, ...]
  Meta: TypeAlias = Type[MetaFlow]


class ControlSpace(dict):
  """
  A control-flow signal is used by its type alone: it is raised, caught
  by type, and carries nothing. A signal class defining methods or state
  is therefore a mistake, and the mistake should fail at the line making
  it rather than later. The body of a signal still binds the names Python
  writes into every class body, a docstring among them, and may define
  its own text.

  Implementation
  --------------

  'MetaFlow.__prepare__' creates the namespace. '__setitem__' admits the
  names in '__white_list__' ('__str__', '__repr__' and the names the
  interpreter writes, such as '__classcell__'), and any name 'Exception'
  holds as an attribute that is not callable, such as '__module__',
  '__qualname__' and '__doc__'. Every other name raises
  'ControlClassError'. The body of the root signal, declared with
  '_root=True', is not checked. 'MetaType' writes '__namespace__' into
  the class past '__setitem__', as for every class it builds.

  Attributes
  ----------

  __white_list__ : tuple[str, ...]
    The names always admitted.

  __metaclass__, __base_classes__, __class_name__ : Any
    The metaclass, bases and name of the signal, for the message of
    'ControlClassError'.

  __is_root__ : bool
    Whether the body is that of the root signal.
  """

  #  The interpreter binds '__classcell__' when a method uses 'super()',
  #  and '__classdictcell__' as well from Python 3.14.
  __white_list__ = (
    '__firstlineno__',
    '__str__',
    '__repr__',
    '__static_attributes__',
    '__classcell__',
    '__classdictcell__',
  )

  __is_root__ = None
  __metaclass__: Meta = None
  __base_classes__ = None
  __class_name__ = None

  @classmethod
  def _getWhiteList(cls, ) -> tuple[str, ...]:
    return maybe(cls.__white_list__, ())

  def __init__(self, mcls: Meta, name: str, bases: Bases, **kw) -> None:
    dict.__init__(self, )
    self.__metaclass__ = mcls
    self.__base_classes__ = bases
    self.__class_name__ = name
    self.__is_root__ = True if kw.get('_root', False) else False

  def __setitem__(self, key: str, value: Any) -> None:
    if key in self._getWhiteList():
      return dict.__setitem__(self, key, value)
    if not maybe(self.__is_root__, False):
      try:
        existing = getattr(Exception, key)
      except AttributeError:
        raise ControlClassError(self, key)
      else:
        if callable(existing):
          raise ControlClassError(self, key)
    return dict.__setitem__(self, key, value)
