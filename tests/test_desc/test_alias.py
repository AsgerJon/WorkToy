"""
TestAlias tests the 'Alias' class from the 'worktoy.desc' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Object
from worktoy.core.sentinels import DELETED
from worktoy.desc import Alias, Field


class NameTag(Object):
  """NameTag is a simple class with a name attribute. """

  __fallback_name__ = 'NameTag'
  __inner_name__ = None
  name = Field()

  def __init__(self, name: str) -> None:
    self.name = name

  @name.GET
  def _getName(self) -> str:
    """Get the name of the NameTag."""
    return self.__inner_name__

  @name.SET
  def _setName(self, value: str) -> None:
    """Set the name of the NameTag."""
    self.__inner_name__ = value

  @name.DELETE
  def _delName(self) -> None:
    """Delete the name of the NameTag."""
    self.__inner_name__ = DELETED

  def __str__(self) -> str:
    """Return the string representation of the NameTag."""
    infoSpec = """%s(%s)"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.name)
    return info

  __repr__ = __str__


class MusicDisc(NameTag):
  """MusicDisc is a subclass of NameTag with a specific name. """

  title = Alias('name')  # Reuses the 'name' but under attribute 'title'


class TestAlias(TestCase):
  """TestAlias tests the Alias class."""

  @classmethod
  def tearDownClass(cls) -> None:
    """Clean up the test class."""
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_alias(self) -> None:
    """Test the Alias class."""
    disc = MusicDisc('Bohemian Rhapsody')
    self.assertEqual(disc.name, 'Bohemian Rhapsody')
    self.assertEqual(disc.title, 'Bohemian Rhapsody')

    disc.title = 'Another One Bites the Dust'
    self.assertEqual(disc.name, 'Another One Bites the Dust')
    self.assertEqual(disc.title, 'Another One Bites the Dust')

    disc.name = 'We Will Rock You'
    self.assertEqual(disc.name, 'We Will Rock You')
    self.assertEqual(disc.title, 'We Will Rock You')

    self.assertEqual(str(disc), repr(disc))

  def test_alias_deletion(self) -> None:
    """Test deleting the alias attributes. Some music titles should be
    deleted."""

    disc = MusicDisc('This is how you remind me')

    del disc.name  # Get that outta here!

    self.assertIs(object.__getattribute__(disc, '__inner_name__'), DELETED)

    with self.assertRaises(AttributeError):
      _ = disc.name
    with self.assertRaises(AttributeError):
      del disc.name
    with self.assertRaises(AttributeError):
      _ = disc.title
    with self.assertRaises(AttributeError):
      del disc.title
