"""The 'worktoy.core' module contains functionality relying only on
builtins."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from ._copyclass import CopyClass
from ._unstupid import unStupid, unPack
from ._readtextfile import readTextFile
from ._singletonclass import SingletonClass
from ._maybe import maybe
from ._plenty import plenty
from ._empty import empty
from ._typenames import Args, Kwargs, ArgTuple, Value
from ._callmemaybe import CallMeMaybe

from ._billions2one import randStr, builtinTypes, randDict
from ._sometype import SomeType
from ._maybetype import maybeType
from ._searchkeys import searchKeys
from ._some import some
from ._maybetypes import maybeTypes
from ._typebag import TypeBag, Container, Numerical, TypeBagParent
from ._extractarg import extractArg
