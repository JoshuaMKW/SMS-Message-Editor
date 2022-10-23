import sys
from pathlib import Path
from typing import List, Optional, Tuple

from sms_message_editor.gui.application import SMSMessageEditor
from sms_message_editor import __version__


def main(argv: Optional[list[str]] = None):
    if argv is None:
        argv = sys.argv[1:]

    app = SMSMessageEditor()

    if len(argv) == 1:
        bmgPath = Path(argv[0])
        if bmgPath.suffix.lower() == ".bmg" and bmgPath.is_file():
            app.load_bmg(bmgPath)

    app.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

#scene = SMSScene.from_bytes(open("scene.bin", "rb"))
# with open("scene_layout.log", "w", encoding="shift-jis") as f:
#    scene.dump(f)
