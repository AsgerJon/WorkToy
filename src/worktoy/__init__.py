"""WorkToy - MetaWork
This module provides the metaclass and namespace classes for the remaining
package"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._primitiveclass import PrimitiveClass, Map, Keys, Values, Items
from ._primitiveclass import Bases, Type, Function, Method, Type, Bases
from ._primitiveclass import WrapperDescriptor, WrapperMethod, Method
from ._primitiveclass import BuiltinFunction, FunctionList, Functional
from ._parsingclass import ParsingClass
from ._exceptionclass import ExceptionClass
from ._defaultclass import DefaultClass
from ._workthis import WorkThis
from ._abstractdescriptor import AbstractDescriptor
from ._decoratordescriptor import DecoratorDescriptor
from ._abstractmetatype import MetaMetaType, AbstractMetaType, AbstractType
