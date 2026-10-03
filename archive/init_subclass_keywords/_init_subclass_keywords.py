"""
The 'initSubclassKeywords' function names the class keywords that the
'__init_subclass__' methods of some classes declare by name.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from inspect import signature, Parameter
from types import FunctionType


def _declaredNames(func: FunctionType) -> list[str]:
  """
  The '_declaredNames' function lists the parameters of 'func' that a
  class statement can give by keyword: every named parameter after the
  first, which receives the class, by position or keyword only. A
  '**kwargs' catch-all names nothing.
  """
  named = (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY)
  params = [p for p in signature(func).parameters.values()]
  out = []
  for param in params[1:]:
    if param.kind in named:
      out.append(param.name)
  return out


def initSubclassKeywords(*classes: type) -> tuple[str, ...]:
  """
  The 'initSubclassKeywords' function names the class keywords that the
  '__init_subclass__' methods of 'classes' declare by name, in the order
  of the classes, each name once.

  Only an '__init_subclass__' written in Python in the namespace of the
  class itself counts, since a class inheriting one declares nothing of
  its own, and a builtin such as 'object.__init_subclass__' takes no
  keyword. A '**kwargs' catch-all declares no keyword either: it promises
  to pass anything on, and what reaches 'object.__init_subclass__' is
  refused there.

  Parameters
  ----------
  *classes : type
      The classes whose own '__init_subclass__' methods are read.

  Returns
  -------
  tuple[str, ...]
      The declared keywords, in the order of the classes, without
      repetition.

  Examples
  --------
  >>> class Tagged:
  ...   def __init_subclass__(cls, tag=None, **kwargs):
  ...     super().__init_subclass__(**kwargs)
  ...     cls.tag = tag
  >>> initSubclassKeywords(Tagged, object)
  ('tag',)
  """
  out = []
  for cls in classes:
    func = cls.__dict__.get('__init_subclass__', None)
    func = getattr(func, '__func__', func)
    if not isinstance(func, FunctionType):
      continue
    for name in _declaredNames(func):
      if name not in out:
        out.append(name)
  return (*out,)
