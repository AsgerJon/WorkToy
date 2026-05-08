"""The ``worktoy.ezdata`` package — auto-generating dataclasses.

Public API:

- ``trust``: decorator marking methods as placeholders so they
  bypass the reserved-name guard.
- ``EZSlot``: per-field metadata.
- ``EZDesc``: descriptor exposing a class kwarg via ``__namespace__``.
- ``EZSpaceHook``: namespace hook collecting fields and installing
  generated dunders.
- ``EZSpace``: namespace class registered with ``EZMeta``.
- ``EZMeta``: metaclass for ``EZData``.
- ``EZData``: auto-generating dataclass base.

The field-collection helpers, coercion helpers, orderability
validator, and method generators are also exported directly so
they can be reused outside the ``EZSpaceHook`` pipeline."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._trust import trust
from ._ez_slot import EZSlot
from ._ez_desc import EZDesc

#  Field-collection helpers
from ._is_field_candidate import isFieldCandidate
from ._resolve_annotation import resolveAnnotation
from ._collect_fields import collectFields

#  Coercion helpers
from ._coerce_positional import coercePositional
from ._coerce_kwarg import coerceKwarg
from ._coerce_attr import coerceAttr

#  Orderability validation and the indexing helper
from ._validate_orderable import validateOrderable
from ._wrap_index import wrapIndex

#  Method generators
from ._make_init import makeInit
from ._make_eq import makeEq
from ._make_hash import makeHash
from ._make_repr import makeRepr
from ._make_str import makeStr
from ._make_iter import makeIter
from ._make_len import makeLen
from ._make_get_item import makeGetItem
from ._make_set_item import makeSetItem
from ._make_del_item import makeDelItem
from ._make_set_attr import makeSetAttr
from ._make_del_attr import makeDelAttr
from ._make_ordering_op import makeOrderingOp
from ._make_as_tuple import makeAsTuple
from ._make_as_dict import makeAsDict

#  Namespace plumbing and public class
from ._ez_space_hook import EZSpaceHook
from ._ez_space import EZSpace
from ._ez_meta import EZMeta
from ._ez_data import EZData

__all__ = [
  'trust',
  'EZSlot',
  'EZDesc',
  'isFieldCandidate',
  'resolveAnnotation',
  'collectFields',
  'coercePositional',
  'coerceKwarg',
  'coerceAttr',
  'validateOrderable',
  'wrapIndex',
  'makeInit',
  'makeEq',
  'makeHash',
  'makeRepr',
  'makeStr',
  'makeIter',
  'makeLen',
  'makeGetItem',
  'makeSetItem',
  'makeDelItem',
  'makeSetAttr',
  'makeDelAttr',
  'makeOrderingOp',
  'makeAsTuple',
  'makeAsDict',
  'EZSpaceHook',
  'EZSpace',
  'EZMeta',
  'EZData',
]
