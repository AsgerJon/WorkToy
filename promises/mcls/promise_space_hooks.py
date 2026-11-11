"""
PromiseSpaceHooks promises the namespace hooks a project writes, from
'worktoy.mcls.space_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import BaseObject, BaseMeta, BaseSpace
from worktoy.mcls.space_hooks import AbstractSpaceHook
from worktoy.waitaminute.meta import QuestionableSyntax


class PromiseSpaceHooks(TestCase):
  """
  A project screens or transforms the bodies of its classes with a hook
  of its own: a subclass of 'AbstractSpaceHook' reimplementing the
  phases it needs, declared in the body of a 'BaseSpace' subclass, which
  a metaclass based on 'BaseMeta' returns from '__prepare__'. Before
  each binding of the body, 'setItemPhase(key, value, old)' runs; raising
  there refuses the binding at its line, and returning True claims it,
  so the class does not receive the name. Inside a phase 'self.space' is
  the namespace of the class statement. The hook screens the class that
  declares the metaclass as well as its subclasses, and worktoy's own
  checks keep running beside it. Source: the docstrings of
  'AbstractSpaceHook', 'AbstractNamespace' and 'BaseMeta'.
  """

  def test_refuse(self) -> None:
    class NoSingleUnderscore(AbstractSpaceHook):
      def setItemPhase(self, key, value, old=None) -> bool:
        if key.startswith('_') and not key.startswith('__'):
          raise NameError(key)
        return False

    class StrictSpace(BaseSpace):
      noSingleUnderscore = NoSingleUnderscore()

    class StrictMeta(BaseMeta):
      @classmethod
      def __prepare__(mcls, name, bases, **kwargs) -> StrictSpace:
        return StrictSpace(mcls, name, bases, **kwargs)

    class Strict(BaseObject, metaclass=StrictMeta):
      shown = 1

    self.assertEqual(Strict.shown, 1)
    with self.assertRaises(NameError):
      class Hidden(Strict):
        _hidden = 1
    with self.assertRaises(NameError):
      class Declaring(BaseObject, metaclass=StrictMeta):
        _hidden = 1
    with self.assertRaises(QuestionableSyntax):
      class Misspelled(Strict):
        def __setname__(self, owner, name) -> None:
          pass

  def test_claim(self) -> None:
    claimed = []

    class Collect(AbstractSpaceHook):
      def setItemPhase(self, key, value, old=None) -> bool:
        if key == 'secret':
          claimed.append((self.space.getClassName(), value))
          return True
        return False

    class CollectSpace(BaseSpace):
      collect = Collect()

    class CollectMeta(BaseMeta):
      @classmethod
      def __prepare__(mcls, name, bases, **kwargs) -> CollectSpace:
        return CollectSpace(mcls, name, bases, **kwargs)

    class Vault(BaseObject, metaclass=CollectMeta):
      secret = 42

    self.assertFalse(hasattr(Vault, 'secret'))
    self.assertEqual(claimed, [('Vault', 42)])
