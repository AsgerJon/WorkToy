"""LMAO"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

fields = """¤¤1TAB¤¤¤¤name¤¤ = Field()"""

accList = [
  '¤¤1TAB¤¤@¤¤name¤¤.GET',
  '¤¤1TAB¤¤def get¤¤Name¤¤(self, ) -> ¤¤TYPE¤¤:',
  '¤¤2TAB¤¤\"\"\"Getter-function for ¤¤name¤¤\"\"\"',
  '¤¤2TAB¤¤return self._¤¤name¤¤',
  '¤¤blank¤¤',
  '¤¤1TAB¤¤@¤¤name¤¤.SET',
  '¤¤1TAB¤¤def set¤¤Name¤¤(self, newValue: ¤¤TYPE¤¤) -> None:',
  '¤¤2TAB¤¤\"\"\"Getter-function for ¤¤name¤¤\"\"\"',
  '¤¤2TAB¤¤self._¤¤name¤¤ = newValue',
]

pvtNames = """¤¤2TAB¤¤self._¤¤name¤¤ = None"""


def getFields(name: str, *_) -> str:
  """Creates the fields code"""
  out = fields.replace('¤¤name¤¤', name)
  out = out.replace('¤¤1TAB¤¤', '  ')
  out = out.replace('¤¤2TAB¤¤', '    ')
  return out


def getPvtNames(name: str, *_) -> str:
  """Creates private variables"""
  out = pvtNames.replace('¤¤name¤¤', name)
  out = out.replace('¤¤2TAB¤¤', '    ')
  return out


def getAccessors(name: str, cls: type) -> str:
  """Creates the accessors code"""
  Name = name[0].upper() + name[1:]
  codeLines = []
  for line in accList:
    out = line.replace('¤¤name¤¤', name)
    out = out.replace('¤¤TYPE¤¤', str(cls))
    out = out.replace('¤¤Name¤¤', Name)
    out = out.replace('¤¤1TAB¤¤', '  ')
    out = out.replace('¤¤2TAB¤¤', '    ')
    out = out.replace('¤¤blank¤¤', '\n')
    if out:
      codeLines.append(out)
  out = '\n'.join(codeLines)
  return out
#
#
# fieldCodes = []
# pvtCodes = []
# accessorList = []
# for NAME, type_ in zip(names, types):
#   fieldCodes.append(getFields(NAME, type_))
#   pvtCodes.append(getPvtNames(NAME, type_))
#   acc = getAccessors(NAME, type_)
#   accessorList.append(acc)
#
# fieldCode = '\n'.join(fieldCodes)
# pvtCode = '\n'.join(pvtCodes)
# accCode = ''.join(accessorList)
