"""LogWidget contains a list of messages by order of appearance. When used
instead of print or ic from the icecream module, messages are logged
visually."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations
import time
from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PySide6.QtCore import Qt, QSize
from typing import List, Tuple, NoReturn


class LogWidget(QWidget):
  """A custom QWidget subclass for logging messages with timestamps."""

  def __init__(self):
    super().__init__()
    self.setMinimumWidth(480)
    self.logList: List[Tuple[float, str, str]] = []
    layout = QVBoxLayout()
    self.setLayout(layout)

  def tellMe(self, message: str) -> NoReturn:
    """Add a log entry with a timestamp.

    Args:
        message: The log message to be added.
    """
    timestamp = time.time()
    pretty_timestamp = datetime.fromtimestamp(timestamp).strftime(
      "%Y-%m-%d %H:%M:%S")
    log_entry = (timestamp, pretty_timestamp, message)
    self.logList.append(log_entry)
    self.updateUI()

  def updateUI(self) -> NoReturn:
    """Update the UI with the log entries."""
    layout = self.layout()

    # Clear the existing labels
    while layout.count():
      item = layout.takeAt(0)
      widget = item.widget()
      # widget.setParent()

    # Add new labels for each log entry
    for timestamp, pretty_timestamp, message in self.logList:
      log_message = f"[{pretty_timestamp}] {message}"
      label = QLabel(log_message)
      layout.addWidget(label)

    # Adjust the widget's size to fit the content
    self.adjustSize()

  def minimumSizeHint(self) -> QSize:
    """Calculate the minimum size based on the content of the log list.

    Returns:
        The minimum size hint for the widget."""
    font_metrics = self.fontMetrics()
    total_height = sum(font_metrics.height() for _, _, _ in self.logList)

    return self.layout().minimumSize() + QSize(0, total_height)


# Example usage
if __name__ == "__main__":
  import sys

  app = QApplication(sys.argv)

  loggingWidget = LogWidget()
  loggingWidget.tellMe("This is the first log entry.")
  loggingWidget.tellMe("This is the second log entry.")

  loggingWidget.show()

  sys.exit(app.exec())
