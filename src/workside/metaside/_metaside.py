"""The MetaSide exposes the metaclass used by the PySide6 classes"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QMainWindow

ShibokenObject = type(QObject)


class MetaSide(ShibokenObject):
  """Subclassing the metaclass used by QWidget"""

  def __new__(mcls,
              name: str,
              bases: tuple[type],
              namespace: dict,
              **kwargs) -> None:
    return ShibokenObject.__new__(mcls, name, bases, namespace, **kwargs)

  def __init__(cls,
               name: str,
               bases: tuple[type],
               namespace: dict,
               **kwargs) -> None:
    ShibokenObject.__init__(cls, name, bases, namespace, **kwargs)


class BaseObject(QObject, MetaSide):
  """In between subclass of QObject with exposed metaclass"""
  pass


class BaseWidget(QWidget, MetaSide):
  """In between subclass of QWidget with exposed metaclass"""
  pass


class BaseWindow(QMainWindow, MetaSide):
  """In between subclass of QMainWindow with exposed metaclass"""
  pass
