# 平台与 Web 服务启动说明

请自行部署平台，或连接房主自行部署的服务器。Windows／Android 客户端可以单机游玩；浏览器版需要先部署 Web 服务，再打开部署地址。

## 部署目录

独立平台部署目录包含 `lobby/`（Python 服务与管理页）和 `web/`（已构建前端、WASM 与资源清单）。完整资源在 `web/engine/data/`；增量代码包不包含该大素材目录，首次部署须单独准备与 `web/engine/resources.json` 匹配的资源。服务器不需要 Git 仓库。

使用 Python 3.11+。管理令牌、房间数据与代码分开保管；更新时只替换已校验的程序和页面，不覆盖私有数据。

## 只启动平台

Windows 发行包已包含原生联机大厅：解压后进入 `Rich4/bin/`，安装 Python 3.11+，即可运行下列命令；独立平台部署包则在其根目录运行：

```powershell
$env:RICH4_ADMIN_TOKEN='请替换为自己的随机管理令牌'
python lobby/server.py --bind 0.0.0.0 --port 27654 --http-bind 127.0.0.1 --http-port 27655 --room-store ./data/rooms.json --create-room 4
```

Linux 使用 `export RICH4_ADMIN_TOKEN='自己的随机管理令牌'` 设置环境变量，其余 Python 命令相同。启动输出显示创建的房间口令；已有持久房间时省略 `--create-room 4`，避免每次增加新房间。

管理页打开 `http://127.0.0.1:27655/`，输入管理令牌。Windows／Android 玩家连接 `服务器IP:27654` 并填写房间口令。管理令牌与房间口令用途不同，管理令牌不发给玩家。

## 同时启动 Web 前端与后端

浏览器版需要单独准备完整 Web 部署包；Windows 发行包只包含原生大厅，不含 Web 游戏前端。安装 Web 依赖并设置管理令牌，然后运行：

```powershell
python -m pip install -r lobby/requirements-web.txt
python lobby/server.py --bind 0.0.0.0 --port 27654 --http-bind 127.0.0.1 --http-port 27655 --room-store ./data/rooms.json --web-bind 0.0.0.0 --web-port 27656 --client-root ./web
```

打开 `http://服务器IP:27656/`。已构建前端由同一个服务提供，不需要另开 Node.js 进程；HTTP 与 WebSocket 共用 Web 端口，原生 TCP 端口独立。

| 用途 | 默认端口 | 客户端填写 |
| --- | --- | --- |
| Windows／Android 原生联机 | TCP 27654 | `服务器IP:27654` |
| Web 游戏与 WebSocket | HTTP／WS 27656 | 浏览器打开网页；服务器可填 `ws://服务器IP:27656/connect` |
| 管理页面 | HTTP 27655，仅回环地址 | 本机打开 `http://127.0.0.1:27655/` |

如将 Web 服务部署在 HTTP 80 端口，浏览器打开 `http://服务器IP/`，对应 WebSocket 为 `ws://服务器IP/connect`。HTTP／WS 部署不需要 HTTPS 证书。

## 分别运行前端开发服务器

此模式需要管理员已有源码工作区、Node.js/npm、已编译的 WASM 与 `web-client/public/engine/` 资源。源码仓库需要访问权限；普通玩家不需要源码。

后端使用上述带 Web 的启动命令，并增加 `--web-origin http://127.0.0.1:5173`；源码工作区内的前端目录采用 `--client-root ./web-client/dist`。另一个终端运行：

```powershell
npm --prefix web-client ci
npm --prefix web-client run dev
```

打开 `http://127.0.0.1:5173/`，游戏房间内的服务器填写 `ws://127.0.0.1:27656/connect`。5173 是前端开发端口，不能填到原生客户端。

## 运行维护

- 管理页保留回环监听，远程管理使用 SSH 隧道，不开放管理令牌给公网。
- `--room-store` 只持久化平台房间配置与口令，不保存进行中的对局。重启前确认无在线玩家。
- 玩家端口需要服务器防火墙允许；局域网直连使用实际局域网 IP，`127.0.0.1` 不能发给其他设备。
- 生产环境可由 systemd 管理。WorkingDirectory 与 ExecStart 指向独立部署目录，ReadWritePaths 指向独立数据目录，避免引用已删除的源码仓库。
- 部署后检查网页、WebSocket、TCP 及真实建房／开局。健康检查可访问 Web 服务的 `/health`。

安装包、游戏操作与断线恢复见 [使用手册](USER-MANUAL.md)。
