"""WorkToy - Core
The core module provides the chain of default classes:
  'PrimitiveClass'
  'ParsingClass'
  'ExceptionClass'
  '...'
  'DefaultClass'
The final class should be called DefaultClass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._primitiveclass import Map, Keys, Values, Items, Bases, Type
from ._primitiveclass import Function, Method, WrapperDescriptor
from ._primitiveclass import WrapperMethod, BuiltinFunction, Functional
from ._primitiveclass import FunctionTuple, FunctionList

from ._primitiveclass import PrimitiveClass
from ._parsingclass import ParsingClass
from ._exceptionclass import ExceptionClass
from ._defaultclass import DefaultClass
