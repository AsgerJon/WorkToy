"""The 'funcReport' analyses a function object and returns a string
description of it including name, typehints and docstring. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from inspect import signature
from typing import get_type_hints

from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.mcls import CallMeMaybe


def funcReport(func: CallMeMaybe) -> str:
  """The 'funcReport' analyses a function object and returns a string
  description of it including name, typehints and docstring. """

  docString = getattr(func, '__doc__', '')
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
      e = """No return type hint found!"""
      raise SyntaxError(e)
  if paramKinds['oneStar']:
    posArgs.append(paramKinds['oneStar'])
  if paramKinds['twoStars']:
    posArgs.append(paramKinds['twoStars'])
  #  Formatting the output
  argStr = ', '.join(posArgs)
  outName = returnType.__name__
  fmtSpec = """def %s(%s) -> %s:<br><tab>\"\"\"%s\"\"\""""
  out = fmtSpec % (funcName, argStr, outName, docString)
  return monoSpace(out)
