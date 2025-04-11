"""AbstractInstantiationException is a custom exception raised to indicate
an attempt to instantiate a class which possesses abstract methods. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import funcReport, monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.base import BaseMetaclass


class AbstractInstantiationException(TypeError):
  """AbstractInstantiationException is a custom exception raised to indicate
  an attempt to instantiate a class which possesses abstract methods. """

  def __init__(self, cls: BaseMetaclass, *args, **kwargs) -> None:
    posArgs = [*args, ]
    keyArgs = {**kwargs, }
    clsName = cls.__name__
    header = """Attempted to instantiate abstract class '%s':"""
    argStr = []
    for arg in posArgs:
      argStr.append(repr(arg))
    for key, arg in keyArgs.items():
      argStr.append("""%s=%s""" % (key, repr(arg)))
    if argStr:
      code = """  %s(%s)""" % (clsName, ', '.join(argStr))
    else:
      code = """  %s()""" % clsName
    body = """The class '%s' has the following abstract methods that 
    disallow instantiation: """
    funcReports = []
    for callMeMaybe in cls.getAbstractMethods():
      wrappedFunction = callMeMaybe.getWrappedFunction()
      report = funcReport(wrappedFunction).replace('\n', '<br><tab>')
      funcReports.append(report)
    funcStr = '<tab><br>'.join(funcReports)
    message = '<br>'.join([header % clsName, code, body % clsName, funcStr])
    TypeError.__init__(self, monoSpace(message))
