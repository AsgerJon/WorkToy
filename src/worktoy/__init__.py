"""Documentation: WorkToy
Collection of General Utilities"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.typify import Kwargs, Args, Value, ArgTuple
from worktoy.parsify import plenty, maybe, SomeType, some
from worktoy.parsify import maybeTypes, searchKeys, maybeType
from worktoy.parsify import extractArg
from worktoy.mockdata import IntFactory, strFactory
from worktoy.stringtools import monoSpace, stringList
from worktoy.waitaminute import ExceptionCore, InstantiationError
from worktoy.waitaminute import ProceduralError, InstantiationError
from worktoy.typify import CallMeMaybe
from worktoy.core import Field
