"""WorkToy - BaseTypes
This module provides a few base types"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

Sample = type('Sample', (), dict(clsMethod=classmethod(lambda cls: cls)))
Keys = type({}.keys())
Values = type({}.values())
Items = type({}.items())
Bases = tuple[type, ...]
Type = type(type('_', (), {}))
Function = (type(getattr(type('_', (), {'_': lambda self: self}), '_')))
Method = (type(getattr(type('_', (), {'_': lambda self: self})(), '_')))
WrapperDescriptor = type(type('_', (), {}).__init__)
WrapperMethod = type(type('_', (), {}).__call__)
BuiltinFunction = type(type('_', (), {}).__new__)

__all__ = [Keys,
           Values,
           Items,
           Bases,
           Type,
           Function,
           Method,
           WrapperDescriptor,
           WrapperMethod,
           BuiltinFunction]

ALL = __all__
