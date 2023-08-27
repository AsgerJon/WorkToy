"""WorkToy - Core - Type collection
This module provides shorthands for many commonly used types."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Union

Sample = type('Sample', (), dict(clsMethod=classmethod(lambda cls: cls)))
Map = Union[type(type('_', (), {}).__dict__), dict]
Keys = type({}.keys())
Values = type({}.values())
Items = type({}.items())
Bases = tuple[type, ...]
Type = type(type('_', (), {}))
Function = (type(getattr(type('_', (), {'_': lambda self: self}), '_')))
Method = (type(getattr(type('_', (), {'_': lambda self: self})(), '_')))
WrapperDescriptor = type(type('_', (), {}).__init__)
WrapperMethod = type(type('_', (), {}).__call__)
BuiltinFunction = type(print)
Functional = Union[WrapperDescriptor, WrapperMethod, Function, Method]
FunctionTuple = (Function, Method, WrapperDescriptor, WrapperMethod,
                 BuiltinFunction)
FunctionList = [*FunctionTuple, ]
Functions = Union[
  Function, Method, WrapperDescriptor, WrapperMethod, BuiltinFunction]
