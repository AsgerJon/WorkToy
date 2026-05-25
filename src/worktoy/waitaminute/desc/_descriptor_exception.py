"""
DescriptorException is the base class for the descriptor protocol
exceptions 'AccessError', 'ProtectedError', and 'ReadOnlyError',
grouping them under one type so they can be caught together. The
related 'WriteOnceError' and 'WithoutException' do not inherit from it.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  pass


class DescriptorException(Exception):
  """
  Base class for the descriptor protocol exceptions 'AccessError',
  'ProtectedError', and 'ReadOnlyError'; catching this type catches
  those three together. 'WriteOnceError' (a 'TypeError') and
  'WithoutException' (a 'RuntimeError') are related descriptor errors
  that do NOT inherit from this class, so a bare
  'except DescriptorException' does not catch them.
  """
  pass
