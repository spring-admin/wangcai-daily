---
version: 1.0.0
last_updated: 2026-07-11T16:57:00+08:00
tags: [mcp, tools, api, config, infrastructure]
openclaw_version: v2026.6.11
mcp_tool_count: 8_core_plus_5_extended
---

# 🔌 MCP Config — 模型上下文协议配置

> 当前OpenClaw Gateway可用的全部MCP工具，按功能域分类。
> 未来 `skill-mcps` 仓库建成后，将作为本文件的精确数据源。

---

## 🛠 核心MCP工具清单

| 工具名 | 类型 | 用途 | 认证方式 | 数据源可靠性 |
|--------|------|------|---------|-------------|
| `metaso-search` | 搜索 | 🥇 **所有搜索的首选工具**——2026-05-23起禁用其他搜索 | 无需（自带API） | 高 — 多源聚合 |
| `amap-maps` | 地图 | 位置搜索、经纬度转换、路径规划、天气查询（北京天气每日用） | Access Key | 高 — 高德官方 |
| `feishu-*` (30个) | 飞书 | IM/文档/日历/多维表格/任务/审批/通讯录/白板 | OAuth 2.0（用户授权） | 高 — 飞书官方 |
| `siyuan-sisyphus` | 思源笔记 | 读写思源笔记（openclaw笔记本可写，另两个只读） | 内置Token | 高 — 本地服务 |
| `browser-automation` | 浏览器 | 网页自动化操作、兜底抓取 | 无需 | 中 — 依赖页面渲染 |
| `trends-hub` | 热榜 | 各平台热搜（微博/知乎/36氪/B站/抖音/豆瓣等） | 无需 | 中 — 第三方聚合 |
| `opencode` | 编码 | 调用群晖NAS上的OpenCode进行开发 | OpenCode Node Token | 高 — 本地服务 |
| `cron` | 调度 | 定时任务创建/管理/运行 | 无需 | 高 — Gateway原生 |

## 🔑 认证凭据位置

| 服务 | 认证方式 | 凭据位置 |
|------|---------|---------|
| 飞书Feishu | OAuth 2.0 | 飞书应用配置（app_id + app_secret）+ 用户授权 |
| 阿里云OSS | Access Key | 环境变量 `OSS_ACCESS_KEY_ID`/`OSS_ACCESS_KEY_SECRET` |
| 微信读书API | WR Key | `~/.openclaw/env/weread.env`（cron需显式source） |
| GitHub Token | PAT | 嵌入在各仓库remote URL中（遵循最小scope原则） |
| OpenCode | Token | Gateway → NAS OpenCode节点的连接配置 |
| 思源笔记 | API Token | 本地内置 |

## 📡 搜索与内容获取供应链

```
L1: metaso-search（主力搜索——唯一搜索工具）
L2: defuddle → https://目标网址（页面转码为可读markdown）
L3: r.jina.ai → http://目标网址（转码回退，中国网络可访问）
L4: browser(profile=openclaw)（最终兜底，渲染整页）
```

## 📤 消息推送渠道

| 渠道 | 工具调用 | 参数模板 |
|------|---------|---------|
| 微信 | `message`（Gatway原生） | `action=send, channel=openclaw-weixin, message=内容` |
| 飞书IM | `feishu_im_user_message` | `action=send, receive_id_type=open_id/chat_id, msg_type=text, content='{"text":"..."}'` |

## 🗄 存储与同步

| 服务 | 用途 | 接入方式 |
|------|------|---------|
| 阿里云OSS | `calendar.ics` 备份/分享 | `siyuan0919.oss-cn-beijing.aliyuncs.com` Python SDK |
| GitHub | Skills/MCP配置备份、代码仓库 | HTTPS + PAT |
| 思源笔记 | 知识管理、AI交互日志归档 | 本地API + Siyuan MCP Skill |
| 群晖NAS | OpenCode运行、文件存储 | 本地网络 |

## 📐 CLI工具速查

| 工具 | 命令 | 用途 |
|------|------|------|
| Ontology CLI | `python3 scripts/ontology.py create\|query\|relate\|validate` | 结构化知识图谱管理 |
| 日历写入 | `python3 tasks/scripts/add_calendar_task.py --summary "任务" --date 20260605 --desc "描述"` | 代办任务写入ics |
| 思源日历同步 | `python3 tasks/scripts/sync_siyuan_calendar.py` | 思源笔记日历→本地 |
| ICS今日任务 | `python3 tasks/scripts/ics-today-tasks.py > tasks/output/ics-today-tasks.json` | 今日任务汇总JSON |
| OSS上传 | `python3 /tmp/upload_oss.py` | 本地文件上传阿里云OSS |
| 心跳处理 | `python3 tasks/scripts/heartbeat_process.py --format raw` | 检查待处理定时任务信号 |
| 消息推送测试 | `message(action=send, channel=openclaw-weixin, message=测试消息)` | 验证微信推送 |

## 🌐 Webhook/回调

| 来源 | 用途 | 接收方式 |
|------|------|---------|
| 飞书事件 | IM消息、日历变更、审批流转 | Gateway Event Handler |
| GitHub Webhook | Push/Wiki/Issue事件 | 待配置 |

> 备注：所有API凭据遵循L0-L4安全分层。Token只在需要时从环境变量读取，不硬编码。
