"""WorkToy - Fields
Implementation of descriptors as fields."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._abstractdescriptor import AbstractDescriptor
from ._callmemaybe import CallMeMaybe, CALL
from ._classdescriptor import ClassDescriptor, CLASS
from ._flag import FLAG
from ._floatdescriptor import FloatDescriptor, FLOAT
from ._integerdescriptor import IntegerDescriptor, INT
from ._listdescriptor import ListDescriptor, LIST
from ._stringdescriptor import StringDescriptor, STR
from ._abstractparams import AbstractParams, Parameter
