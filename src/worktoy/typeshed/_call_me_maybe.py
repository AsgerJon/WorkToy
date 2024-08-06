"""This file provides typing.Callable or similar."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


def _CallMeMeta(BaseMeta):
  def __new__(cls, name, bases, namespace, **kwargs):
    return super().__new__(cls, name, bases, namespace, **kwargs)
