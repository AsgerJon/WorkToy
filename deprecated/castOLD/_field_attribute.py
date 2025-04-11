"""FieldAttribute encapsulates the attributes of a field in a class. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations


class FieldAttribute:
  """FieldAttribute encapsulates the attributes of a field in a class. """

  __field_name__ = None
  __field_class__ = None
  __default_value__ = None
  __default_factory__ = None
