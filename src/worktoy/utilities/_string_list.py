"""
The 'stringList' takes a string and returns a list of strings containing
substrings separated by a separator (default: ', ').

Keyword argument 'sep' specifies the separator(s) to use. More than one
separator may be specified by passing a non-empty iterable of strings.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import maybe


def stringList(*args: str, **kwargs: str) -> list[str]:
  """
  Splits input strings using all provided separators in sequence.

  Keyword-only argument 'sep' may be a string or list of strings. Each
  separator is applied in turn, so that later separators act on results
  of earlier splits.
  """
  seps = kwargs.get('seps', None)
  sep = kwargs.get('sep', None)
  if sep is None:
    sep = kwargs.get('separator', None)
  if seps is not None and sep is not None:
    raise ValueError("Specify either 'sep' or 'seps', not both.")
  if seps is None:
    seps = [maybe(sep, ', '), ]
  posArgs = [str(arg) for arg in args if str(arg)]
  for sep in seps:
    base = sep.join([*posArgs, ])
    posArgs = base.split(sep)
  return [s.strip() for s in posArgs if s.strip() != '']
