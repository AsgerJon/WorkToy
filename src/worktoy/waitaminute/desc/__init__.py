"""The 'worktoy.waitaminute.desc' package collects the exceptions raised
by the descriptor protocol in 'worktoy.desc' and 'worktoy.core'.

'AccessError', 'ProtectedError', 'ReadOnlyError', and 'PhantomBoxError'
share the 'DescriptorException' base, so a single
'except DescriptorException' catches all four. The first three are
'AttributeError's as well, as Python's own refusals of a read, a write and
a deletion are, so 'except AttributeError' catches them. 'WriteOnceError' (a
'TypeError'), 'WithoutException' (a 'RuntimeError'), 'MissingInstanceDict'
(a 'TypeError'), 'NamelessCallback' (a 'SyntaxError'), 'NotADescriptor' (a
'TypeError'), and 'NotAliasable', 'DanglingAlias' and 'SharedDescriptor'
(all three 'SyntaxError') are collected here too but do not inherit that
base.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ._descriptor_exception import DescriptorException
from ._access_error import AccessError
from ._protected_error import ProtectedError
from ._read_only_error import ReadOnlyError
from ._without_exception import WithoutException
from ._write_once_error import WriteOnceError
from ._phantom_box_error import PhantomBoxError
from ._missing_instance_dict import MissingInstanceDict
from ._nameless_callback import NamelessCallback
from ._not_a_descriptor import NotADescriptor
from ._not_aliasable import NotAliasable
from ._dangling_alias import DanglingAlias
from ._shared_descriptor import SharedDescriptor

__all__ = [
  'DescriptorException',
  'AccessError',
  'ReadOnlyError',
  'ProtectedError',
  'WithoutException',
  'WriteOnceError',
  'PhantomBoxError',
  'MissingInstanceDict',
  'NamelessCallback',
  'NotADescriptor',
  'NotAliasable',
  'DanglingAlias',
  'SharedDescriptor',
]
