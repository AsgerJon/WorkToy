"""
SimpleComplex is a 'ComplexMixin' adding nothing of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test import ComplexMixin


class SimpleComplex(ComplexMixin):
  """
  The bank runs against implementations of 'ComplexMixin', and the
  plainest implementation is a subclass adding nothing: it keeps its
  parts where the mixin keeps them and takes the whole arithmetic from
  it. 'SimpleComplex' is that implementation, the target the bank of
  this folder runs against and the class the tests of the mixin use.
  """
