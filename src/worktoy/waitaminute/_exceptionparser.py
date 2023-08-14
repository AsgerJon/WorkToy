"""ExceptionParser subclasses the AbstractParser. The custom exceptions
found in the WorkToy package share this one parser. When raising one of
these exceptions, pass the class, instance, method being called along with
the variable name involved and its type. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never

from worktoy.parsing import AbstractParser


class ExceptionParser(AbstractParser):
  """ExceptionParser subclasses the AbstractParser. The custom exceptions
  found in the WorkToy package share this one parser. When raising one of
  these exceptions, pass the class, instance, method being called along with
  the variable name involved and its type. """

  def __init__(self, *args, **kwargs) -> None:
    AbstractParser.__init__(self, *args, **kwargs)
