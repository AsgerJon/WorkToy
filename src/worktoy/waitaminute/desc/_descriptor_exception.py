"""
DescriptorException is the base class for the descriptor-protocol
exceptions 'AccessError', 'ProtectedError', 'ReadOnlyError' and
'PhantomBoxError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import NoPickle


class DescriptorException(NoPickle, Exception):
  """
  Base class for the descriptor protocol exceptions 'AccessError',
  'ProtectedError', 'ReadOnlyError' and 'PhantomBoxError'; catching this
  type catches those four together. The first three are 'AttributeError's
  as well, as Python's own refusals of a read, a write and a deletion are.
  'WriteOnceError' (a 'TypeError') and
  'WithoutException' (a 'RuntimeError') are related descriptor errors
  that do NOT inherit from this class, so a bare
  'except DescriptorException' does not catch them.
  """
  pass
