"""The 'worktoy.waitaminute' module provides custom exception classes. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ._cast_mismatch import CastMismatch
from ._type_cast_exception import TypeCastException
from ._argument_exception import ArgumentException
from ._dispatch_exception import DispatchException
from ._num_cast_exception import NumCastException
from ._duplicate_signature_exception import DuplicateSignatureException
from ._name_mismatch_exception import NameMismatchException
from ._abstract_instantiation_exception import AbstractInstantiationException
from ._subclass_exception import SubclassException
from ._empty_box import EmptyBox
