"""ViewField subclasses FunctionField and provides what appears to be a
field, but which is in fact a particular view. Instead of returning the
value of a private variable, it computes a value and returns."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.field import FunctionField


class ViewField(FunctionField):
  """ViewField subclasses FunctionField and provides what appears to be a
  field, but which is in fact a particular view. Instead of returning the
  value of a private variable, it computes a value and returns it."""
