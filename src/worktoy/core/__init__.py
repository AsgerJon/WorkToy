"""The 'worktoy.core' module contains functionality relying only on
builtins."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
from ._singletonclass import SingletonClass
from ._maybe import maybe
from ._plenty import plenty
from ._empty import empty
from ._typenames import CallMeMaybe, Args, Kwargs, ArgTuple, Value
from ._billions2one import randStr, builtin_types, randDict
from ._sometype import SomeType
from ._maybetype import maybeType
from ._searchkeys import searchKeys
from ._some import some
from ._maybetypes import maybeTypes

from ._extractarg import extractArg
