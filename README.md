# [OneLauncher](https://Github.com/JuneStepp/OneLauncher) 简体中文版

[English](README.en.md)

> 本仓库是 OneLauncher 的**简体中文分支**，在原版基础上汉化了界面并做了少量调整，依据 GPLv3+ 许可发布。
> 原项目版权归 June Stepp 所有，修改声明见文末[「关于本分支」](#关于本分支)。

![OneLauncher window examples](https://i.imgur.com/UtCIHSl.png)

[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/lwwy8888-cmd/LotroOneLauncher_CN?include_prereleases)](https://github.com/lwwy8888-cmd/LotroOneLauncher_CN/releases/latest) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

一个为 [LOTRO（指环王 Online）](https://www.lotro.com/) 和 [DDO（龙与地下城 Online）](https://www.ddo.com/) 打造的功能增强启动器，内置插件、皮肤与音乐资源管理器。

## 功能

- 多账号支持
- 保存密码
- 插件、皮肤与音乐管理器
- 插件外部脚本支持
- Linux 与 macOS 下自动配置 WINE
- 多客户端支持
- *以及更多*

## 安装

本分支提供 **Windows 64 位免安装版**：下载压缩包，解压后直接运行 `LotroOneLauncher_CN.exe` 即可，无需安装程序。

- [直接下载 2.1.3 免安装包](https://github.com/lwwy8888-cmd/LotroOneLauncher_CN/releases/latest/download/LotroOneLauncher_CN-2.1.3-win64-portable.zip)
- [全部发布版](https://github.com/lwwy8888-cmd/LotroOneLauncher_CN/releases)
- [系统要求](#系统要求)
- [从源码运行](CONTRIBUTING.md#development-install)
- [上游原版（英文，含 macOS 与 Linux 版）](https://github.com/JuneStepp/OneLauncher/releases/latest)

### macOS（上游原版，本分支未提供）

- 下载最新发布版：
    - [arm64（Apple Silicon）](http://github.com/JuneStepp/OneLauncher/releases/latest/download/OneLauncher-macOS-ARM64.zip)
    - [x86_64（Intel）](http://github.com/JuneStepp/OneLauncher/releases/latest/download/OneLauncher-macOS-x86_64.zip)
- 双击 `OneLauncher-macOS-*.zip` 文件解压。
- 如果需要，把解压出的 `OneLauncher` 拖进「应用程序」文件夹。
- 双击 `OneLauncher` 即可打开。
- 如果出现「OneLauncher 无法打开，因为它来自未识别的开发者」之类的提示，请进入「系统设置」的「隐私与安全性」部分，那里会有允许打开 OneLauncher 的选项。

祝你冒险愉快！注意第一次进入游戏时可能会有卡顿，这是正常现象，很快就会消失。

### 系统要求

#### Windows

需要 Windows 10（1809 或更高版本）或 Windows 11，这是 [Qt6 支持的版本范围](https://doc.qt.io/qt-6/windows.html)。

#### Linux

大多数人只需要[安装 WINE](https://github.com/lutris/docs/blob/master/WineDependencies.md#distribution-specific-instructions) 即可。如果之后遇到问题，再检查其余要求。

- WINE 的依赖项，参见[这些命令](https://github.com/lutris/docs/blob/master/WineDependencies.md#distribution-specific-instructions)。
- [Qt 支持的 OS 版本](https://doc.qt.io/qt-6/linux.html#supported-configurations)
- 如果使用 X11，需要 `libxcb-cursor0` 或 `xcb-cursor0`。
- `libz`
- 一个 Secret Service 后端，例如 Gnome Keyring 或 KWallet

## 命令行用法

所有设置都可以从命令行覆盖，这对创建自定义快捷方式尤其有用。例如，用法语启动 LOTRO 预览客户端可以这样写：`--game lotro-preview --locale fr`。

```txt
Usage: onelauncher COMMAND [OPTIONS]

Environment variables can also be used. For example, --config-directory can be  
set with ONELAUNCHER_CONFIG_DIRECTORY.

╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ --help (-h)           Display this message and exit.                         │
│ --install-completion  Install shell completion for this application.         │
│ --version             Display application version.                           │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Parameters ─────────────────────────────────────────────────────────────────╮
│ --game              Which game to load. Can be either a game type or game    │
│                     config ID. [choices: lotro, lotro-preview, ddo,          │
│                     ddo-preview]                                             │
│ --config-directory  Where OneLauncher settings are stored [default:          │
│                     /home/june/.config/onelauncher]                          │
│ --games-directory   Where OneLauncher game specific data is stored [default: │
│                     /home/june/.local/share/onelauncher/games]               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Program Options ────────────────────────────────────────────────────────────╮
│ --default-locale              Default language for games and UI              │
│ --always-use-default-locale-  Use default language for UI regardless of game │
│   for-ui --no-always-use-def  language                                       │
│   ault-locale-for-ui                                                         │
│ --games-sorting-mode          Order to show games in UI [choices: priority,  │
│                               last-played, alphabetical]                     │
│ --on-game-start               What OneLauncher should do when a game is      │
│                               started [choices: stay, close]                 │
│ --log-verbosity               Minimum log severity that will be shown in the │
│                               console and log file [choices: debug, info,    │
│                               warning, error, critical]                      │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Game Options ───────────────────────────────────────────────────────────────╮
│ --game-directory              The game's install directory                   │
│ --locale                      Language used for game                         │
│ --client-type                 Which version of the game client to use        │
│                               [choices: win64, win32, win32-legacy,          │
│                               win32-legacy]                                  │
│ --high-res-enabled            If the high resolution game files should be    │
│   --no-high-res-enabled       used                                           │
│ --standard-game-launcher-fil  Name of the standard game launcher executable. │
│   ename                       Ex. LotroLauncher.exe                          │
│ --patch-client-filename       Name of the dll used for game patching. Ex.    │
│                               patchclient.dll                                │
│ --game-settings-directory     Custom game settings directory. This is where  │
│                               user preferences, screenshots, and addons are  │
│                               stored.                                        │
│ --newsfeed                    URL of the feed (RSS, ATOM, etc) to show in    │
│                               the launcher                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Game Account Options ───────────────────────────────────────────────────────╮
│ --username              Login username                                       │
│ --display-name          Name shown instead of account name                   │
│ --last-used-world-name  World last logged into. Will be the default at next  │
│                         login                                                │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Game Addons Options ────────────────────────────────────────────────────────╮
│ --startup-scripts          Python scripts run before game launch. Paths are  │
│   --empty-startup-scripts  relative to the game's documents config directory │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Game WINE Options ──────────────────────────────────────────────────────────╮
│ --builtin-prefix-enabled      If WINE should be automatically managed        │
│   --no-builtin-prefix-enable                                                 │
│   d                                                                          │
│ --user-wine-executable-path   Path to the WINE executable to use when WINE   │
│                               isn't automatically managed                    │
│ --user-prefix-path            Path to the WINE prefix to use when WINE isn't │
│                               automatically managed                          │
│ --wine-debug-level            Value for the WINEDEBUG environment variable   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 插件开发者须知

### 如何让你的插件出现在 OneLauncher 中

上游作者会关注 [LotroInterface](https://lotrointerface.com) 上的 RSS 源，凡是格式正确的插件都会被加入。清单文件**不是**必需的。
如果你的插件还没被收录，可以在上游仓库提 issue 或发邮件给作者。

### 压缩包格式

- 插件必须以 zip 格式上传！
- 压缩包应当有一个描述性的名称（例如不要叫「skin」或「plugin」）
- 压缩包没有根目录、有多个根目录，或者包含了一部分指向数据目录的路径（如「ui/skins」或「Plugins」），这些情况可以接受，但不推荐。

### 清单文件

清单文件（compendium file）应放在插件的顶层目录中，文件名格式如下：

`{名称}.{plugin/skin/music}compendium`
例如 `Example Plugin.plugincompendium`

清单文件的内容格式如下：

```xml
<{Plugin/Skin/Music}Config>
    <Id>{LOTRO INTERFACE ID}</Id>
    <Name>{NAME}</Name>
    <Description>{DESCRIPTION}</Description>
    <Version>{VERSION}</Version>
    <Author>{AUTHOR}</Author>
    <InfoUrl>http://www.lotrointerface.com/downloads/info{LOTRO INTERFACE ID}</InfoUrl>
    <DownloadUrl>http://www.lotrointerface.com/downloads/download{LOTRO INTERFACE ID}</DownloadUrl>
    <!--描述符仅插件需要-->
    <Descriptors>
        <descriptor>{AUTHOR}\{NAME}.plugin</descriptor>
        <!--如果主插件还包含其他插件，可以添加更多描述符。这里表示所有 .plugin 文件的路径。-->
    </Descriptors>
    <!--任何类型的插件都可以添加依赖。被依赖的插件不必与依赖方类型相同-->
    <Dependencies>
        <dependency>{INTERFACE ID OF DEPENDENCY}</dependency>
        <!--依赖数量不限-->
    </Dependencies>
    <!--插件可以申请在每次启动游戏时运行一个 Python 脚本的权限。-->
    <StartupScript>{PATH TO PYTHON SCRIPT IN SAME FORMAT AS DESCRIPTORS}</StartupScript>
</{Plugin/Skin/Music}Config>
```

一个示例：

```xml
<PluginConfig>
    <Id>314159</Id>
    <Name>Example Plugin</Name>
    <Description>Does example things</Description>
    <Version>4.0.4</Version>
    <Author>June Stepp</Author>
    <InfoUrl>http://www.lotrointerface.com/downloads/info314159</InfoUrl>
    <DownloadUrl>http://www.lotrointerface.com/downloads/download314159</DownloadUrl>
    <Descriptors>
        <descriptor>JuneStepp\Example.plugin</descriptor>
        <descriptor>JuneStepp\Another Example.plugin</descriptor>
    </Descriptors>
    <Dependencies>
        <dependency>0</dependency>
        <dependency>367</dependency>
    </Dependencies>
    <StartupScript>JuneStepp\example.py</StartupScript>
</PluginConfig>
```

@lunarwtr 有一个 [vscode 扩展](https://github.com/lunarwtr/vscode-lotro-api)，可以检查清单文件及其他相关文件。其中还包含[XML schema](https://github.com/lunarwtr/vscode-lotro-api/tree/main/xsds)，你可以手动引用。

### 补丁

补丁必须与被补丁的插件保持相同的格式。最常见的问题是漏掉了改动位置之上层级的文件夹。

制作补丁时需要留意以下几点：

确保补丁……

- 与被补丁的插件保持完全相同的文件夹结构。
- 不要修改被补丁插件的清单文件。
- 安装在被补丁对象之后。
- 名称清晰明确。

### 合集

插件的合集可以通过把你想要的插件列为你的插件的依赖来实现。添加依赖的方法参见[清单文件](#清单文件)一节。

### 依赖

依赖会在你的插件之后自动安装。添加依赖的方法参见[清单文件](#清单文件)一节。Turbine Utilities 的 ID 为 `0`。

### 启动脚本

启动脚本是在每次启动游戏前运行的 Python 脚本。安装带有启动脚本的插件时，程序会向用户请求运行权限并展示脚本内容。插件应当预料到用户可能拒绝授权，并处理好这种情况。为你的插件添加启动脚本的方法参见[清单文件](#清单文件)一节。

#### 内置变量

这些是可以在启动脚本中直接使用的预置变量。

- `__file__`：你的启动脚本的字符串路径。
- `__game_dir__`：当前游戏目录的字符串路径。
- `__game_config_dir__`：当前游戏设置文件夹的字符串路径。通常位于用户文档文件夹下的「The Lord of the Rings Online」或「Dungeons and Dragons Online」，但也可以配置成其他位置。

## 自定义客户端

### OneLauncher 横幅图片

游戏横幅图片显示在 OneLauncher 新闻源的上方，通常期望尺寸为 300x136 像素，过大的图片会被缩小。放置在 `{游戏目录}/{语言资源文件夹}/banner.png` 路径的图片会替换该游戏与语言对应的默认横幅。如果用户所选语言没有对应图片，则显示默认图片。路径示例：`C://Program Files/Standing Stone Games/Lord of The Rings Online/en/banner.png`。

## 许可

GPLv3+ 许可证。版权所有 2019-2026 - June Stepp。
详见 [LICENSE](LICENSE.md) 文件。

[Font Awesome](https://github.com/FortAwesome/Font-Awesome/blob/master/LICENSE.txt) 字体采用 [SIL Open Font License](http://scripts.sil.org/OFL) 许可。

[Material Design Icons](https://github.com/Templarian/MaterialDesign/blob/master/LICENSE) 字体采用 [Apache License Version 2.0](http://www.apache.org/licenses/LICENSE-2.0) 许可。

《指环王 Online》是 Middle-earth Enterprises 的商标。
《龙与地下城 Online》是 Wizards of the Coast LLC 的商标。
《指环王 Online》与《龙与地下城 Online》游戏及标识归 Standing Stone Games LLC 所有。本项目与 Standing Stone Games LLC、Middle-earth Enterprises 及 Wizards of the Coast LLC 均无任何关联。

## 关于本分支

本仓库是 [OneLauncher](https://github.com/JuneStepp/OneLauncher) 的简体中文分支。依据 GPLv3+ 第 5a 条，在此声明所做的修改：

- **界面汉化**：新增 `zh-CN` 语言与完整的 Qt 翻译链，中文系统开箱即为中文界面
- **首次运行简化**：原先的多页设置向导改为单个「选择游戏」页面
- **免安装打包**：新增 `build/pyinstaller_compile.py`，可产出解压即用的免安装版本
- **品牌标识**：窗口标题与「关于」窗口显示 `LotroOneLauncher_CN`

原项目版权：(C) 2019-2026 June Stepp。本分支的全部改动同样以 GPL-3.0-or-later 许可发布。
