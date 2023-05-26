#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence

import sys
import os
import inspect
from typing import Type, Any

from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence

import os
import importlib.util


def generate_stub_files(package_dir: str) -> None:
  """Generate stub files (.pyi) for a given package directory and its
  contents recursively.

  Args:
      package_dir (str): Path to the package directory.
  """
  for dirpath, dirnames, filenames in os.walk(package_dir):
    for filename in filenames:
      if filename.endswith(".py") and not filename.startswith("__"):
        module_path = os.path.join(dirpath, filename)
        generate_stub_file(module_path)


def generate_stub_file(module_path: str) -> None:
  """Generate a stub file (.pyi) for a given Python module.

  Args:
      module_path (str): Path to the Python module (.py file).
  """
  module_name = os.path.basename(module_path)
  module_name_without_extension = os.path.splitext(module_name)[0]
  stub_file_path = f"{module_name_without_extension}.pyi"

  cuntPath = os.path.dirname(module_path)
  cuntName = '%s.pyi' % os.path.splitext(os.path.basename(module_path))[0]
  cuntPath = os.path.join(cuntPath, cuntName)

  package_dir = os.path.dirname(module_path)
  spec = importlib.util.spec_from_file_location(
    module_name_without_extension,
    module_path)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)

  stub_content = "# This is a stub file generated from the original Python " \
                 "" \
                 "" \
                 "" \
                 "" \
                 "" \
                 "" \
                 "" \
                 "module\n\n"

  for attr_name in dir(module):
    if not attr_name.startswith("__"):
      stub_content += f"{attr_name}: ...\n"

  with open(cuntPath, "w") as stub_file:
    stub_file.write(stub_content)


if __name__ == "__main__":
  # Provide the path to the directory containing the __init__.py file of
  # your package
  cunt = r'f:\cloud\worktoy\src\worktoy'
  generate_stub_files(cunt)

  app = QApplication(sys.argv)
  timer = QTimer()
  timer.setInterval(1000)
  main = QMainWindow()
  pix = QPixmap('risitas.jpg')
  label = QLabel()
  label.setFixedSize(QSize(300, 300))
  label.setPixmap(pix)
  main.setFixedSize(QSize(300, 300))
  main.setCentralWidget(label)
  timer.timeout.connect(main.close)
  if main.show() is None:
    print('lol')
    timer.start()
  sys.exit(app.exec())
