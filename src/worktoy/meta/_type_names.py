"""This file provides some common type aliases used by 'worktoy.meta'. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Tuple, Callable

from worktoy.meta import AbstractNamespace


def functionInstance() -> None:
  pass


Function = type(functionInstance)

FunctionTypes: TypeAlias = Union[Function, classmethod, staticmethod]
Bases: TypeAlias = Union[type, Tuple[type, ...]]
Namespace: TypeAlias = Union[dict, AbstractNamespace]
Space: TypeAlias = Namespace
FunctionDecorator: TypeAlias = Callable[[Callable], Callable]
ClassDecorator: TypeAlias = Callable[[type], type]
Decorator: TypeAlias = Union[FunctionDecorator, ClassDecorator]
