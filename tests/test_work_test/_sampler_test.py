"""
SamplerTest subclasses 'BaseTest' and provides base classes for the tests
of the 'sampler classes in the 'worktoy.work_test.samplers' module.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest
from worktoy.work_test.samplers import BaseSampler

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class SamplerTest(BaseTest):
  """
  SamplerTest provides base classes for the tests of the 'sample classes in
  the 'worktoy.work_test.samplers' module.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __item_count__: int = 32
  __col_count__: int = 8
  __row_count__: int = 4
  __tested_class__: type = BaseSampler

  @classmethod
  def rollSampler(cls, sampler: BaseSampler, ) -> tuple[Any, ...]:
    """
    This method takes a sampler instance and collects samples from the
    'item', 'row' and 'table' virtual attributes and concatenates them.

    Parameters
    ----------
    sampler : BaseSampler
      The sample instance to roll.

    Returns
    -------
    tuple[Any, ...]
      The generated samples.
    """
    sampler.rowCount = cls.__row_count__
    sampler.colCount = cls.__col_count__
    items = (*(sampler.item for _ in range(cls.__item_count__)),)
    rowItems = (*sampler.row,)
    table = []
    for row in sampler.table:
      table.extend(row)
    return (*items, *rowItems, *table)
