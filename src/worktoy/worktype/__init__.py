"""
WorkToy - WorkType
Functionalities relating to type hinting"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._abstractattribute import AbstractAttribute
from ._abstractmetatype import AbstractMetaType
from ._metanamespace import MetaNameSpace, AbstractNameSpace
from ._typenamespace import TypeNameSpace
from ._abstracttype import AbstractType

if TYPE_CHECKING:
  from ._typingversions import CallMeMaybe
else:
  from ._callmemaybe import CallMeMaybe
