"""
WYD is a custom exception class raised to indicate exceptions during
development of tests.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


class WYD(TypeError, ValueError):
  """
  Custom exception raised if something stupid happens because testing code.
  """

  def __init__(self, exception: Exception = None) -> None:
    """
    wut u doin bro?
    """
    if isinstance(exception, Exception):
      infoSpec = """Unexpected %s: '%s'"""
      excType = type(exception).__name__
      excStr = str(exception)
      info = infoSpec % (excType, excStr)
      Exception.__init__(self, info)
    elif isinstance(exception, str):
      Exception.__init__(self, exception)
    else:
      Exception.__init__(self, """wut u doin??""")
