"""Field is a decorator factory setting property like fields on class from
a simple decorator. Use keyword arguments get, set, del to indicate what
accessor operations are to be allowed. The default is to allow setter and
getter, but to have deleter raise a ReadOnlyError. Users are encouraged to
subclass the Field class. This may be of particular interest if several
classes share exactly one data type whilst remaining otherwise different."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations
from ._basemeta import BaseMeta
from ._fieldmeta import FieldMeta
from ._decorators import Decorator
from ._fieldapply import FieldApply
from ._fieldenums import Perm, Name, Acc
from ._field import Field
