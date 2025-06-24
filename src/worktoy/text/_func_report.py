"""The 'funcReport' analyses a function object and returns a string
description of it including name, typehints and docstring. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from inspect import signature
from typing import get_type_hints
from types import FunctionType

from . import monoSpace

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


def funcReport(func: FunctionType, **kwargs) -> str:
  """The 'funcReport' analyses a function object and returns a string
  description of it including name, typehints and docstring. """

  docString = getattr(func, '__doc__', None)
  if not docString:
    if kwargs.get('strict', True):
      e = """No docstring found!"""
      raise SyntaxError(e)
    docString = """Imagine not providing a docstring!"""
  typeHints = get_type_hints(func)
  typeSig = signature(func)
  funcName = getattr(func, '__name__', 'unknown')
  #  Collecting parameter kinds from the 'inspect.Signature' object
  paramKinds = dict(oneStar='', twoStars='')
  for (key, param) in typeSig.parameters.items():
    if param.kind.name == 'VAR_POSITIONAL':
      paramKinds['oneStar'] = """*%s""" % param.name
    if param.kind.name == 'VAR_KEYWORD':
      paramKinds['twoStars'] = """**%s""" % param.name
  #  Collecting type hints
  posArgs = []
  returnType = None
  for (name, type_) in typeHints.items():
    if name == 'return':
      returnType = type_
      continue
    posArgs.append("""%s: %s""" % (name, type_.__name__))
  else:
    if returnType is None:
      if kwargs.get('strict', True):
        e = """No return type hint found!"""
        raise SyntaxError(e)
      returnType = type(None)
  if paramKinds['oneStar']:
    posArgs.append(paramKinds['oneStar'])
  if paramKinds['twoStars']:
    posArgs.append(paramKinds['twoStars'])
  #  Formatting the output
  argStr = ', '.join(posArgs)
  if returnType is type(None):
    outName = 'None'
  else:
    outName = returnType.__name__
  fmtSpec = """def %s(%s) -> %s:<br><tab>\"\"\"%s\"\"\""""
  out = fmtSpec % (funcName, argStr, outName, docString)
  return monoSpace(out)
