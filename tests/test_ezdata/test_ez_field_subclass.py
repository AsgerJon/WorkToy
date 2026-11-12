"""
TestEZFieldSubclass tests a subclass of 'EZField' from 'worktoy.ezdata'
that takes options of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField, fields
from worktoy.waitaminute.ezdata import IncompleteFieldException
from . import EzdataTest


class TestEZFieldSubclass(EzdataTest):
  """
  A project that wants a field to carry more than a type and a default,
  a line about the field say, subclasses 'EZField': the parentheses of
  'Described[int](...)' reach the '__init__' of the subclass, which
  keeps what is its own and hands the arguments of the default on to
  'EZField.__init__'. A clone, which is what a subclass of the dataclass
  and a second name in one body hold, is of the same class and keeps
  what the field holds. The tests pin the call, a dataclass of such
  fields, both clones, the clone taken by hand, and the refusal of a
  field class whose '__init__' hands nothing on.
  """

  @staticmethod
  def makeFamily() -> tuple:
    """A field class carrying a line about the field, and a dataclass."""

    class Described(EZField):
      def __init__(self, *args, about: str = '', **kwargs) -> None:
        EZField.__init__(self, *args, **kwargs)
        self.about = about

    class Config(EZData):
      host = Described[str]('localhost', about='The host to listen on')
      port = Described[int](8080, about='The port to listen on')

    return Described, Config

  def test_parentheses_reach_the_init(self) -> None:
    Described, _ = self.makeFamily()
    field = Described[int](8080, about='The port to listen on')
    self.assertIs(type(field), Described)
    self.assertIs(field.fieldType, int)
    self.assertEqual(field.posArgs, (8080,))
    self.assertEqual(field.keyArgs, {})
    self.assertEqual(field.about, 'The port to listen on')
    self.assertEqual(field.defaultValue, 8080)
    self.assertIs(field(9090), field)
    self.assertEqual(field.posArgs, (9090,))
    self.assertEqual(field.about, '')

  def test_dataclass_of_such_fields(self) -> None:
    Described, Config = self.makeFamily()
    self.assertEqual(Config().asTuple(), ('localhost', 8080))
    config = Config('example.org', port=443)
    self.assertEqual(config.asDict(), dict(host='example.org', port=443))
    self.assertEqual(config.replace(port=80).port, 80)
    for field in fields(Config):
      with self.subTest(field=field.fieldName):
        self.assertIs(type(field), Described)
        self.assertIs(field.fieldOwner, Config)
        self.assertEqual(field.keyArgs, {})
    self.assertEqual([field.about for field in fields(Config)],
                     ['The host to listen on', 'The port to listen on'])

  def test_inherited_field_keeps_class_and_options(self) -> None:
    Described, Config = self.makeFamily()

    class Server(Config):
      workers = Described[int](4, about='The worker processes')

    inherited = Server.__ez_fields__['port']
    original = Config.__ez_fields__['port']
    self.assertIsNot(inherited, original)
    self.assertIs(type(inherited), Described)
    self.assertEqual(inherited.about, 'The port to listen on')
    self.assertEqual(inherited.fieldName, 'port')
    self.assertIs(inherited.fieldOwner, Server)
    self.assertIs(original.fieldOwner, Config)
    self.assertEqual(Server().asTuple(), ('localhost', 8080, 4))

  def test_second_name_keeps_class_and_options(self) -> None:
    Described, _ = self.makeFamily()

    class Range(EZData):
      low = Described[int](0, about='A bound of the range')
      high = low

    first, second = fields(Range)
    self.assertIsNot(second, first)
    self.assertIs(type(second), Described)
    self.assertEqual(second.about, 'A bound of the range')
    self.assertEqual(first.fieldName, 'low')
    self.assertEqual(second.fieldName, 'high')
    self.assertEqual(Range(1, 9).asDict(), dict(low=1, high=9))

  def test_clone_holds_what_the_field_holds(self) -> None:
    Described, Config = self.makeFamily()
    bound = Config.__ez_fields__['port']
    #  Put on the field after its class took it, so that it stands
    #  behind the name and the owner among what the field holds.
    bound.reviewed = True
    self.assertEqual([*vars(bound)][-3:],
                     ['__field_name__', '__field_owner__', 'reviewed'])
    held = dict(
      __field_type__=int,
      __pos_args__=(8080,),
      __key_args__={},
      about='The port to listen on',
      reviewed=True,
    )
    for clone in (bound.clone(), Described.clone_(bound)):
      with self.subTest(clone=repr(clone)):
        self.assertIsNot(clone, bound)
        self.assertIs(type(clone), Described)
        self.assertEqual(vars(clone), held)
    plain = EZField.clone_(bound)
    self.assertIs(type(plain), EZField)
    self.assertEqual(vars(plain), held)
    self.assertEqual(bound.fieldName, 'port')
    self.assertIs(bound.fieldOwner, Config)

  def test_clone_asks_no_init(self) -> None:
    class Measured(EZField):
      def __init__(self, *args, unit: str, **kwargs) -> None:
        EZField.__init__(self, *args, **kwargs)
        self.unit = unit

    class Rod(EZData):
      length = Measured[float](1.0, unit='m')

    class Beam(Rod):
      load = Measured[float](0.0, unit='N')

    self.assertEqual([field.unit for field in fields(Beam)], ['m', 'N'])
    self.assertEqual(Beam(2).asTuple(), (2.0, 0.0))

  def test_init_handing_nothing_on_is_refused(self) -> None:
    class Deaf(EZField):
      def __init__(self, *args, **kwargs) -> None:
        self.heard = (args, kwargs)

    self.assertEqual(Deaf[int](8080).heard, ((8080,), {}))
    with self.assertRaises(IncompleteFieldException) as context:
      class Config(EZData):
        port = Deaf[int](8080)

    exception = context.exception
    self.assertEqual(exception.clsName, 'Config')
    self.assertEqual(exception.fieldName, 'port')
    self.assertEqual(exception.missing, "no construction arguments were "
                     "given, or the '__init__' of 'Deaf' did not hand them "
                     "on to 'EZField.__init__'")
    self.assertEqual(str(exception), "EZData subclass 'Config' has "
                     "incomplete field 'port': no construction arguments "
                     "were given, or the '__init__' of 'Deaf' did not hand "
                     "them on to 'EZField.__init__'. Use 'EZField[T](...)' "
                     "to declare both the type and the construction "
                     "arguments.")
