"""
TestEZHash test that immutable EZData classes allow for hashing
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData
from worktoy.waitaminute.ez import FrozenEZException, UnfrozenHashException

if TYPE_CHECKING:  # pragma: no cover
  pass

from . import EZTest


class RGB(EZData, frozen=True):
  """
  RGB is an immutable EZData class representing a color in RGB format.
  It is used to test the hashing functionality of EZData classes.
  """

  R = 0
  G = 0
  B = 0


class TestEZHash(EZTest):
  """
  TestEZHash tests that immutable EZData classes allow for hashing.
  """

  def test_good_get(self) -> None:
    """
    Test that the RGB class can be hashed and compared correctly.
    """
    red = RGB(255, 0, 0, )
    green = RGB(0, 255, 0, )
    blue = RGB(0, 0, 255, )

    self.assertIsInstance(red, RGB)
    self.assertIsInstance(green, RGB)
    self.assertIsInstance(blue, RGB)

    self.assertEqual(red.R, 255)
    self.assertEqual(red.G, 0)
    self.assertEqual(red.B, 0)
    self.assertEqual(green.R, 0)
    self.assertEqual(green.G, 255)
    self.assertEqual(green.B, 0)
    self.assertEqual(blue.R, 0)
    self.assertEqual(blue.G, 0)
    self.assertEqual(blue.B, 255)

  def test_bad_get(self) -> None:
    """
    Test that the RGB class raises an error when trying to set attributes.
    """
    red = RGB(255, 0, 0, )
    with self.assertRaises(FrozenEZException) as context:
      red.R = 100  # type: ignore[assignment]
    e = context.exception
    self.assertEqual(e.fieldName, 'R')
    self.assertEqual(e.className, 'RGB')
    self.assertEqual(e.oldValue, 255)
    self.assertEqual(e.newValue, 100)
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(FrozenEZException) as context:
      red.R = 100
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.fieldName, 'R')
    self.assertEqual(e.className, 'RGB')
    self.assertEqual(e.oldValue, 255)
    self.assertEqual(e.newValue, 100)

    with self.assertRaises(FrozenEZException) as context:
      red.G = 100
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.fieldName, 'G')
    self.assertEqual(e.className, 'RGB')
    self.assertEqual(e.oldValue, 0)
    self.assertEqual(e.newValue, 100)
    with self.assertRaises(FrozenEZException) as context:
      red.B = 100
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.fieldName, 'B')
    self.assertEqual(e.className, 'RGB')
    self.assertEqual(e.oldValue, 0)
    self.assertEqual(e.newValue, 100)

  def test_hash(self) -> None:
    """Tests hashing of RGB instances by creating a 'dict' object with RGB
    instances as keys. """

    farve = {
        RGB(255, 0, 0): 'Rød',
        RGB(0, 255, 0): 'Grøn',
        RGB(0, 0, 255): 'Blå',
    }
    color = {
        RGB(255, 0, 0): 'Rouge',
        RGB(0, 255, 0): 'Vert',
        RGB(0, 0, 255): 'Bleu',
    }

    keys = [RGB(255, 0, 0), RGB(0, 255, 0), RGB(0, 0, 255)]
    #  Despite being different instances, the keys should have same hash
    #  values.
    navne = ['Rød', 'Grøn', 'Blå']
    noms = ['Rouge', 'Vert', 'Bleu']

    for key, navn, nom in zip(keys, navne, noms):
      self.assertEqual(farve[key], navn)
      self.assertEqual(color[key], nom)

  def test_iterable(self) -> None:
    """Tests that RGB instances can be iterated over."""
    values = (255, 0, 144)
    pink = RGB(*values, )
    for v, p in zip(values, pink):
      self.assertEqual(v, p)

  def test_len(self) -> None:
    """Testing the length of the base class."""
    self.assertEqual(len(RGB), 3)

  def test_iter(self) -> None:
    """Testing the iterator of the base class."""
    for char, slot in zip('RGB', RGB):
      self.assertEqual(char, slot)

  def test_contains(self) -> None:
    """Testing the 'in' operator on the base class."""
    self.assertIn('R', RGB)
    self.assertIn('G', RGB)
    self.assertIn('B', RGB)
    self.assertNotIn('A', RGB)
    self.assertNotIn('C', RGB)
    self.assertNotIn('D', RGB)

  def test_init_fewer_args(self) -> None:
    """Testing the RGB class with fewer arguments."""
    rgb = RGB(255, 0)
    self.assertEqual(rgb.R, 255)
    self.assertEqual(rgb.G, 0)
    self.assertEqual(rgb.B, 0)

    rgb = RGB(0, 255)
    self.assertEqual(rgb.R, 0)
    self.assertEqual(rgb.G, 255)
    self.assertEqual(rgb.B, 0)

    rgb = RGB(0, 0, 255)
    self.assertEqual(rgb.R, 0)
    self.assertEqual(rgb.G, 0)
    self.assertEqual(rgb.B, 255)

  def test_init_fewer_kwargs(self) -> None:
    """Testing the RGB class with fewer keyword arguments."""
    rgb = RGB(R=255, G=0)
    self.assertEqual(rgb.R, 255)
    self.assertEqual(rgb.G, 0)
    self.assertEqual(rgb.B, 0)

    rgb = RGB(G=255, B=0)
    self.assertEqual(rgb.R, 0)
    self.assertEqual(rgb.G, 255)
    self.assertEqual(rgb.B, 0)

    rgb = RGB(B=255, R=0)
    self.assertEqual(rgb.R, 0)
    self.assertEqual(rgb.G, 0)
    self.assertEqual(rgb.B, 255)

  def test_init_mix_args_kwargs(self) -> None:
    """Testing the RGB class with a mix of positional and keyword
    arguments."""
    rgb = RGB(255, G=0, B=0)
    self.assertEqual(rgb.R, 255)
    self.assertEqual(rgb.G, 0)
    self.assertEqual(rgb.B, 0)

    rgb = RGB(255, 0, B=0)
    self.assertEqual(rgb.R, 255)
    self.assertEqual(rgb.G, 0)
    self.assertEqual(rgb.B, 0)

    rgb = RGB(R=0, G=0, B=255)
    self.assertEqual(rgb.R, 0)
    self.assertEqual(rgb.G, 0)
    self.assertEqual(rgb.B, 255)

  def test_bad_hash(self) -> None:
    """Testing that the RGB class raises an error when trying to hash
    it."""

    class BadRGB(EZData, frozen=False):
      """
      BadRGB is a mutable EZData class that should not be hashable.
      It is used to test the hashing functionality of EZData classes.
      """
      R = 0
      G = 0
      B = 0

    with self.assertRaises(UnfrozenHashException) as context:
      _ = {
          BadRGB(255, 0, 0): 'Rot',
          BadRGB(0, 255, 0): 'Grün',
          BadRGB(0, 0, 255): 'Blau',
      }
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.className, 'BadRGB')
