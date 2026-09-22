"""Entry point used by the PyInstaller build.

``src/onelauncher/__main__.py`` uses relative imports, so it cannot be used as
a PyInstaller entry script directly. Importing the package here keeps it a
normal module run, which is also what the ``onelauncher`` console script does.
"""

from onelauncher.__main__ import main

if __name__ == "__main__":
    main()
