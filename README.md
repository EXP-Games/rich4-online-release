# 大富翁 4 · 联机重制版下载

保留原版对照入口，提供 Windows、Android 和浏览器重制版，支持八张经典地图、八种主题随机路线、单机存档和跨端联机。

[自行部署浏览器版](PLATFORM.md) · [下载与发布页](https://github.com/EXP-Games/rich4-online-release/releases) · [游戏介绍与下载站](https://exp-games.github.io/rich4-online-release/) · [完整使用手册](USER-MANUAL.md)

最新预览版 [v0.1.15-preview.20261117](https://github.com/EXP-Games/rich4-online-release/releases/tag/v0.1.15-preview.20261117) 已发布。Windows 和 Android 均为完整过场包；本期不提供轻量 APK。

## 下载 v0.1.15-preview.20261117

| 平台 | 完整包大小 | 必须下载的分卷 |
| --- | --- | --- |
| Windows x64 | 约 4.31 GB | [001](https://github.com/EXP-Games/rich4-online-release/releases/download/v0.1.15-preview.20261117/Rich4-Windows-x64-v0.1.15-preview.20261117.zip.001) · [002](https://github.com/EXP-Games/rich4-online-release/releases/download/v0.1.15-preview.20261117/Rich4-Windows-x64-v0.1.15-preview.20261117.zip.002) · [003](https://github.com/EXP-Games/rich4-online-release/releases/download/v0.1.15-preview.20261117/Rich4-Windows-x64-v0.1.15-preview.20261117.zip.003) |
| Android ARM64 | 约 3.31 GB | [001](https://github.com/EXP-Games/rich4-online-release/releases/download/v0.1.15-preview.20261117/Rich4-Android-arm64-v0.1.15-preview.20261117.apk.001) · [002](https://github.com/EXP-Games/rich4-online-release/releases/download/v0.1.15-preview.20261117/Rich4-Android-arm64-v0.1.15-preview.20261117.apk.002) |

同一文件夹还需要：[release-manifest.json](https://github.com/EXP-Games/rich4-online-release/releases/download/v0.1.15-preview.20261117/release-manifest.json) · [Merge-Packages.cmd](https://github.com/EXP-Games/rich4-online-release/releases/download/v0.1.15-preview.20261117/Merge-Packages.cmd) · [Merge-Packages.ps1](https://github.com/EXP-Games/rich4-online-release/releases/download/v0.1.15-preview.20261117/Merge-Packages.ps1) · [SHA256SUMS.txt](https://github.com/EXP-Games/rich4-online-release/releases/download/v0.1.15-preview.20261117/SHA256SUMS.txt)。双击 CMD 后先校验并合并，再解压 ZIP 或安装 APK。Windows 要下载 **3 卷**，Android 要下载 **2 卷**。

Windows／Android 所有公开分卷及拼接后的完整文件 SHA-256 已核对通过：[校验报告](docs/release-015-downloads.json)。

## 随机路线与移动提示

开始游戏时，在地图选择页开启「随机」，选择主题后设置角色并开局；联机房间由房主在「选择地图」中开启。道路、地产、公共设施以及海岸、水域、地表分区和景物随本局生成，使用所选主题的音乐、价格与已有素材。宇宙使用星空与岩地，南岛使用沙滩、浅海与棕榈。

开启随机后，可先查看本局道路、地产和主题地形的实际俯视预览，再决定开局。路网包含不规则环线、双环、共享走廊、L 形、内湾和曲折环线六类。

随机局可保存、读取和断线恢复，恢复时保留原来的地图与行走进度。新生成地图会避让特殊地点和购房地块的完整图案范围；旧存档保持原布局。联机所有玩家与平台须使用相同规则版本，旧规则版本不能混入本局；仅界面微调不要求相同构建版本。

掷骰后，人物脚下显示剩余步数；每走完一格减 1，移动结束后消失。提示随人物、镜头、旋转和缩放更新。

## 1. 平台启动方式

平台提供房间管理和联机转发。解压 Windows 发行包后，进入 `Rich4/bin/`，安装 Python 3.11+ 即可启动原生联机大厅；独立平台部署包也可在其根目录启动：

```powershell
$env:RICH4_ADMIN_TOKEN='请替换为自己的管理令牌'
python lobby/server.py --bind 0.0.0.0 --port 27654 --http-bind 127.0.0.1 --http-port 27655 --room-store ./data/rooms.json --create-room 4
```

游戏客户端连接 `服务器IP:27654`；管理页打开 <http://127.0.0.1:27655/>，使用管理令牌登录。`--create-room 4` 创建四席位平台房间，已有持久房间时可省略。Linux 使用 `export RICH4_ADMIN_TOKEN='自己的管理令牌'` 设置令牌。管理页不向玩家公开。

## 2. Web 后端和前端启动方式

部署包运行已构建前端：

```powershell
python lobby/server.py --bind 0.0.0.0 --port 27654 --http-bind 127.0.0.1 --http-port 27655 --room-store ./data/rooms.json --web-bind 0.0.0.0 --web-port 27656 --client-root ./web
```

打开 `http://服务器IP:27656/`。HTTP／WebSocket 使用 27656，原生 TCP 使用 27654。首次部署需准备与清单匹配的 `web/engine/data/` 素材；更新代码可复用素材。

从源码启动时先按 [平台与 Web 启动说明](PLATFORM.md) 构建 WASM、准备资源和前端，然后将 `--client-root ./web` 换为 `--client-root ./web-client/dist`。前端单独开发运行 `npm --prefix web-client run dev`，打开 `http://127.0.0.1:5173/`；后端允许来源 `--web-origin http://127.0.0.1:5173`，游戏内服务器填写 `ws://127.0.0.1:27656/connect`。

## 3. Web 浏览器版本游玩

先按 [平台启动说明](PLATFORM.md) 自行部署 Web 服务，再打开部署地址（例如 `http://服务器IP:27656/`），等待首批资源准备，选择「开始游戏」或「多人联机」。使用 HTTP／WS，无需证书。网页存档保存在当前浏览器和站点中，清除站点数据会删除存档，不同设备不自动共享。

## 4. Windows 版本游玩

下载 Windows 包；若为分卷，先下载全部分卷及合并工具，运行 `Merge-Packages.cmd` 校验还原 ZIP。全部解压后打开 `Rich4/`：

| 入口 | 用途 |
| --- | --- |
| `大富翁4-Re.exe` | 高清重制版，日常游玩入口 |
| `大富翁4-Re.cmd` | 显示控制台日志的重制版入口 |
| `大富翁4.exe` | 原版对照入口，默认《多元宇宙之旅》 |

保留完整目录，包含 `resources/Fonts/`；中文字体已随包提供，无需在电脑上另外安装。重制版成品包可直接运行；原版入口和 Windows 本地建房需要 Python 3.11+，加入平台房间不需要 Python。原版和重制版设置、存档独立。日志统一放在 `logs/`。

## 5. Android 版本游玩

Android 8.0+ 的 64 位 ARM 手机安装 ARM64 完整 APK。若为分卷，先在电脑上运行合并工具还原 APK，再传到手机安装；不能直接安装 `.001`。本地 x86_64 完整包用于对应架构模拟器。

首次启动需准备资源，预留安装和解压空间。完整包包含 21 段独立过场及全部游戏内动画、音乐和语音，无需额外下载过场。同签名版本可覆盖安装保留数据；当前使用开发签名。

## 6. 联机步骤

1. Windows／Android 服务器填自己部署的 `服务器IP:27654`；浏览器打开自己部署的网页，使用当前站点服务，或填 `ws://服务器IP:27656/connect`。
2. 填写昵称。房主平台建房，或使用管理员给出的平台房间；其他玩家输入相同六位口令，点击「加入房间」。
3. 切换人物，房主设置地图、期限和席位。空位开局补 AI，关闭席位不参与。
4. 选择离线预案并准备；未加入房间前准备按钮不可点击。其他玩家准备后由房主开始。
5. 当前行动者操作 GO、道具和卡片。同步期间点击会保留一次操作，完成后自动执行。正常结算后回到原房间。

Windows「本地建房」监听 `0.0.0.0`，其他设备连接房主实际的局域网／公网 IP，不能使用 `127.0.0.1`。浏览器「本地建房」由当前服务器托管。局域网以外直连需开放或转发端口。联机不提供存档，服务重启不保留进行中的对局；断线按预案执行，重连在安全边界恢复席位。

UI 与布局微调的小版本，在联机规则代次兼容时可共同游玩；规则不兼容时需更新客户端。

## 操作与文档

经典八图：中国台湾、中国大陆、日本、美国、宇宙、武侠、恐龙、南岛历险。单机有 30 个存档槽，包含 1 个自动存档。右侧资料卡查看资金、地产、股票和其他信息，小地图旁按钮定位、旋转和缩放。

- [使用手册](USER-MANUAL.md)：下载安装、六种启动／游玩方式、联机、存档与常见问题。
- [官方原版说明书](https://cdn.akamai.steamstatic.com/steam/apps/2059810/manuals/%E5%A4%A7%E5%AF%8C%E7%BF%814%E8%AA%AA%E6%98%8E%E6%9B%B8.pdf?t=1658992525)：原版规则 PDF。
- [平台与 Web 启动说明](PLATFORM.md)：平台部署、前后端启动、端口与运行维护。

原版文件与重制版独立，原始资源仅用于已有游戏的本地重制与对照，请遵守相应版权和分发约束。
