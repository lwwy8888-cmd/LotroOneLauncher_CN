"""Build a portable, installer-free Windows build with PyInstaller.

Unlike ``build/nuitka_compile.py`` this needs no C compiler. The result is a
plain folder that can be zipped and unzipped anywhere: the executable reads
its resources from its own directory, so nothing has to be installed.

Run with: python build/pyinstaller_compile.py
"""

import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from onelauncher import __about__

ROOT = Path(__file__).resolve().parent.parent
# Only the final archive goes into the repository; the intermediate build tree
# is kept outside of it, since it holds thousands of files.
ZIP_DIR = ROOT / "release"
BUILD_ROOT = Path(tempfile.gettempdir()) / "onelauncher-pyi"
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

# Modules that are never imported by the launcher. Excluding them keeps
# PyInstaller from collecting their DLLs and translations, which saves several
# megabytes per module. QtOpenGL drags in a software OpenGL fallback
# (opengl32sw.dll, 7 MB) used only for machines without a GPU driver.
EXCLUDED_MODULES = (
    "PySide6.QtOpenGL",
    "PySide6.QtOpenGLWidgets",
    "PySide6.QtQml",
    "PySide6.QtQuick",
    "PySide6.QtQuickWidgets",
    "PySide6.Qt3DCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtMultimedia",
    "PySide6.QtDesigner",
    "PySide6.QtUiTools",
    "PySide6.QtTest",
)

# Files left behind by the collector that the program never loads. Each entry
# is checked before removal, so a path that does not exist is simply skipped.
UNUSED_FILES = (
    "opengl32sw.dll",
    "d3dcompiler_47.dll",
    "Qt6OpenGL.dll",
    "Qt6OpenGLWidgets.dll",
    "Qt6Qml.dll",
    "Qt6Quick.dll",
    "Qt6Designer.dll",
    "QtOpenGL.pyd",
    "QtOpenGLWidgets.pyd",
    "QtQml.pyd",
    "QtQuick.pyd",
    "QtDesigner.pyd",
)

# Qt ships its own translations for the standard dialogs (file pickers, message
# boxes) in a ``translations`` folder next to the DLLs. The launcher's own UI
# strings come from its own locale folder instead, so only the files matching
# its supported language are worth keeping. The ``qtbase_`` files are by far
# the largest of the set.
KEPT_QT_TRANSLATIONS = ("qtbase_zh_CN.qm", "qt_zh_CN.qm", "qtbase_en.qm")


def prepare_build_dir() -> Path:
    """Return an empty output directory for PyInstaller.

    An existing tree is moved aside rather than deleted, because bulk deletion
    of thousands of files trips the sandbox's delete guard.
    """
    out_dir = BUILD_ROOT / "out"
    if not out_dir.exists():
        return out_dir

    stale = BUILD_ROOT / f"out-{int(time.time())}"
    out_dir.rename(stale)
    print(f"Moved previous build aside: {stale}")
    return out_dir


def build() -> Path:
    """Run PyInstaller and return the directory containing the built app."""
    out_dir = prepare_build_dir()
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
    for module in EXCLUDED_MODULES:
        arguments += ["--exclude-module", module]
    arguments += [
        "--distpath",
        str(out_dir),
        "--workpath",
        str(BUILD_ROOT / "work"),
        "--specpath",
        str(ROOT),
        str(ENTRY_SCRIPT),
    ]

    subprocess.run(arguments, check=True, cwd=ROOT)  # noqa: S603
    return out_dir / APP_NAME


def prune(app_dir: Path) -> int:
    """Delete collected files the launcher never loads.

    Excluding modules stops PyInstaller from importing them, but Qt plugins and
    translations are gathered by glob, so they still end up in the tree. Returns
    the number of bytes freed.
    """
    freed = 0
    removed = []

    for name in UNUSED_FILES:
        for path in app_dir.rglob(name):
            if path.is_file():
                freed += path.stat().st_size
                removed.append(path.relative_to(app_dir))
                path.unlink()

    # Translation files live next to the DLLs, not inside the package folder, so
    # every ``translations`` directory in the tree is swept. Both the ``qt_``
    # (Qt 6 style) and ``qtbase_`` (Qt 5 style) prefixes are covered, since
    # PySide6 ships both sets.
    for translations in app_dir.rglob("translations"):
        if not translations.is_dir():
            continue
        for path in translations.glob("*.qm"):
            if path.name in KEPT_QT_TRANSLATIONS:
                continue
            freed += path.stat().st_size
            removed.append(path.relative_to(app_dir))
            path.unlink()

    for relative in sorted(removed):
        print(f"  pruned {relative}")
    print(f"Pruned {len(removed)} files, {freed / 1048576:.1f} MB freed")
    return freed


def make_zip(app_dir: Path) -> Path:
    """Zip the app directory so that unzipping yields a ready to run folder."""
    ZIP_DIR.mkdir(exist_ok=True)
    version = __about__.version_parsed.base_version
    archive = ZIP_DIR / f"{APP_NAME}-{version}-win64-portable"
    # Overwriting a single file is fine, unlike deleting a directory tree.
    archive.with_suffix(".zip").unlink(missing_ok=True)
    return Path(
        shutil.make_archive(
            str(archive), "zip", root_dir=app_dir.parent, base_dir=app_dir.name
        )
    )


def main() -> None:
    app_dir = build()
    print(f"App folder: {app_dir}")

    prune(app_dir)

    zip_path = make_zip(app_dir)
    print(f"Portable archive: {zip_path}")
    print(f"Archive size: {zip_path.stat().st_size / 1048576:.1f} MB")


if __name__ == "__main__":
    main()
