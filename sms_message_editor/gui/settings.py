
from enum import IntEnum
from typing import Optional

from PySide6.QtCore import QSettings, QObject, QByteArray


class SMSMessageEditorSettings(QObject):
    """
    Program settings and GUI layout information
    """
    __singleton: Optional["SMSMessageEditorSettings"] = None

    class Themes(IntEnum):
        LIGHT = 0
        DARK = 1

    def __new__(cls: type["SMSMessageEditorSettings"]) -> "SMSMessageEditorSettings":
        if SMSMessageEditorSettings.__singleton is not None:
            return SMSMessageEditorSettings.__singleton
        return super(SMSMessageEditorSettings, cls).__new__(cls)

    def __init__(self, settings: Optional[QSettings] = None, parent: Optional[QObject] = None) -> None:
        if SMSMessageEditorSettings.__singleton is not None:
            return

        super().__init__(parent)
        self.load(settings)

        SMSMessageEditorSettings.__singleton = self

    @staticmethod
    def get_instance() -> "SMSMessageEditorSettings":
        if SMSMessageEditorSettings.__singleton is None:
            return SMSMessageEditorSettings()
        return SMSMessageEditorSettings.__singleton

    def is_dark_theme(self) -> bool:
        return self.settings.value("Settings/Theme", self.Themes.LIGHT) == self.Themes.DARK

    def set_theme(self, theme: Themes) -> None:
        self.settings.setValue("Settings/Theme", theme)

    def save(self) -> bool:
        from sms_message_editor.gui.application import SMSMessageEditor
        app = SMSMessageEditor.get_instance()

        if app.gui.messageMenuBar._themeAction.isChecked():
            self.set_theme(self.Themes.DARK)
        else:
            self.set_theme(self.Themes.LIGHT)
        self.settings.setValue("GUI/Geometry", app.gui.saveGeometry())
        self.settings.setValue("GUI/State", app.gui.saveState())
        self.settings.setValue("Path/OpenCwd", app.gui._cachedOpenPath)
        return True

    def load(self, settings: Optional[QSettings] = None) -> bool:
        from sms_message_editor.gui.application import SMSMessageEditor
        app = SMSMessageEditor.get_instance()

        if settings is None:
            settings = QSettings("JoshuaMK", "SMS Message Editor")
        self.settings = settings

        geometry = self.settings.value("GUI/Geometry", QByteArray(b""))
        state = self.settings.value("GUI/State", QByteArray(b""))
        app.gui._cachedOpenPath = self.settings.value("Path/OpenCwd", None)
        app.gui.restoreGeometry(geometry)
        app.gui.restoreState(state)

        app.gui.messageMenuBar._themeAction.blockSignals(True)
        app.gui.messageMenuBar._themeAction.setChecked(self.is_dark_theme())
        app.gui.messageMenuBar._themeAction.blockSignals(False)
        app.gui.signal_theme(self.is_dark_theme())

        return True

    def reset(self):
        self.settings.clear()

    def clear_settings(self):
        self.settings.remove("Settings")
