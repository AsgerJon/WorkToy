"""
PromiseFamily promises the names and bases of the exceptions in
'worktoy.waitaminute'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import importlib
from unittest import TestCase

from worktoy.waitaminute import WorkToyException
from worktoy.waitaminute.desc import DescriptorException

#  Each exception, by the package it imports from, with the builtin it
#  is also an instance of.
FAMILY = {
  'worktoy.waitaminute': {
    'TypeException': TypeError,
    'UncheckableType': TypeError,
    'VariableNotNone': Exception,
    'UnpackException': ValueError,
    'SubclassException': TypeError,
    'MissingVariable': AttributeError,
  },
  'worktoy.waitaminute.desc': {
    'DescriptorException': Exception,
    'AccessError': AttributeError,
    'ReadOnlyError': AttributeError,
    'ProtectedError': AttributeError,
    'WithoutException': RuntimeError,
    'WriteOnceError': TypeError,
    'PhantomBoxError': Exception,
    'MissingInstanceDict': TypeError,
    'NamelessCallback': SyntaxError,
    'NotADescriptor': TypeError,
    'DanglingAlias': SyntaxError,
    'SharedDescriptor': SyntaxError,
    'ReferenceConflict': SyntaxError,
    'OverloadReference': SyntaxError,
    'RecursiveRead': RecursionError,
  },
  'worktoy.waitaminute.meta': {
    'DuplicateHook': Exception,
    'IllegalInstantiation': TypeError,
    'HookException': Exception,
    'DelException': SyntaxError,
    'QuestionableSyntax': SyntaxError,
    'ReservedName': SyntaxError,
    'UnboundClassHook': SyntaxError,
    'OverloadConflict': SyntaxError,
    'ReboundOverload': SyntaxError,
    'MixedMethodKind': SyntaxError,
    'ClaimedName': SyntaxError,
    'ShadowedClassHook': SyntaxError,
    'SlotsRefused': SyntaxError,
    'DuplicateSentinel': TypeError,
    'ControlClassError': TypeError,
  },
  'worktoy.waitaminute.dispatch': {
    'BareOverload': TypeError,
    'DispatchException': TypeError,
    'DuplicateSignature': TypeError,
    'TypeCastException': TypeError,
    'UnboundCastHook': SyntaxError,
  },
  'worktoy.waitaminute.keenum': {
    'KeeBoxTypeError': TypeError,
    'KeeBoxValueError': ValueError,
    'KeeBoxException': Exception,
    'KeeNameConflict': ValueError,
    'KeeCaseException': ValueError,
    'KeeDuplicate': Exception,
    'KeeFlagDuplicate': Exception,
    'KeeTypeException': TypeError,
    'KeeWriteOnceError': AttributeError,
    'KeeResolveError': Exception,
    'KeeFlagNameError': ValueError,
    'KeeMemberNameError': SyntaxError,
  },
  'worktoy.waitaminute.ezdata': {
    'DuplicateError': SyntaxError,
    'ExtraPositionalException': TypeError,
    'KwargsOnlyException': TypeError,
    'IncompleteFieldException': SyntaxError,
    'ReservedFieldError': SyntaxError,
    'ClassFieldError': SyntaxError,
    'ReservedMethodError': SyntaxError,
    'ExtraKeywordException': TypeError,
    'RepeatedFieldException': TypeError,
    'ReservedAttributeError': SyntaxError,
  },
}


class PromiseFamily(TestCase):
  """
  Every exception of worktoy lives in 'worktoy.waitaminute', in the
  subpackage named for the layer that raises it, and imports from there.
  Each is a 'WorkToyException', so one 'except WorkToyException' catches
  every exception of the library, and each is also the builtin that best
  matches its meaning, so an existing 'except TypeError' or 'except
  AttributeError' keeps catching what it caught. The refusals of a
  descriptor access, 'AccessError', 'ReadOnlyError' and 'ProtectedError'
  among them, share 'DescriptorException' as well. The control-flow
  signals are not exceptions in this sense and are no
  'WorkToyException'. Source: the docstrings of the 'waitaminute'
  package, 'WorkToyException' and 'ProtectedError', and '__all__' of
  each subpackage.
  """

  def test_every_exception(self) -> None:
    for moduleName, members in FAMILY.items():
      module = importlib.import_module(moduleName)
      for name, builtin in members.items():
        with self.subTest(name=name):
          exceptionType = getattr(module, name)
          self.assertTrue(issubclass(exceptionType, WorkToyException))
          self.assertTrue(issubclass(exceptionType, builtin))

  def test_root(self) -> None:
    self.assertTrue(issubclass(WorkToyException, Exception))

  def test_descriptor_refusals(self) -> None:
    module = importlib.import_module('worktoy.waitaminute.desc')
    for name in ('AccessError', 'ReadOnlyError', 'ProtectedError',
                 'PhantomBoxError'):
      with self.subTest(name=name):
        self.assertTrue(issubclass(getattr(module, name), DescriptorException))
