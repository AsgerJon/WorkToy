"""WorkToy - MetaWork
This module provides the metaclass and namespace classes for the remaining
package"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._basetypes import Keys, Values, Items, Function, Method, Type, Bases
from ._basetypes import WrapperDescriptor, WrapperMethod, BuiltinFunction
from ._defaultclass import DefaultClass
from ._abstractmetatype import AbstractMetaType, AbstractType
from ._metaattribute import MetaAttribute
from ._metanamespace import MetaNameSpace, AbstractNameSpace
from ._abstractattribute import AbstractAttribute
from ._immutableattribute import ImmutableAttribute
from ._mutableattribute import MutableAttribute
from ._listattribute import ListAttribute
from ._dictattribute import DictAttribute
from ._numattribute import NumAttribute
from ._intattribute import IntAttribute
from ._floatattribute import FloatAttribute
from ._strattribute import StrAttribute
from ._callmemaybe import CallMeMaybe
from ._attributenamespace import AttributeNameSpace
