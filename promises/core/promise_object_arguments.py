"""
PromiseObjectArguments promises the kept arguments and names of an
'Object' from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Object
from worktoy.core.sentinels import THIS, OWNER, DESC
from worktoy.waitaminute import MissingVariable


class PromiseObjectArguments(TestCase):
  """
  An 'Object' keeps the arguments it was created with, and
  'getPosArgs' and 'getKeyArgs' give them back. During an access, an
  argument that is 'THIS' becomes the instance and one that is 'OWNER'
  the owner; outside an access the two stay themselves. 'DESC' always
  becomes the descriptor. Only an argument that is a placeholder itself
  is replaced, not one inside a container. 'hasSentinelArgs' tells
  whether any argument is a placeholder. 'getPrivateName' turns the
  field name 'fooBar' into '__foo_bar__', and raises 'MissingVariable'
  for a descriptor no class holds. The mapping is not one to one:
  'foo_bar' gives '__foo_bar__' as well, and 'dict' gives the '__dict__'
  Python uses itself. Source: the 'Object' docstring and
  the docstrings of 'getContextualSentinels', 'filterSentinels',
  'hasSentinelArgs' and 'getPrivateName'.
  """

  def test_arguments_kept(self) -> None:
    class Plain(Object):
      pass

    plain = Plain(1, 'two', key=3)
    self.assertEqual(plain.getPosArgs(), (1, 'two'))
    self.assertEqual(plain.getKeyArgs(), {'key': 3})
    self.assertFalse(plain.hasSentinelArgs())

  def test_placeholders_during_access(self) -> None:
    class Echo(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        return self.getPosArgs(), self.getKeyArgs()

    class Holder:
      echo = Echo(THIS, [THIS], owner=OWNER, desc=DESC)

    holder = Holder()
    posArgs, keyArgs = holder.echo
    self.assertIs(posArgs[0], holder)
    self.assertEqual(posArgs[1], [THIS])
    self.assertIs(keyArgs['owner'], Holder)
    self.assertIs(keyArgs['desc'], vars(Holder)['echo'])

  def test_placeholders_outside_access(self) -> None:
    class Plain(Object):
      pass

    plain = Plain(THIS, OWNER, DESC)
    self.assertEqual(plain.getPosArgs(), (THIS, OWNER, plain))
    self.assertTrue(plain.hasSentinelArgs())

  def test_private_name(self) -> None:
    class Plain(Object):
      pass

    class Holder:
      fooBar = Plain()

    self.assertEqual(vars(Holder)['fooBar'].getPrivateName(), '__foo_bar__')

  def test_private_name_not_one_to_one(self) -> None:
    class Plain(Object):
      pass

    class Holder:
      foo_bar = Plain()
      dict = Plain()

    self.assertEqual(vars(Holder)['foo_bar'].getPrivateName(), '__foo_bar__')
    self.assertEqual(vars(Holder)['dict'].getPrivateName(), '__dict__')

  def test_private_name_unplaced(self) -> None:
    class Plain(Object):
      pass

    plain = Plain()
    with self.assertRaises(MissingVariable) as context:
      plain.getPrivateName()
    e = context.exception
    self.assertIs(e.instance, plain)
    self.assertEqual(e.varName, '__field_name__')
    self.assertEqual(e.expectedTypes, (str,))
