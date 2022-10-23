import sys
import webbrowser
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QSize, Slot, Signal
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from sms_message_editor import __version__, VariadicArgs, VariadicKwargs
from sms_message_editor.gui.images import get_icon
from sms_message_editor.gui.settings import SMSMessageEditorSettings
from sms_message_editor.gui.window import BMGMessageEditorWindow
from sms_message_editor.filesystem import get_program_folder, resource_path


class SMSMessageEditor(QApplication):
    """
    Junior's Toolbox Application
    """
    __singleton: Optional["SMSMessageEditor"] = None

    def __new__(cls, *args: VariadicArgs, **kwargs: VariadicKwargs) -> "SMSMessageEditor":
        if SMSMessageEditor.__singleton is not None:
            return SMSMessageEditor.__singleton
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        if SMSMessageEditor.__singleton is not None:
            return

        super().__init__()

        SMSMessageEditor.__singleton = self

        # Force Windows Taskbar Icon
        if sys.platform in {"win32", "cygwin", "msys"}:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                self.get_window_title()
            )

        self.gui = BMGMessageEditorWindow()

        self.gui.setWindowTitle(self.get_window_title())
        self.gui.setWindowIcon(get_icon("program.png"))
        self.update_theme(BMGMessageEditorWindow.Theme.LIGHT)

        self.gui.messageMenuBar.themeChangeRequested.connect(self.update_theme)
        self.gui.messageMenuBar.issueRequested.connect(self.open_issue_page)

        self.gui.themeChanged.connect(self.update_theme)

        # # Set up file dialogs
        # self.gui.messageMenuBar.actionNew.triggered.connect(
        #     lambda _: self.reset()
        # )  # throw away checked flag
        # self.gui.actionClose.triggered.connect(
        #     lambda _: self.reset()
        # )  # throw away checked flag
        # self.gui.actionOpen.triggered.connect(
        #     lambda _: self.open_scene()
        # )  # throw away checked flag
        # self.gui.actionSave.triggered.connect(
        #     lambda _: self.save_scene(self.scenePath)
        # )  # throw away checked flag
        # self.gui.actionSaveAs.triggered.connect(
        #     lambda _: self.save_scene()
        # )  # throw away checked flag
        # self.gui.actionReportBug.triggered.connect(
        #     lambda _: self.open_issue_page()
        # )

        # Set up theme toggle

        fontFolder = resource_path("gui/fonts/")
        for fontFile in fontFolder.iterdir():
            if not fontFile.is_file():
                continue
            QFontDatabase.addApplicationFont(str(fontFile))

        self.settings = SMSMessageEditorSettings()
        self.settings.load()

    # --- GETTER / SETTER --- #

    @staticmethod
    def get_instance() -> "SMSMessageEditor":
        if SMSMessageEditor.__singleton is None:
            return SMSMessageEditor()
        return SMSMessageEditor.__singleton

    # --- GUI --- #

    @staticmethod
    def get_config_path():
        versionStub = __version__.replace(".", "-")
        return get_program_folder(f"{__name__} v{versionStub}") / "program.cfg"

    @staticmethod
    def get_window_title():
        return f"SMS Message Editor v{__version__}"

    def update_theme(self, theme: "BMGMessageEditorWindow.Theme"):
        """
        Update the UI theme to the specified theme
        """
        #from qdarkstyle import load_stylesheet, load
        from sms_message_editor.gui.qdarktheme import load_stylesheet, load_palette
        if theme == BMGMessageEditorWindow.Theme.LIGHT:
            self.theme = BMGMessageEditorWindow.Theme.LIGHT
            self.setStyleSheet(load_stylesheet("light"))
        else:
            self.theme = BMGMessageEditorWindow.Theme.DARK
            self.setStyleSheet(load_stylesheet("dark"))

    def show(self):
        """
        Show the GUI
        """
        self.gui.show()

    @Slot()
    def open_issue_page(self):
        webbrowser.open(
            "https://github.com/JoshuaMKW/SMS-Message-Editor/issues/new?assignees=JoshuaMKW&labels=bug&template=bug_report.md&title=%5BBUG%5D+Short+Description",
            new=0,
            autoraise=True
        )
