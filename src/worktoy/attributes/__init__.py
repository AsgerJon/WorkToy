"""WorkToy - Attributes
This module provides the attributes implementing descriptors. Please note
the nomenclature:
  Attribute - The class.
  Field - Instance of attribute."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._readytarget import ReadyTarget
from ._constantattribute import ConstantAttribute
from ._variableattribute import VariableAttribute
from ._strattribute import StrAttribute
