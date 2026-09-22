"""Qt UI translation loading.

The ``locale/`` directory mechanism originally only provided localized game
client language names and images. This module adds Qt UI translations
(``.qm`` files) on top of it, so an available locale can also localize the
interface text.

Two kinds of translation get installed:

- Qt's own translations, which localize built-in widget text such as the
  standard dialog buttons.
- The application's own translation, which lives next to the locale in
  ``locale/<lang_tag>/onelauncher_<lang_tag>.qm``.
"""

import logging
from pathlib import Path

from PySide6 import QtCore

from .resources import OneLauncherLocale

logger = logging.getLogger(__name__)

# Qt does not keep translators alive, so references have to be held.
_active_translators: list[QtCore.QTranslator] = []


def get_translation_file(locale: OneLauncherLocale) -> Path:
    """Return the path of the application translation file for locale."""
    return locale.data_dir / f"onelauncher_{locale.lang_tag}.qm"


def _qt_translation_files(locale: OneLauncherLocale) -> list[Path]:
    """Return the Qt translation files that match locale."""
    translations_dir = Path(
        QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.LibraryPath.TranslationsPath)
    )
    # Qt names its translation files with underscores, ex. "zh_CN".
    qt_locale_name = locale.lang_tag.replace("-", "_")
    return [
        file
        for file in (
            translations_dir / f"{prefix}_{qt_locale_name}.qm"
            for prefix in ("qtbase", "qt")
        )
        if file.exists()
    ]


def install_ui_translator(locale: OneLauncherLocale) -> bool:
    """Load and install the UI translations for locale.

    Qt's own translations are always installed when available. The application
    translation is optional, since the source language is English.

    Returns:
        bool: True if an application translation was loaded. False if the
            locale has no application translation, in which case the source
            language is used.
    """
    for translator in _active_translators:
        QtCore.QCoreApplication.removeTranslator(translator)
    _active_translators.clear()

    for file in _qt_translation_files(locale):
        translator = QtCore.QTranslator()
        if translator.load(str(file)):
            QtCore.QCoreApplication.installTranslator(translator)
            _active_translators.append(translator)
            logger.debug(
                QtCore.QCoreApplication.translate(
                    "i18n", "Installed Qt translation %s"
                ),
                file.name,
            )

    app_translation = get_translation_file(locale)
    if not app_translation.exists():
        logger.debug(
            QtCore.QCoreApplication.translate(
                "i18n", "There is no UI translation for %s"
            ),
            locale.lang_tag,
        )
        return False

    translator = QtCore.QTranslator()
    if not translator.load(str(app_translation)):
        logger.error(
            QtCore.QCoreApplication.translate(
                "i18n", "Failed to load UI translation file: %s"
            ),
            app_translation,
        )
        return False

    QtCore.QCoreApplication.installTranslator(translator)
    _active_translators.append(translator)
    logger.debug(
        QtCore.QCoreApplication.translate("i18n", "Installed UI translation for %s"),
        locale.lang_tag,
    )
    return True
