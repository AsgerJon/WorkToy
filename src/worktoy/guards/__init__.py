"""WorkToy - Guards
This package provides guards that raises predefined errors in certain
circumstances."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_guard import AbstractGuard
from ._none_guard import NoneGuard
from ._some_guard import SomeGuard
from ._type_guard import TypeGuard
