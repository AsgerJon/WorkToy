"""WorkSide - Widgets - AttributeWidget
This descriptor classes wraps a widget class and should be set on other
widgets. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.widgets import CoreWidget
from worktoy import AbstractAttribute


class AttributeWidget(AbstractAttribute):
  """Widgets as attributes"""
  