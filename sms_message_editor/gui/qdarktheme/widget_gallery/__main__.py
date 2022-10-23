"""Module allowing for `python -m qdarktheme.widget_gallery`."""
import sys

from sms_message_editor.gui.qdarktheme import load_stylesheet
from sms_message_editor.gui.qdarktheme.qtpy.QtCore import Qt
from sms_message_editor.gui.qdarktheme.qtpy.QtWidgets import QApplication
from sms_message_editor.gui.qdarktheme.widget_gallery.BMGMessageEditorWindow import WidgetGallery

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):  # Enable High DPI display with Qt5
        # type: ignore
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    win = WidgetGallery()
    win.menuBar().setNativeMenuBar(False)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    win.show()
    app.exec()
