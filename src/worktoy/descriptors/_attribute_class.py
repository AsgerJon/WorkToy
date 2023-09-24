"""WorkSide - Core - ParseCode
Code writing assistant"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.worktoyclass import WorkToyClass


class AttributeClass(WorkToyClass):
  """WorkSide - Core - ParseCode
  Code writing assistant"""

  _getterLines = [
    '<tab=1>@<name>.GET',
    '<tab=1>def get<Name>(self, ) -> <type>:',
    '<tab=2>\"\"\"Getter-function for <name>\"\"\"',
    '<tab=2>return self.<pvtName>',
  ]

  _setterLines = [
    '<tab=1>@<name>.SET',
    '<tab=1>def set<Name>(self, newValue: <type>) -> None:',
    '<tab=2>\"\"\"Setter-function for <name>\"\"\"',
    '<tab=2>self.<pvtName> = newValue',
  ]

  _illegalSetterLines = [
    '<tab=1>@<name>.SET',
    '<tab=1>def set<Name>(self, *_) -> Never:',
    '<tab=2>\"\"\"Illegal setter-function for <name>\"\"\"',
    '<tab=2>from worktoy.waitaminute import ReadOnlyException',
    '<tab=2>attName = \'<name>\'',
    '<tab=2>insName = str(self)',
    '<tab=2>clsName = self.__class__',
    '<tab=2>raise ReadOnlyException(attName, insName, clsName)',
  ]

  _illegalDeleterLines = [
    '<tab=1>@<name>.DEL',
    '<tab=1>def del<Name>(self, *_) -> Never:',
    '<tab=2>\"\"\"Illegal deleter-function for <name>\"\"\"',
    '<tab=2>from worktoy.waitaminute import ProtectedAttributeError',
    '<tab=2>attName = \'<name>\'',
    '<tab=2>insName = str(self)',
    '<tab=2>clsName = self.__class__',
    '<tab=2>raise ProtectedAttributeError(attName, insName, clsName)',
  ]

  _initLine = ['<tab=2>self.<pvtName> = <type>', ]

  _classLine = ['<tab=1><name> = Attribute()', ]

  def preAccessor(self, entry: dict, ) -> str:
    """Creates a header for the accessor functions for a particular
    attribute named 'attName'."""
    innerName = '  %s  ' % entry.get('name', )
    innerName = innerName.center(65, 'x')
    left, right = innerName.split(entry.get('name', ))[:2]
    left = left.replace('x', '<')
    right = right.replace('x', '>')
    innerName = '| %s%s%s |' % (left, entry.get('name', ), right)
    post = r'  # %s #  ' % innerName
    n = len(entry.get('name', ))
    postPost = (n * '¨').center(65, '¨')
    postPost = '  # | %s | #  ' % postPost
    return '%s\n%s' % (post, postPost)

  def postAccessor(self, entry: dict[str, str], ) -> str:
    """Creates a footer marking the end of the accessors for the named
    attribute."""
    innerName = '_'.center(65, '_')
    pre = '  # | %s | #  ' % innerName
    return pre

  def __init__(self, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)
    self._attrs = []
    self._clsName = None
    self._docstring = None
    self._parent = None

  setCls = lambda self, name: setattr(self, '_clsName', name)
  getCls = lambda self: getattr(self, '_clsName', )
  setDoc = lambda self, doc: setattr(self, '_docstring', doc)
  getDoc = lambda self: getattr(self, '_docstring')
  setParent = lambda self, parent: setattr(self, '_parent', parent)
  getParent = lambda self: getattr(self, '_parent')
  getCapName = lambda self, name: '%s%s' % (name[0].upper(), name[1:])

  def getSnakeName(self, name: str) -> str:
    """Getter-function for snake-cased dunder name."""
    snake = ['_%s' % c.lower() if c.isupper() else c for c in name]
    return '__%s__' % (''.join(snake))

  def addAttribute(self,
                   name: str,
                   defVal: str,
                   defType: str,
                   allowSetter: bool = None,
                   allowGetter: bool = None,
                   allowDeleter: bool = None) -> None:
    """Adds the named attribute with its type and default value."""
    allowSetter = self.maybe(allowSetter, True)
    allowGetter = self.maybe(allowGetter, True)
    allowDeleter = self.maybe(allowDeleter, False)
    if allowDeleter:
      raise NotImplementedError
    if not allowGetter:
      raise NotImplementedError
    self._attrs.append(
      dict(name=name,
           defVal=defVal,
           type_=defType,
           allowGetter=allowGetter,
           allowSetter=allowSetter,
           allowDeleter=False))

  def collectTags(self, entry: dict) -> dict:
    """Collects the replacement entries"""
    name = entry.get('name', )
    defVal = entry.get('defVal', )
    type_ = entry.get('type_', )
    tags = {
      '<tab=1>'  : '  ',
      '<tab=2>'  : '    ',
      '<name>'   : name,
      '<Name>'   : '%s%s' % (name[0].upper(), name[1:]),
      '<pvtName>': self.getSnakeName(name),
      '<parent>' : self.getParent(),
      '<type>'   : type_,
      '<clsName>': self.getCls(),
      '<doc>'    : self.getDoc(),
      '<defVal>' : defVal,
    }
    return tags

  def getClassTags(self) -> dict:
    """Getter-function for the tags on the class level and not related to
    each attribute."""
    return {
      '<parent>' : self.getParent(),
      '<clsName>': self.getCls(),
      '<doc>'    : self.getDoc(),
    }

  def getUniversalTags(self) -> dict:
    """Getter-function for the tags that are shared by all classes. """
    return {
      '<tab=1>': '  ',
      '<tab=2>': '    ',
      '<tab=4>': 2 * '    ',
      '<tab=8>': 4 * '    ',
    }

  def getAttributeTags(self) -> list[dict]:
    """Getter-function for the tags that are specific to each attribute."""
    return self._attrs

  def getGetterLines(self, entry: dict) -> list[str]:
    """Getter-function for the lines creating the getter function"""
    allowGetter = entry.get('allowGetter')
    if allowGetter:
      return self._getterLines
    raise NotImplementedError

  def getSetterLines(self, entry: dict) -> list[str]:
    """Getter-function for the lines creating the setter function"""
    allowSetter = entry.get('allowSetter')
    if allowSetter:
      return self._setterLines
    return self._illegalSetterLines

  def getDeleterLines(self, entry: dict) -> list[str]:
    """Getter-function for the lines creating the deleter function"""
    allowDeleter = entry.get('allowDeleter')
    if allowDeleter:
      raise NotImplementedError
    return self._illegalDeleterLines

  def collectLines(self, entry: dict) -> str:
    """Collects code creating the accessors"""
    _getters = '\n'.join(self.getGetterLines(entry))
    _deleters = '\n'.join(self.getDeleterLines(entry))
    _setters = '\n'.join(self.getSetterLines(entry))

    return '\n\n'.join([_getters, _setters, _deleters, ])

  def getAttributeAccessorCodes(self, entry: dict) -> str:
    """Getter-function for the code creating the accessors"""
    code = self.collectLines(entry)
    for key, val in self.collectTags(entry).items():
      code = code.replace(key, val)
    preCode = self.preAccessor(entry)
    postCode = self.postAccessor(entry)
    return '%s\n%s\n\n%s' % (preCode, code, postCode)

  def getAttributeInitLine(self, entry: dict) -> str:
    """Getter-function for the line in the __init__ required by this
    attribute."""
    code = '\n'.join(self._initLine)
    data = self.collectTags(entry)
    for key, val in data.items():
      code = code.replace(key, val)
    return code

  def getAttributeClassLine(self, entry: dict) -> str:
    """Getter-function for the line in the class body required by this
    attribute."""
    code = '\n'.join(self._classLine)
    data = self.collectTags(entry)
    for key, val in data.items():
      code = code.replace(key, val)
    return code

  def getClassHeader(self, ) -> str:
    """Getter-function for the class header code"""
    parent = self.getParent()
    clsName = self.getCls()
    docString = self.getDoc()
    if parent is None:
      lines = ['class <clsName>:', '<tab=1><doc>', ]
    else:
      lines = ['class <clsName>(<parent>):', '<tab=1><doc>', ]
    code = '\n'.join(lines)
    code = code.replace('<clsName>', clsName)
    code = code.replace('<doc>', docString)
    if parent is not None:
      code = code.replace('<parent>', parent)
    return code.replace('<tab=1>', '  ')

  def getInitHeader(self) -> str:
    """Getter-function for the initiator header function"""
    parent = self.getParent()
    if parent is None:
      lines = ['<tab=1>def __init__(self, *args, **kwargs) -> None:', ]
    else:
      lines = [
        '<tab=1>def __init__(self, *args, **kwargs) -> None:',
        '<tab=2><parent>.__init__(self, *args, **kwargs)'
      ]
    code = '\n'.join(lines)
    tags = {**self.getClassTags(), **self.getUniversalTags()}
    for key, val in tags.items():
      code = code.replace(key, val)
    return code

  def buildInit(self, ) -> str:
    """Builds the __init__ function"""
    codeLines = [self.getInitHeader(), ]
    for attr in self.getAttributeTags():
      codeLines.append(self.getAttributeInitLine(attr))
    return '\n'.join(codeLines)

  def buildAttributeClassBody(self) -> str:
    """Builds the start of the class body"""
    codeLines = [self.getClassHeader(), ]
    for attr in self.getAttributeTags():
      codeLines.append(self.getAttributeClassLine(attr))
    line = '  # | %s | #' % '_'.center(65, '_')
    codeLines.append(line)
    return '\n%s' % ('\n'.join(codeLines))

  def buildAccessors(self) -> str:
    """Builds the accessor functions"""
    codeLines = []
    for attr in self.getAttributeTags():
      entry = self.getAttributeAccessorCodes(attr)
      codeLines.append(entry)
    return '\n'.join(codeLines)

  def buildCode(self, **kwargs) -> str:
    """Builds the code"""
    classHead = self.buildAttributeClassBody()
    accessorFunctions = self.buildAccessors()
    initFunc = ''
    if not kwargs.get('noInit', False):
      initFunc = self.buildInit()
    return '\n'.join([classHead, accessorFunctions, initFunc])
