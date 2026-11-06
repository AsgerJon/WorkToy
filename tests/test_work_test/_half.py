"""
Half is a sampler declaring its value type and not its recipe.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.work_test.samplers import BaseSampler


class Half(BaseSampler):
  """
  'SamplerMeta' promises to refuse a sampler that leaves one of the two
  hooks abstract when it is built, not at its first row. 'Half' declares
  the value type and not the recipe, so building one is the refusal the
  tests pin.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getValueType(self, **kwargs) -> type:
    return int
