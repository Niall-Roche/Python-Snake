import cx_Freeze
import sys

application_title = "Snek"

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cx_Freeze.setup(
    name = application_title,
    version = "1.0",
    description = "NO STEP ON SNEK GAME",
    options = {
        "build_exe" : {
            "include_files" : [
                "assets",
                ("DB/gameDB.db", "DB/gameDB.db")
            ],
            "packages": [
                "pygame",
                "sqlite3",
                "random",
                "logging"
            ],
            "includes": [
                "Block",
                "InputBox",
                "Button"
            ],
            "excludes": [
                'tcl',
                'ttk',
                'tkinter',
                'Tkinter'
            ]
        }
    },
    executables = [
        cx_Freeze.Executable("main.py", base = base)
    ]
)
