"""The primitives module provides orphan utility classes and functions.
These do not rely on importing from any packages other than the builtin
ones. This means that these cannot raise custom exceptions, but instead
raises builtin ones. Other modules using them must implement custom
exceptions as appropriate."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


from ._maybe import maybe, onlyIf, maybeFirstIf, maybeAllIf, maybeType
from ._maybe import maybeTypes, empty, some, plenty