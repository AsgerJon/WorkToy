"""
TestFixBox tests 'FixBox' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox, FixBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import WriteOnceError, ProtectedError
from . import DescTest, Config


class TestFixBox(DescTest):
  """
  A 'FixBox' takes one value per instance and keeps it: a later write
  raises 'WriteOnceError', a deletion 'ProtectedError', and a read
  stores the default it builds, so the first read fixes the value as a
  write would. The tests pin each, the cast of the first write, the
  callback before a refused write, and the storage apart from an
  'AttriBox' at the same name.
  """

  def test_first_write_is_final(self) -> None:
    Config.attempts.clear()
    config = Config()
    config.port = 9000
    self.assertEqual(config.port, 9000)
    with self.assertRaises(WriteOnceError) as context:
      config.port = 9001
    self.assertIs(context.exception.desc, Config.__dict__['port'])
    self.assertEqual(context.exception.oldValue, 9000)
    self.assertEqual(context.exception.newValue, 9001)
    self.assertIn("'Config.port'", str(context.exception))
    self.assertIn('existing value: 9000 with new value: 9001!',
                  str(context.exception))
    self.assertEqual(config.port, 9000)
    self.assertEqual(Config.attempts, [9000, 9001])

  def test_read_fixes_the_default(self) -> None:
    config = Config()
    self.assertEqual(config.host, 'localhost')
    with self.assertRaises(WriteOnceError) as context:
      config.host = 'elsewhere'
    self.assertEqual(context.exception.oldValue, 'localhost')
    self.assertIs(context.exception.desc, Config.__dict__['host'])
    self.assertEqual(context.exception.newValue, 'elsewhere')
    self.assertIn("'Config.host'", str(context.exception))

  def test_first_write_cast(self) -> None:
    config = Config()
    config.port = 8081.0
    self.assertEqual(config.port, 8081)
    self.assertIs(type(config.port), int)

  def test_deletion_refused(self) -> None:
    config = Config()
    config.port = 1
    with self.assertRaises(ProtectedError) as context:
      del config.port
    self.assertEqual(context.exception.oldVal, 1)
    self.assertIs(context.exception.instance, config)
    self.assertIs(context.exception.desc, Config.__dict__['port'])
    self.assertIn("'Config.port'", str(context.exception))
    self.assertEqual(config.port, 1)

  def test_storage_apart_from_attribox(self) -> None:
    class Base(BaseObject):
      x = AttriBox[int](1)

    class Fixed(Base):
      x = FixBox[int](2)

    fixed = Fixed()
    self.assertEqual(fixed.x, 2)
    self.assertEqual(Base.__dict__['x'].__get__(fixed, Fixed), 1)
    self.assertEqual(Fixed.__dict__['x']._getStorageName(),
                     '__x__fixbox_field_object__')
    self.assertEqual(Base.__dict__['x']._getStorageName(),
                     '__x__attribox_field_object__')

  def test_random_first_values(self) -> None:
    for value in self.randomInteger.row:
      config = Config()
      config.port = value
      with self.subTest(value=value):
        self.assertEqual(config.port, value)
        with self.assertRaises(WriteOnceError) as context:
          config.port = value + 1
        self.assertIs(context.exception.desc, Config.__dict__['port'])
        self.assertEqual(context.exception.oldValue, value)
        self.assertEqual(context.exception.newValue, value + 1)
        self.assertIn("'Config.port'", str(context.exception))
