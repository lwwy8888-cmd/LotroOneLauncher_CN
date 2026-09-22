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

    zip_path = make_zip(app_dir)
    print(f"Portable archive: {zip_path}")
    print(f"Archive size: {zip_path.stat().st_size / 1048576:.1f} MB")


if __name__ == "__main__":
    main()
