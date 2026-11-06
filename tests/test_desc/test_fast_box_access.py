"""
TestFastBoxAccess tests the reads, writes and deletions of a 'FastBox'
from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import FastBox
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import MissingInstanceDict
from . import DescTest, Particle


class TestFastBoxAccess(DescTest):
  """
  A read of a 'FastBox' is one lookup, a write one check and one store
  with no cast, and a deletion lets the next read start over. The tests
  pin the shared value and the value per instance, the strict write,
  the deletion, the refusals for an instance without a dictionary and
  for a box never placed, which come ahead of the type check, and the
  value a factory must produce.
  """

  def test_read_builds_once(self) -> None:
    particle = Particle()
    self.assertEqual(particle.mass, 1.0)
    self.assertIs(type(particle.mass), float)
    self.assertIn('__fast_mass__', particle.__dict__)
    self.assertIs(particle.tags, particle.tags)
    self.assertEqual(particle.tags, [])
    self.assertIsNot(particle.tags, Particle().tags)
    self.assertEqual(particle.name, 'particle')
    self.assertIsInstance(Particle.mass, FastBox)

  def test_write_checks_type_without_cast(self) -> None:
    particle = Particle()
    particle.mass = 2.5
    self.assertEqual(particle.mass, 2.5)
    with self.assertRaises(TypeException) as context:
      particle.mass = 2
    self.assertEqual(context.exception.varName, 'mass')
    self.assertEqual(context.exception.actualObject, 2)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (float,))
    self.assertIn("'mass'", str(context.exception))
    self.assertEqual(particle.mass, 2.5)
    with self.assertRaises(TypeException) as context:
      particle.name = b'bytes'
    self.assertEqual(context.exception.varName, 'name')
    self.assertEqual(context.exception.actualObject, b'bytes')
    self.assertIs(context.exception.actualType, bytes)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'name'", str(context.exception))

  def test_delete_starts_over(self) -> None:
    particle = Particle()
    particle.mass = 3.0
    del particle.mass
    self.assertEqual(particle.mass, 1.0)
    del particle.mass
    with self.assertRaises(MissingVariable) as context:
      del particle.mass
    self.assertEqual(context.exception.varName, 'mass')
    self.assertIs(context.exception.instance, particle)
    self.assertEqual(context.exception.expectedTypes, ())
    self.assertEqual(str(context.exception), "Missing 'Particle.mass'!")

  def test_instance_without_dict(self) -> None:
    class Slotted:
      __slots__ = ()

    box = Particle.__dict__['mass']
    slotted = Slotted()
    with self.assertRaises(MissingInstanceDict) as context:
      box.__get__(slotted, Slotted)
    self.assertIs(context.exception.instance, slotted)
    self.assertEqual(context.exception.fieldName, 'mass')
    self.assertEqual(context.exception.ownerName, 'Slotted')
    self.assertIn("'Slotted.mass'", str(context.exception))
    with self.assertRaises(MissingInstanceDict) as context:
      box.__set__(slotted, 2.0)
    self.assertIs(context.exception.instance, slotted)
    self.assertEqual(context.exception.fieldName, 'mass')
    self.assertEqual(context.exception.ownerName, 'Slotted')
    #  A wrong value changes nothing: no value could be stored, so the
    #  dictionary is refused before the value is looked at.
    with self.assertRaises(MissingInstanceDict) as context:
      box.__set__(slotted, 'two')
    self.assertIs(context.exception.instance, slotted)
    self.assertEqual(context.exception.fieldName, 'mass')
    with self.assertRaises(MissingInstanceDict) as context:
      box.__delete__(slotted)
    self.assertIs(context.exception.instance, slotted)
    self.assertEqual(context.exception.fieldName, 'mass')
    self.assertIn("'Slotted.mass'", str(context.exception))

  def test_box_never_placed(self) -> None:
    class Plain:
      pass

    box = FastBox[int](1)
    plain = Plain()
    with self.assertRaises(MissingVariable) as context:
      box.__get__(plain, Plain)
    self.assertEqual(context.exception.varName, '__field_name__')
    self.assertIs(context.exception.instance, box)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertEqual(
      str(context.exception),
      "Missing 'FastBox.__field_name__: str'!"
      )
    with self.assertRaises(MissingVariable) as context:
      box.__set__(plain, 2)
    self.assertEqual(context.exception.varName, '__field_name__')
    self.assertIs(context.exception.instance, box)
    #  A wrong value through a box without a name is refused for the
    #  name, never as a type error naming the field 'None'.
    with self.assertRaises(MissingVariable) as context:
      box.__set__(plain, 'two')
    self.assertEqual(context.exception.varName, '__field_name__')
    self.assertIs(context.exception.instance, box)
    with self.assertRaises(MissingVariable) as context:
      box.__delete__(plain)
    self.assertEqual(context.exception.varName, '__field_name__')
    self.assertIs(context.exception.instance, box)
    self.assertIs(box.__get__(None, Plain), box)

  def test_build(self) -> None:
    class Weird:
      def __new__(cls) -> int:
        return 5

    class Owner:
      w = FastBox[Weird]()

    with self.assertRaises(TypeException) as context:
      _ = Owner().w
    self.assertEqual(context.exception.varName, 'w')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (Weird,))
    self.assertIn("'Weird'", str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      FastBox.__new__(FastBox)._build()
    self.assertEqual(context.exception.varName, '__field_type__')
    self.assertEqual(context.exception.expectedTypes, (type,))
    self.assertIn("'FastBox.__field_type__: type'", str(context.exception))
    self.assertEqual(Particle.__dict__['mass']._build(), 1.0)
    self.assertEqual(Particle.__dict__['tags']._build(), [])

  def test_random_writes(self) -> None:
    particle = Particle()
    for value in self.randomFloat.row:
      particle.mass = value
      with self.subTest(value=value):
        self.assertEqual(particle.mass, value)
