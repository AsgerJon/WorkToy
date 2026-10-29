"""
AttriBox is a lazily built, strongly typed attribute descriptor.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import copyreg
from copy import deepcopy, Error
from typing import TYPE_CHECKING, TypeVar, overload

from . import _RootAlias, Field, BaseDescriptor
from ..core import Object
from ..core.sentinels import DELETED, SentinelMeta, THIS
from ..utilities import typeCast, textFmt
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.desc import MissingInstanceDict
from ..waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Union, Optional, TypeAlias

  FieldType: TypeAlias = Union[type, TypeVar]

T = TypeVar('T')


class AttriBox(BaseDescriptor[T]):
  """
  'AttriBox' is the canonical implementation of Python's descriptor
  protocol without boilerplate code in 'worktoy'. Several other such
  'boxes' are found in the library. These refer back to this documentation.

  Python provides a very powerful descriptor protocol that 'AttriBox'
  leverages to provide strongly typed attributes of Python classes. In
  addition, the objects at the attributes are lazily instantiated
  when first accessed, and cached for subsequent accesses.

  In the examples below, the function overloading implemented by
  'worktoy.dispatch' and 'worktoy.mcls' provides constructor methods.

  >>>from __future__ import annotations  # required for type hints
  >>>
  >>>from worktoy.core.sentinels import THIS
  >>>from worktoy.dispatch import overload
  >>>from worktoy.desc import AttriBox
  >>>from worktoy.mcls import BaseObject
  >>>
  >>>
  >>>class Point(BaseObject):
  >>>  #  Point in 2D space with 'float'-typed attributes
  >>>  x = AttriBox[float](0.)
  >>>  y = AttriBox[float](0.)
  >>>
  >>>  @overload(float, float)
  >>>  def __init__(self, x: float, y: float) -> None:
  >>>    self.x = x
  >>>    self.y = y
  >>>
  >>>  @overload(THIS)  # THIS meaning another 'Point' instance
  >>>  def __init__(self, other: Point) -> None:
  >>>    self.x = other.x
  >>>    self.y = other.y
  >>>
  >>>  @overload()
  >>>  def __init__(self) -> None:
  >>>    pass
  >>>
  >>>
  >>>if __name__ == '__main__':
  >>>  p0 = Point()  # Leaving the default values of 'x' and 'y' at 0.0
  >>>  p1 = Point(p0.x, p0.y)
  >>>#  Continues below with the 'Circle' class

  In the above, when 'p0.x' is accessed for the first time, it is actually
  the following call:
  >>>  x = AttriBox.__get__(Point.x, p0, Point)

  The above line covers substantial boilerplate code that users of
  'worktoy' need not write. One important note is the lazy instantiation
  which defers to first access. Below, the 'Point' instances on
  'Circle.center' are created only the moment 'Circle.center' is accessed
  or when assigned to.

  Below, the 'Circle' class continues the example above and uses its
  'Point' class:

  >>>#  Continued from the 'Point' example above
  >>>
  >>>class Circle(BaseObject):
  >>>  #  Circle in 2D space with 'Point'-typed attribute
  >>>  center = AttriBox[Point](69, 420)
  >>>  radius = AttriBox[float](1.)
  >>>
  >>>  @overload(float, float, float)
  >>>  def __init__(self, x: float, y: float, radius: float) -> None:
  >>>    self.center = Point(x, y)
  >>>    self.radius = radius
  >>>
  >>>  @overload.flex(Point, float)
  >>>  def __init__(self, center: Point, radius: float) -> None:
  >>>    self.center = center
  >>>    self.radius = radius
  >>>
  >>>  @overload(Point)  # using default radius of 1.0
  >>>  def __init__(self, center: Point) -> None:
  >>>    self.center = center
  >>>
  >>>  @overload(float)  # using default center of (69, 420)
  >>>  def __init__(self, radius: float) -> None:
  >>>    self.radius = radius
  >>>
  >>>  @overload()  # Using defaults for both center and radius
  >>>  def __init__(self) -> None:
  >>>    pass
  >>>
  >>>
  >>>if __name__ == '__main__':
  >>>  c = Circle(1.0, 2.0, 3.0)
  >>>  print(c.center.x)  # 1.0
  >>>  c.center.x = 4.0
  >>>  print(c.center.x)  # 4.0

  ##Sentinels

  Since the 'AttriBox' instances exist before their owning classes,
  the sentinel objects from 'worktoy.core.sentinels' provide placeholders.
  The most common of these is 'THIS', which is replaced by the instance of
  the owning class that is accessed through. Similarly, 'OWNER' is
  replaced by the owning class itself and 'DESC' by the descriptor itself.
  For example:

  >>>from __future__ import annotations  # required for type hints
  >>>
  >>>from worktoy.core.sentinels import THIS, OWNER, DESC
  >>>from worktoy.desc import AttriBox
  >>>
  >>>
  >>>class Wrapper:
  >>>  #  Trivial wrapping class
  >>>  __wrapped__: Optional[object] = None
  >>>
  >>>  def __init__(self, object_: object) -> None:
  >>>    self.__wrapped__ = object_
  >>>
  >>>
  >>>class Contrived:
  >>>  #  Demonstration of the sentinels THIS, OWNER and DESC
  >>>  wrapTHIS = AttriBox[Wrapper](THIS)
  >>>  wrapOWNER = AttriBox[Wrapper](OWNER)
  >>>  wrapDESC = AttriBox[Wrapper](DESC)
  >>>
  >>>
  >>>if __name__ == '__main__':
  >>>  c = Contrived()
  >>>  print(c.wrapTHIS.__wrapped__ is c)  # True
  >>>  print(c.wrapOWNER.__wrapped__ is Contrived)  # True
  >>>  print(c.wrapDESC.__wrapped__ is Contrived.wrapDESC)  # True

  ##Casting

  A field always holds an instance of its field type, so a value of
  another type is converted when nothing is lost, and refused otherwise.
  This is what lets an 'int' be assigned to a 'float' field, or 'bytes'
  to a 'str' field:

  >>>from worktoy.desc import AttriBox
  >>>
  >>>
  >>>class Measurement:
  >>>  value = AttriBox[float](0.)
  >>>  unit = AttriBox[str]('m')
  >>>
  >>>
  >>>if __name__ == '__main__':
  >>>  m = Measurement()
  >>>  m.value = 3  # the 'int' 3 is stored as the 'float' 3.0
  >>>  m.unit = b'cm'  # the 'bytes' are decoded as UTF-8 to 'cm'
  >>>  print(m.value, m.unit)  # 3.0 cm
  >>>  m.value = '3'  # raises TypeException: no string is parsed

  Every conversion goes through 'worktoy.utilities.typeCast'. The numbers
  'bool', 'int', 'float' and 'complex' convert among themselves when no
  value is lost, so 2.0 becomes the 'int' 2 but 2.5 is refused, and the
  texts 'str', 'bytes' and 'bytearray' convert among themselves as UTF-8.
  A value already of the field type is stored as it is, so a 'bool'
  assigned to an 'AttriBox[int]' stays a 'bool'. Any other class, a
  subclass of 'int' or 'str' included, accepts its own instances only,
  unless it defines the classmethod '__cast_as__', which receives the
  value and returns an instance of the class, or 'NotImplemented' to
  refuse it:

  >>>from __future__ import annotations  # required for type hints
  >>>
  >>>from worktoy.desc import AttriBox
  >>>
  >>>
  >>>class Vector:
  >>>  x = AttriBox[float](0.)
  >>>  y = AttriBox[float](0.)
  >>>
  >>>  def __init__(self, x: float = 0., y: float = 0.) -> None:
  >>>    self.x, self.y = x, y
  >>>
  >>>  @classmethod
  >>>  def __cast_as__(cls, value: object) -> Vector:
  >>>    if isinstance(value, tuple) and len(value) == 2:
  >>>      return cls(*value)
  >>>    return NotImplemented
  >>>
  >>>
  >>>class Particle:
  >>>  velocity = AttriBox[Vector]()
  >>>
  >>>
  >>>if __name__ == '__main__':
  >>>  p = Particle()
  >>>  p.velocity = (1, 2)  # cast through 'Vector.__cast_as__'
  >>>  print(p.velocity.x, p.velocity.y)  # 1.0 2.0

  No constructor is ever called on an assigned value: without
  '__cast_as__', assigning the tuple '(1, 2)' to a 'Vector' field raises
  'TypeException' rather than calling 'Vector(1, 2)'. The default is the
  other way round: the arguments in the parentheses go to the constructor
  of the field type at the first read, a lone argument included, and
  nothing is cast. So 'AttriBox[float](1)' holds 'float(1)', which is
  1.0, and 'AttriBox[int](2.5)' holds 'int(2.5)', which is 2. A lone
  argument already of the field type is copied instead; see 'Edge Cases'.

  ##Workflows

  Typed state with defaults. A class lists its fields with their types
  and defaults, and every instance starts from the defaults, with objects
  of its own:

  >>>from worktoy.desc import AttriBox
  >>>
  >>>
  >>>class Settings:
  >>>  host = AttriBox[str]('localhost')
  >>>  port = AttriBox[int](8080)
  >>>  tags = AttriBox[list](['default'])
  >>>
  >>>
  >>>if __name__ == '__main__':
  >>>  a, b = Settings(), Settings()
  >>>  a.port = 9090.0  # stored as the 'int' 9090
  >>>  a.tags.append('fast')
  >>>  print(a.port, b.port, b.tags)  # 9090 8080 ['default']

  Parts that know their whole. With 'THIS', a field builds its object
  from the instance it belongs to, at the first read, so the part can
  refer back to that instance. In Qt, for instance,
  'AttriBox[QLabel]('Hello', THIS)' builds 'QLabel('Hello', window)', a
  label with the window as its parent:

  >>>from __future__ import annotations  # required for type hints
  >>>
  >>>from worktoy.core.sentinels import THIS
  >>>from worktoy.desc import AttriBox
  >>>
  >>>
  >>>class Engine:
  >>>  def __init__(self, car: Car) -> None:
  >>>    self.car = car  # the car this engine belongs to
  >>>
  >>>
  >>>class Car:
  >>>  engine = AttriBox[Engine](THIS)
  >>>
  >>>
  >>>if __name__ == '__main__':
  >>>  one, two = Car(), Car()
  >>>  print(one.engine.car is one)  # True
  >>>  print(one.engine is two.engine)  # False

  Reacting to changes. The 'preSet' and 'onSet' decorators of a box
  register methods that run before and after each assignment. One that
  raises in 'preSet' refuses the value, and the field keeps the one it
  had:

  >>>from __future__ import annotations  # required for type hints
  >>>
  >>>from worktoy.desc import AttriBox
  >>>
  >>>
  >>>class Account:
  >>>  balance = AttriBox[float](0.)
  >>>
  >>>  @balance.preSet
  >>>  def _refuseOverdraft(self, value: float) -> None:
  >>>    if value < 0:
  >>>      raise ValueError('no overdraft')
  >>>
  >>>  @balance.onSet
  >>>  def _report(self, value: float) -> None:
  >>>    print('balance:', value)
  >>>
  >>>
  >>>if __name__ == '__main__':
  >>>  account = Account()
  >>>  account.balance = 100  # balance: 100.0
  >>>  account.balance = -5  # raises ValueError; the balance stays 100.0

  ##Edge Cases

  A single default argument already of the field type is deep-copied for
  each instance, so a mutable default is never shared, as the 'tags' of
  'Settings' above show. A value that refuses to be copied, such as a
  lock, raises 'TypeError' at the first read, since each instance cannot
  have its own; give the box the arguments of the constructor instead.

  A sentinel argument always goes to the constructor, even when the
  instance it stands for is already of the field type:

  >>>from __future__ import annotations  # required for type hints
  >>>
  >>>from worktoy.core.sentinels import THIS
  >>>from worktoy.desc import AttriBox
  >>>
  >>>
  >>>class Parent:
  >>>  def __init__(self, *args) -> None:
  >>>    self.args = args
  >>>
  >>>
  >>>class Child(Parent):
  >>>  mom = AttriBox[Parent](THIS)
  >>>
  >>>
  >>>if __name__ == '__main__':
  >>>  child = Child()
  >>>  print(child.mom is child)  # False: the field holds 'Parent(child)'

  Only the arguments themselves are replaced. A sentinel inside a
  container stays a sentinel, so 'AttriBox[list]([THIS])' holds a list
  containing 'THIS'.

  A box bound to two names in one class body gives two fields, each with
  a value of its own. One box bound in the bodies of two classes raises
  'SharedDescriptor' as the second class is created; a field several
  classes share is declared in a common base.

  >>>from worktoy.desc import AttriBox
  >>>
  >>>
  >>>class Square:
  >>>  width = height = AttriBox[int](1)
  >>>
  >>>
  >>>if __name__ == '__main__':
  >>>  print(Square.width is Square.height)  # False

  Deleting a field makes the next read raise 'MissingVariable', an
  'AttributeError', as for a deleted plain attribute, and assigning the
  field again restores it.

  The value is stored in the instance '__dict__', so a class declaring
  '__slots__' without '__dict__' is refused with 'MissingInstanceDict' as
  the class is created.

  Before Python 3.12, the refusals raised as a class is created,
  'SharedDescriptor' and 'MissingInstanceDict' among them, arrive inside
  a 'RuntimeError', which the interpreter raises for any exception from
  '__set_name__'.

  Parameters
  ----------

  Attributes
  ----------

  Raises
  ------
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_type__: Optional[type] = None

  #  Public Variables
  fieldType: Field[type] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @fieldType.GET
  def getFieldType(self) -> type:
    """
    The field type is the class in the subscript, 'int' in 'AttriBox[int]',
    and every value the attribute holds is an instance of it; 'box.fieldType'
    reads it. A 'THIS' in the subscript reads as the class whose body
    declares the box, once that class exists.

    Returns
    -------
    type
        The field type.

    Raises
    ------
    MissingVariable
        If the box was never subscripted.
    """
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
    return self.__field_type__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getStorageName(self) -> str:
    """
    An instance keeps the field object of the attribute in its own
    '__dict__' under this name, '__x__attribox_field_object__' for an
    'AttriBox' at 'x', which is what 'vars(instance)' shows. The name of
    the box class is part of it, so a 'FixBox' at the same name stores
    apart from an 'AttriBox'.

    Returns
    -------
    str
        The storage name.

    Raises
    ------
    MissingVariable
        If the box was never placed on a class, and so has no name.
    """
    if self.getFieldOwner() is None:
      raise MissingVariable(self, '__field_name__', str)
    fieldName = self.getFieldName()
    boxName = type(self).__name__.lower()
    return '__%s__%s_field_object__' % (fieldName, boxName)

  def _resolve(self, *args, **kwargs) -> T:
    """
    Makes the field object an instance receives at its first read. The
    arguments of the declaration go to the constructor of the field type,
    so 'AttriBox[int](2.5)' holds 2, and 'AttriBox[QLabel]('Hello', THIS)'
    makes a label whose parent is the instance. The one exception is a lone
    argument already of the field type: it is deep-copied, so
    'AttriBox[list]([1, 2])' gives every instance a list of its own. A
    sentinel such as 'THIS' always goes to the constructor, even when the
    instance it stands for is of the field type. Whatever the constructor
    raises reaches the read as it is.

    Parameters
    ----------
    *args : Any
        The positional arguments of the declaration, sentinels replaced.
    **kwargs : Any
        The keyword arguments of the declaration, sentinels replaced.

    Returns
    -------
    T
        The field object, an instance of the field type, tagged.

    Raises
    ------
    TypeError
        If a lone argument of the field type cannot be copied.
    TypeException
        If the constructor returns something that is not an instance of
        the field type.
    """
    if len(args) == 1 and not kwargs and not self.hasSentinelArgs():
      if isinstance(args[0], self.fieldType):
        try:
          argCopy = deepcopy(args[0])
        except (Error, TypeError, ValueError) as exception:
          infoSpec = """The default of '%s.%s' is a '%s' that cannot be
          copied, so each instance cannot have its own. Give the box the
          arguments of the '%s' constructor instead: '%s[%s](...)'."""
          typeName = self.fieldType.__name__
          info = infoSpec % (
            self.getFieldOwner().__name__, self.getFieldName(), typeName,
            typeName, type(self).__name__, typeName,
          )
          raise TypeError(textFmt(info)) from exception
        else:
          self._applyTags(argCopy)
          return argCopy
    fieldObject = self.fieldType(*args, **kwargs)
    if isinstance(fieldObject, self.fieldType):
      return self._applyTags(fieldObject)
    raise TypeException(self.getFieldName(), fieldObject, self.fieldType)

  def _applyTags(self, fieldObject: Any, ) -> T:
    """
    Writes the tags '__field_name__', '__field_owner__' and '__field_box__'
    on a field object the box made, so code holding only the object can
    tell where it belongs: the class that declares it, the name it is
    declared at and the box that made it. A field object without an
    instance '__dict__', such as an 'int' or a 'str', cannot carry them and
    is left untagged, and an assigned value is never tagged.

    Parameters
    ----------
    fieldObject : Any
        The field object the box made.

    Returns
    -------
    T
        The same field object, tagged where it can be.
    """
    if not self.fieldType.__dictoffset__:
      return fieldObject
    object.__setattr__(fieldObject, '__field_name__', self.getFieldName())
    object.__setattr__(fieldObject, '__field_owner__', self.getFieldOwner())
    object.__setattr__(fieldObject, '__field_box__', self)
    return fieldObject

  def _store(self, instance: Any, value: Any) -> None:
    """
    Stores a value for an instance under its storage name with
    'object.__setattr__', so a '__setattr__' of the owning class, one that
    guards the attributes of the class, does not stand in the way of its
    boxes.

    Parameters
    ----------
    instance : Any
        The instance to store the value for.
    value : Any
        The value to store, a field object or 'DELETED'.

    Returns
    -------
    None

    Raises
    ------
    MissingVariable
        If the box was never placed on a class.
    MissingInstanceDict
        If the instance has no '__dict__' to store in.
    """
    pvtName: str = self._getStorageName()
    try:
      object.__setattr__(instance, pvtName, value)
    except AttributeError as attributeError:
      if self.getFieldOwner() is None:
        raise MissingVariable(
          self,
          '__field_name__',
          str
          ) from attributeError
      fieldName = self.getFieldName()
      raise MissingInstanceDict(instance, fieldName) from attributeError

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> T:
    """
    Reading the attribute through an instance gives the field object that
    instance holds. It is made at the first read, from the arguments of the
    declaration, and kept, so every later read gives the very same object.
    Nothing is made before that read, which is why a field type that needs
    a running application, such as a Qt widget, may be declared in a class
    body at import. Deleting an attribute never read makes nothing either.

    Parameters
    ----------
    instance : Any
        The instance the attribute is read through.
    owner : type
        The class of the instance.
    **kwargs : Any
        '_deleting=True' when 'Object.__delete__' asks for the value it is
        about to delete, which reads what is stored and makes nothing.

    Returns
    -------
    T
        The field object of the instance.
    """
    pvtName = self._getStorageName()
    try:
      value = object.__getattribute__(instance, pvtName)
    except AttributeError as attributeError:
      if kwargs.get('_deleting', False):
        raise attributeError
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      args = self.getPosArgs()
      kwargs = self.getKeyArgs()
      fieldObject = self._resolve(*args, **kwargs)
      self._store(instance, fieldObject)
      return self.__instance_get__(instance, owner, _recursion=True)
    else:
      return value

  def _cast(self, value: Any) -> T:
    """
    Converts an assigned value that is not of the field type, as 'typeCast'
    allows: numbers among numbers and texts among texts, without loss, or
    through a '__cast_as__' classmethod of the field type, which is how a
    class of a project accepts values of other types.

    Parameters
    ----------
    value : Any
        The assigned value.

    Returns
    -------
    T
        The value converted to the field type.

    Raises
    ------
    TypeException
        If 'typeCast' refuses the value, naming the attribute.
    """
    fieldType = self.getFieldType()
    try:
      return typeCast(fieldType, value)
    except TypeCastException as typeCastException:
      fieldName = self.getFieldName()
      raise TypeException(fieldName, value, fieldType) from typeCastException

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> T:
    """
    Assigning to the attribute stores a value of the field type as it is
    and converts any other through '_cast', so on an 'AttriBox[float]'
    'm.value = 3' stores 3.0 and 'm.value = "3"' raises 'TypeException'.
    No constructor runs on an assigned value: for a 'Vector' attribute to
    accept a tuple, 'Vector' declares '__cast_as__'. The 'onSet' callbacks
    receive the value as stored, the converted one.

    Parameters
    ----------
    instance : Any
        The instance the attribute is assigned through.
    value : Any
        The assigned value.
    **kwargs : Any
        '_recursion=True' on the second pass, after the conversion.

    Returns
    -------
    T
        The value stored, an instance of the field type.

    Raises
    ------
    TypeException
        If the value is not of the field type and '_cast' refuses it.
    """
    if isinstance(value, self.fieldType):
      self._store(instance, value)
      return value
    if kwargs.get('_recursion', False):
      raise RecursionError
    cast = self._cast(value)
    return self.__instance_set__(instance, cast, _recursion=True)

  def __instance_delete__(self, instance: Any, *_, **kwargs) -> None:
    """
    'del obj.x' deletes the attribute for that instance: the next read
    raises 'MissingVariable', an 'AttributeError', as for a deleted plain
    attribute, a second 'del' raises it too, and the next assignment brings
    the attribute back.

    Parameters
    ----------
    instance : Any
        The instance the attribute is deleted from.
    *_ : Any
        The value being deleted, which 'Object.__delete__' passes and the
        box does not need.
    **kwargs : Any
        Keyword arguments of the descriptor protocol, unused.

    Returns
    -------
    None
    """
    self._store(instance, DELETED)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # @formatter:off
  @overload
  def __get__(self, instance: None, owner: type) -> Self: ...
  @overload
  def __get__(self, instance: Any, owner: type) -> T: ...
  # @formatter:on

  def __get__(self, instance: Any, owner: type) -> Union[Self, T]:
    """
    Read through the class, as 'Point.x', a box gives itself, so it can be
    inspected or have callbacks registered on it; read through an instance
    it gives the field object. A box set on a class after the class was
    created, with 'setattr' rather than in the class body, never learned
    its name or was never subscripted, and its first read raises
    'MissingVariable'.

    Parameters
    ----------
    instance : Any
        The instance the attribute is read through, or None when read
        through the class.
    owner : type
        The class the attribute is read through.

    Returns
    -------
    Union[Self, T]
        The box itself through the class, the field object through an
        instance.

    Raises
    ------
    MissingVariable
        If the box reached its first read without a field type or a name.
    """
    if instance is not None:
      if self.__field_type__ is None:
        raise MissingVariable(self, '__field_type__', type)
    return super().__get__(instance, owner)

  def __copy__(self) -> Self:
    """
    'copy.copy' of a box gives the box itself; see '__deepcopy__'.

    Returns
    -------
    Self
        The box itself.
    """
    return self

  def __deepcopy__(self, memo: dict) -> Self:
    """
    'copy.deepcopy' of a box gives the box itself. That is what makes deep
    copies of instances with boxed attributes work: a field object names
    its box in the '__field_box__' tag, so copying the object, or the
    instance holding it, reaches the box, and a copy of the box would be a
    descriptor on no class. The copied field object keeps naming the box
    its class declares, as the original does. A separate box is made by
    subscripting and calling the box class again.

    Parameters
    ----------
    memo : dict
        The memo of the 'copy.deepcopy' call, unused.

    Returns
    -------
    Self
        The box itself.
    """
    return self

  def __reduce__(self) -> tuple:
    """
    A box placed on a class pickles as a reference to the class and the
    name it is declared at, so 'pickle' gives back the very box the class
    declares, and an unpickled field object, whose '__field_box__' tag
    names the box, finds that box. This is what lets an instance with boxed
    attributes, tags included, survive 'pickle', as long as its class can
    be imported. A box not yet placed on a class pickles by its state.

    Returns
    -------
    tuple
        'getattr' with the class and the name for a placed box, else the
        default reconstruction from the state of the box.
    """
    owner, name = self.__field_owner__, self.__field_name__
    if owner is None or name is None:
      #  The default protocol, spelled out: 'object.__reduce_ex__' would
      #  call back into this method.
      return copyreg.__newobj__, (type(self),), self.__dict__
    return getattr, (owner, name)

  @classmethod
  def __class_getitem__(cls, fieldType: FieldType) -> Self:
    """
    The subscript fixes the field type, the class every value of the
    attribute is an instance of, and gives a new box of the class
    subscripted, so 'FixBox[int]' gives a 'FixBox'. 'THIS' as the field
    type stands for the class whose body declares the box, so a 'Node' may
    hold a 'Node'. Only a plain class can be a field type: a 'TypeVar' goes
    to 'typing', so 'class Sub(AttriBox[T])' declares a generic subclass,
    and such an alias, or a generic such as 'list[int]', bound in a class
    body raises 'PhantomBoxError' as the class is created.

    Parameters
    ----------
    fieldType : type or TypeVar
        The field type fixed by the subscript.

    Returns
    -------
    Self
        A new box of the class subscripted, carrying 'fieldType'.

    Raises
    ------
    TypeException
        If 'fieldType' is not a 'type' or 'TypeVar'.
    TypeError
        If 'fieldType' is a sentinel other than 'THIS', such as 'OWNER'.
    """
    if isinstance(fieldType, SentinelMeta) and fieldType is not THIS:
      infoSpec = """The subscript '%s[%s]' names a sentinel as the field
      type. A sentinel stands for a meaning, such as the enclosing class,
      and is no type of value a field could hold; the field type is the
      class of the values the field holds."""
      info = infoSpec % (cls.__name__, fieldType.__name__)
      raise TypeError(textFmt(info))
    #  'isinstance(fieldType, type)' reads '__class__', which a builtin
    #  parametrized generic such as 'list[int]' forwards to its origin on
    #  Python 3.9 and 3.10, answering 'True'. The type of the subscript is
    #  a metaclass exactly when the subscript is a plain class, on every
    #  version, without an attribute lookup a class-level hook could answer.
    if issubclass(type(fieldType), type) or fieldType is THIS:
      self = object.__new__(cls)
      self.__field_type__ = fieldType
      return self  # noqa
    try:
      out = super().__class_getitem__(fieldType)
    except Exception as exception:
      name, value = 'fieldType', fieldType
      raise TypeException(name, value, type, TypeVar) from exception
    else:
      return _RootAlias.fromAlias(out)

  def __call__(self: Any, *args, **kwargs) -> Self:
    """
    The parentheses of 'center = AttriBox[Point](1, 2)' hold the arguments
    for the constructor of the field type. They are kept until an instance
    first reads the attribute, and 'Point(1, 2)' is called for it then;
    nothing is made at the class-body line. 'THIS', 'OWNER' and 'DESC'
    among them stand for the instance, its class and the box. Leaving the
    call off, as in 'AttriBox[int]', is the same as empty parentheses.

    Parameters
    ----------
    *args : Any
        The positional arguments for the constructor of the field type.
    **kwargs : Any
        The keyword arguments for the constructor of the field type.

    Returns
    -------
    Self
        'self', so the call site can chain straight into a class-body
        assignment, for example 'x = AttriBox[int](42)'.

    Raises
    ------
    TypeError
        If the box is already placed on a class, as when called again
        through it, 'Holder.n(5)'.
    """
    if self.__field_owner__ is not None:
      infoSpec = """The box at '%s.%s' took the arguments of its default as
      its class was created, and cannot take new ones."""
      ownerName = self.__field_owner__.__name__
      info = infoSpec % (ownerName, self.__field_name__)
      raise TypeError(textFmt(info))
    Object.__init__(self, *args, **kwargs)
    return self

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    Runs as the class holding the box is created, and is where a wrong
    declaration is refused on the class statement instead of at some later
    read: a box never subscripted, as 'AttriBox()', and a box on a class
    whose instances have no '__dict__', a class declaring '__slots__'
    without one, since the box keeps the field object there. It is also
    where 'THIS' as the field type becomes the class. One box bound to two
    names, as 'width = height = AttriBox[int](0)', gives two attributes,
    and one box bound in the bodies of two classes raises
    'SharedDescriptor'; see 'BaseDescriptor.__set_name__'. How Python before
    3.12 reports these refusals is told at 'Object.__set_name__'.

    Parameters
    ----------
    owner : type
        The class being created that holds the box.
    name : str
        The name the box is bound to in the class body.
    **kwargs : Any
        Passed on to 'BaseDescriptor.__set_name__'.

    Returns
    -------
    None

    Raises
    ------
    MissingVariable
        If the box was never subscripted.
    MissingInstanceDict
        If the instances of 'owner' have no '__dict__'.
    SharedDescriptor
        If the box is already placed on another class.
    """
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
    #  Zero exactly when instances of 'owner' have no '__dict__'.
    if not type.__getattribute__(owner, '__dictoffset__'):
      raise MissingInstanceDict(owner, name)
    if self.__field_type__ is THIS:
      self.__field_type__ = owner
    if self.__pos_args__ is None:
      BaseDescriptor.__init__(self)
    super().__set_name__(owner, name, **kwargs)
