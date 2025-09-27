"""The 'tests.test_desc' module provides tests for the 'worktoy.desc'
module."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._complex_fields import ComplexFields
from ._complex_fields_subclass import ComplexFieldsSubclass
from ._complex_box import ComplexBox
from ._complex_label import ComplexLabel
from ._complex_alias import ComplexAlias
from ._boxed_float import BoxedFloat
from ._boxed_object import BoxedObject
from ._box_owner import BoxOwner
from ._desc_test import DescTest

__all__ = [
    'ComplexFields',
    'ComplexFieldsSubclass',
    'ComplexBox',
    'ComplexLabel',
    'ComplexAlias',
    'BoxedFloat',
    'BoxedObject',
    'BoxOwner',
    'DescTest',
]
