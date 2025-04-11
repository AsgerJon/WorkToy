"""The 'worktoy.ezdata' module provides 'EZData'. This class is intended
to be subclassed to create data classes. Attributes must be defined in the
class body and are strongly typed. Dynamic attributes are not supported.
Setting attributes with custom descriptors is not supported. Unless a
subclass specifically implements the __init__ method an automatic
implementation of __init__ is provided. This implementation accepts
positional arguments to set attributes in the order they are defined in
the class body. Keyword arguments can also be used to set attributes by
name. In case conflict, keyword arguments take precedence over positional
arguments."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._ez_space import EZSpace
from ._ez_meta import EZMeta
from ._ez_data import EZData
