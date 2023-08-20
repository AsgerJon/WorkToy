"""unStupids the type hinting"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import ast
import os
from time import ctime
from typing import List


def generateProtocolsForPath(path: str):
  """
  Generate Protocol definitions for all classes defined in Python files
  at the specified path.
  """
  for root, _, files in os.walk(path):
    for file in files:
      if file.endswith(".py") and not file.startswith("I_"):
        filePath = os.path.join(root, file)
        generateProtocolsForFile(filePath)


def generateProtocolsForFile(filePath: str):
  """
  Generate Protocol definitions for all classes defined in a Python file.
  """
  with open(filePath, 'r') as file:
    tree = ast.parse(file.read())

  protocolDefinitions = []

  for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
      protocolDefinitions.append(generateProtocolForClass(node))

  saveProtocolDefinitions(filePath, protocolDefinitions)


def generateProtocolForClass(node: ast.ClassDef) -> str:
  """
  Generate a Protocol definition for a class AST node.
  """
  className = node.name

  methods = []
  for n in node.body:
    if isinstance(n, ast.FunctionDef):
      params = ", ".join(
        f"{arg.arg}: {ast.dump(arg.annotation, annotate_fields=False)}"
        for arg in n.args.args if arg.annotation is not None
      )
      returnType = ast.dump(n.returns,
                            annotate_fields=False) if n.returns else "..."
      methods.append(f"  def {n.name}({params}) -> {returnType}:\n    "
                     f"\"\"\"Method description.\"\"\"")

  methodsCode = "\n    ".join(methods)

  return f"""
class {className}(Protocol):
  \"\"\"Protocol version of the {className} class.\"\"\"
  {methodsCode}
    """


def saveProtocolDefinitions(originalFilePath: str,
                            protocolDefinitions: List[str]):
  """
  Save Protocol definitions to Python files in a 'protocols' directory.
  """
  dirPath = os.path.dirname(originalFilePath)
  protocolsDir = os.path.join(dirPath, 'protocols')

  os.makedirs(protocolsDir, exist_ok=True)

  for protocolDefinition in protocolDefinitions:
    protocolName = protocolDefinition.split('\n', 2)[0].split(' ')[1]
    protocolFilePath = os.path.join(protocolsDir, f"{protocolName}.py")

    with open(protocolFilePath, 'w') as protocolFile:
      protocolFile.write("from typing import Protocol\n\n")
      protocolFile.write(protocolDefinition)


# Usage Example:
# This will generate Protocol definitions for all classes defined in
# Python files
# in the specified directory and its subdirectories.


if __name__ == '__main__':
  scriptPath = os.path.realpath(__file__)
  scriptDir = os.path.dirname(scriptPath)

  packageDir = os.path.join(scriptDir, 'src', 'package')
  generateProtocolsForPath(packageDir)
  print(ctime())