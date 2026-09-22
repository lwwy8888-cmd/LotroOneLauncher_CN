"""Build a portable, installer-free Windows build with PyInstaller.

Unlike ``build/nuitka_compile.py`` this needs no C compiler. The result is a
plain folder that can be zipped and unzipped anywhere: the executable reads
its resources from its own directory, so nothing has to be installed.

Run with: python build/pyinstaller_compile.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

from onelauncher import __about__

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "release"
WORK_DIR = ROOT / "build" / "pyi-work"
ENTRY_SCRIPT = ROOT / "build" / "pyinstaller_entry.py"

APP_NAME = __about__.__display_name__

# Source directory -> destination inside the app folder. These paths are
# relative to the application directory, exactly as the program expects them.
DATA_DIRS = (
    ("src/onelauncher/locale", "locale"),
    ("src/onelauncher/images", "images"),
    ("src/onelauncher/external", "external"),
    ("src/onelauncher/schemas", "schemas"),
    ("src/onelauncher/network/schemas", "network/schemas"),
    ("src/onelauncher/addons/schemas", "addons/schemas"),
)


def build() -> Path:
    """Run PyInstaller and return the directory containing the built app."""
    arguments = [
        sys.executable or "python",
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        # Resources are located through the executable's own directory, so the
        # contents must not be moved into the default "_internal" subfolder.
        "--contents-directory",
        ".",
        "--name",
        APP_NAME,
        "--icon",
        "src/onelauncher/images/OneLauncherIcon.ico",
        "--paths",
        "src",
        # __about__ reads its version through importlib.metadata.
        "--copy-metadata",
        __about__.__package__,
        "--hidden-import",
        "keyring.backends.Windows",
    ]
    for source, destination in DATA_DIRS:
        arguments += ["--add-data", f"{source};{destination}"]
    arguments += [
        "--distpath",
        str(OUT_DIR),
        "--workpath",
        str(WORK_DIR),
        "--specpath",
        str(ROOT),
        str(ENTRY_SCRIPT),
    ]

    subprocess.run(arguments, check=True, cwd=ROOT)  # noqa: S603
    return OUT_DIR / APP_NAME


def make_zip(app_dir: Path) -> Path:
    """Zip the app directory so that unzipping yields a ready to run folder."""
    version = __about__.version_parsed.base_version
    archive = OUT_DIR / f"{APP_NAME}-{version}-win64-portable"
    zip_path = Path(
        shutil.make_archive(
            str(archive), "zip", root_dir=app_dir.parent, base_dir=app_dir.name
        )
    )
    return zip_path


def main() -> None:
    app_dir = build()
    print(f"App folder: {app_dir}")

    zip_path = make_zip(app_dir)
    print(f"Portable archive: {zip_path}")
    print(f"Archive size: {zip_path.stat().st_size / 1048576:.1f} MB")


if __name__ == "__main__":
    main()
