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

from ._coretypes import Map, Keys, Values, Items, Bases, Type
from ._coretypes import Function, Method, WrapperDescriptor
from ._coretypes import WrapperMethod, BuiltinFunction, Functional
from ._coretypes import FunctionTuple, FunctionList

from ._coreclass import CoreClass
from ._stringaware import StringAware

from ._abstractdescriptor import AbstractDescriptor
from ._flag import FLAG
from ._listdescriptor import LIST
from ._integerdescriptor import IntegerDescriptor, INT
from ._floatdescriptor import FloatDescriptor, FLOAT
from ._classdescriptor import ClassDescriptor, CLASS
from ._stringdescriptor import StringDescriptor, STR
from ._callmemaybe import CallMeMaybe, CALL

from ._cls import CLS
from ._abstracttask import AbstractTask
from ._monitortask import MonitorTask
from ._exceptionclass import ExceptionClass
from ._defaultclass import DefaultClass

from ._testclass import TestClass
