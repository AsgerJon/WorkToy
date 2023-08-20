"""The worktype provides functionalities relating to type hinting"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from ._typingversions import CallMeMaybe

if not TYPE_CHECKING:
  from ._abstractmetatype import AbstractMetaType
  from ._abstracttype import AbstractType
  from ._callmemaybe import CallMeMaybe
