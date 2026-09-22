import importlib.metadata

from packaging.version import Version

# Metadata has been temporarily manually entered to work with Nuitka.
# See https://github.com/Nuitka/Nuitka/issues/2965

# metadata = importlib.metadata.metadata(__package__)   # noqa: ERA001
# `__title__` is also used for the config directory name, the keyring service
# name, and the CLI/env prefix. It is intentionally left unchanged so that this
# fork keeps working with existing OneLauncher settings and saved passwords.
__title__ = "OneLauncher"
# Name shown to the user in the window title and the about window.
__display_name__ = "LotroOneLauncher_CN"
__version__ = importlib.metadata.version(__package__)
__description__ = "LOTRO 与 DDO 的启动器与插件管理器 - 简体中文版"
__project_url__ = "https://github.com/lwwy8888-cmd/LotroOneLauncher_CN"
__author__ = "June Stepp"
__author_email__ = "contact@junestepp.me"
__license__ = "GPL-3.0-or-later"
# __title__ = metadata["Name"]  # noqa: ERA001
# __version__ = metadata["Version"]  # noqa: ERA001
version_parsed = Version(__version__)
# __description__ = metadata["Summary"]  # noqa: ERA001
# # Update checks only work with a repository hosted on GitHub.
# __project_url__ = metadata.get("Home-page")  # noqa: ERA001
# __author__ = metadata.get("Author")  # noqa: ERA001
# __author_email__ = metadata.get("Author-email")  # noqa: ERA001
# __license__ = metadata.get("License")  # noqa: ERA001
__copyright__ = "(C) 2019-2026 June Stepp"
# GPL section 5a requires modified versions to carry a notice of the change.
__copyright_history__ = (
    "Simplified Chinese fork, modified from OneLauncher\n"
    "Based on PyLotRO\n(C) 2009-2010 AJackson\n"
    "Based on LotROLinux\n(C) 2007-2008 AJackson\n"
    "Based on CLI launcher for LOTRO\n(C) 2007-2010 SNy"
)
