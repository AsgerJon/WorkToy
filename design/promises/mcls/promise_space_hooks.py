"""
PromiseSpaceHooks promises the namespace hooks a project writes, from
'worktoy.mcls.space_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject, BaseMeta, BaseSpace
from worktoy.mcls.space_hooks import AbstractSpaceHook


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
  checks keep running beside it.

  From 1.3.0 the order of the hooks is promised as well. The hooks of the
  base namespace classes run first, 'reservedNameHook', 'nameHook' and
  'loadSpaceHook' for a 'BaseSpace', then those the namespace class
  declares itself, in the order declared. Every phase calls them in that
  order, and the first hook claiming a binding ends the round, so the
  hooks after it never see the binding; 'loadSpaceHook' claims every
  '@overload' record. 'classGetHooks', a classmethod of the namespace
  class, gives the hooks in the order they run, and a namespace class
  reimplementing it runs its hooks in the order it gives, which is how a
  hook of a project runs ahead of an inherited one. Source: the
  docstrings of 'AbstractSpaceHook', 'AbstractNamespace' and 'BaseMeta',
  and section 6 of the mcls part of 'design/manual.md'.
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
    with self.assertRaises(Exception):
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

  def test_hook_order(self) -> None:
    class First(AbstractSpaceHook):
      pass

    class Second(AbstractSpaceHook):
      pass

    class OrderSpace(BaseSpace):
      first = First()
      second = Second()

    names = [hook.getFieldName() for hook in OrderSpace.classGetHooks()]
    self.assertEqual(names, [
      'reservedNameHook', 'nameHook', 'loadSpaceHook', 'first', 'second',
    ])

  def test_claim_hides_from_later_hooks(self) -> None:
    seen = []

    class Claim(AbstractSpaceHook):
      def setItemPhase(self, key, value, old=None) -> bool:
        return True if key == 'secret' else False

    class Watch(AbstractSpaceHook):
      def setItemPhase(self, key, value, old=None) -> bool:
        seen.append(key)
        return False

    class WatchSpace(BaseSpace):
      claim = Claim()
      watch = Watch()

    class WatchMeta(BaseMeta):
      @classmethod
      def __prepare__(mcls, name, bases, **kwargs) -> WatchSpace:
        return WatchSpace(mcls, name, bases, **kwargs)

    class Vault(BaseObject, metaclass=WatchMeta):
      secret = 42
      shown = 1

      @overload(int)
      def twice(self, value: int) -> int:
        return 2 * value

    self.assertIn('shown', seen)
    self.assertNotIn('secret', seen)
    self.assertNotIn('twice', seen)
    self.assertEqual(Vault().twice(3), 6)

  def test_reorder_by_class_get_hooks(self) -> None:
    seen = []

    class Watch(AbstractSpaceHook):
      def setItemPhase(self, key, value, old=None) -> bool:
        seen.append(key)
        return False

    class EarlySpace(BaseSpace):
      watch = Watch()

      @classmethod
      def classGetHooks(cls) -> list:
        own = cls.watch
        hooks = [h for h in super().classGetHooks() if h is not own]
        at = hooks.index(BaseSpace.loadSpaceHook)
        return [*hooks[:at], own, *hooks[at:]]

    class EarlyMeta(BaseMeta):
      @classmethod
      def __prepare__(mcls, name, bases, **kwargs) -> EarlySpace:
        return EarlySpace(mcls, name, bases, **kwargs)

    names = [hook.getFieldName() for hook in EarlySpace.classGetHooks()]
    self.assertEqual(names, [
      'reservedNameHook', 'nameHook', 'watch', 'loadSpaceHook',
    ])

    class Early(BaseObject, metaclass=EarlyMeta):
      @overload(int)
      def twice(self, value: int) -> int:
        return 2 * value

    self.assertIn('twice', seen)
    self.assertEqual(Early().twice(4), 8)
