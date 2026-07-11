---
version: 1.0.0
last_updated: 2026-07-11T16:57:00+08:00
tags: [skills, inventory, mcp]
skill_count: 95
source_repo: https://github.com/spring-admin/wangcai-daily (work-in-progress)
---

# 🛠 Skills — 技能树

> 当前OpenClaw已安装的全部Skills汇总（约95个）。
> 未来 `skill-mcps` 仓库建成后，将作为本文件的精确数据源。

---

## 🎯 核心执行类 Skill

| 技能名称 | Skill位置 | 用途 | 触发方式 | 预期输出 |
|---------|-----------|------|---------|---------|
| `morning-news-cron` | skills/morning-news-cron | 晨间新闻推送全流程 | cron定时/手动 | 格式化的微信早报 |
| `daily-study-push` | skills/daily-study-push | 备考学习提醒与推送 | cron定时 | 学习进度+题目推送 |
| `self-improving-agent` | skills/self-improving-agent | Agent自我改进闭环 | 心跳/手动 | 规则更新+优化建议 |
| `proactive-agent` | skills/proactive-agent | 主动执行模式 | 条件触发 | 预处理+预检查 |
| `exec-guard` | skills/exec-guard | 命令执行安全护卫 | 执行前自动拦截 | 命令安全评级+放行/拦截 |
| `clawpressor` | skills/clawpressor | 上下文压缩复用 | 长对话时调用 | 压缩后的上下文摘要 |
| `clawswitch` | skills/claw-switch | Agent/Runtime切换 | 动态条件 | 切换后的新会话 |

## 🤖 AI模型与Agent集成

| 技能名称 | 用途 | 调用方式 |
|---------|------|---------|
| `claude-code` | Claude Code集成 | MCP/命令行 |
| `claude-code-mastery` | Claude Code高级用法 | 按需调用 |
| `codebuddy-code` | CodeBuddy CLI集成 | MCP/命令行 |
| `hermes-agent` | Hermes记忆代理 | 非重要工作前调取 |
| `kb-retriever` | 知识库检索 | 搜索增强 |
| `context-compressor` | 上下文管理压缩 | 长对话调用 |
| `context-engineering` | 上下文工程 | 优化prompt构造 |
| `interview-me` | AI面试模拟 | 按需触发 |
| `idea-refine` | 想法打磨与深化 | 创意讨论时调用 |
| `self-improving-agent` | 持续自我改进 | 心跳时触发 |

## 📡 搜索与数据采集

| 技能名称 | 用途 | 优先级 |
|---------|------|--------|
| `cn-web-search-2.4.0` | 中文网络搜索 | 🥇 首选用metaso-search MCP |
| `find-skills` | 技能发现 | 按需 |
| `mcp-tool-utils` | MCP工具管理 | 调试/配置时 |
| `mcp-config` | MCP配置 | 配置修改时 |
| `crawling-social-media` | 社交媒体爬取 | 数据采集任务 |

## 📝 内容生产

| 技能名称 | 用途 | 典型场景 |
|---------|------|---------|
| `documentation-and-adrs` | 文档/ADR生成 | 技术决策记录 |
| `diagram-maker` | 图表生成 | 架构图/流程图 |
| `image-prompt-generator` | AI绘图提示词生成 | DALL-E/Midjourney |
| `meme-maker` | 梗图制作 | 娱乐/社交 |
| `image-analysis-litiao` | 图片分析 | 读取图片内容 |
| `gpt-image-2` | GPT图片生成 | DALL-E 3生成 |

## 📊 财经审计与专业知识

| 技能名称 | 用途 | 领域 |
|---------|------|------|
| `a-stock-financial` | A股财务分析 | 投资/财务 |
| `audit-data-assistant` | 审计数据助手 | IT审计 |
| `senior-accountant` | 高级会计知识 | 中级会计备考 |
| `chen-yiwei-combined` | 陈轶玮审计综合 | IT审计专业 |
| `chen-yiwei-perspective` | 陈轶玮审计视角 | IT审计专业 |
| `chenyiwei-bbs` | 审计论坛 | IT审计社群 |
| `fortune-master-pro` | 命理/运势分析 | 个人/娱乐 |

## 🔧 开发工程

| 技能名称 | 用途 |
|---------|------|
| `api-and-interface-design` | API接口设计 |
| `ci-cd-and-automation` | CI/CD自动化 |
| `code-review-and-quality` | 代码审查 |
| `code-simplification` | 代码简化重构 |
| `debugging-and-error-recovery` | 调试与错误恢复 |
| `deprecation-and-migration` | 废弃迁移 |
| `incremental-implementation` | 增量式实现 |
| `performance-optimization` | 性能优化 |
| `planning-and-task-breakdown` | 计划与任务拆分 |
| `security-and-hardening` | 安全加固 |
| `frontend-ui-engineering` | 前端工程 |
| `git-workflow-and-versioning` | Git工作流 |

## 🛡 安全防护

| 技能名称 | 用途 |
|---------|------|
| `security-auditor` | 安全审计（对应泉哥IT审计背景） |
| `360guard-skillvetter-upgrade-version` | 360安全卫士+技能审查 |
| `moltguard` | 安全防护 |
| `exec-guard` | 执行安全护卫 |

## 🏥 健康考试与辅助

| 技能名称 | 用途 |
|---------|------|
| `medical-advice` | 医疗建议 |
| `exam-prep` | 考试备考（中级会计方向） |
| `ontologys` | 知识图谱管理 |
| `doubt-driven-development` | 怀疑驱动开发 |
| `shipping-and-launch` | 发布启动 |
| `idea-refine` | 想法打磨 |

## 🗄 文件与存储

| 技能名称 | 用途 | 备注 |
|---------|------|------|
| `file-manager` | 文件管理 | 日常工作 |
| `baidu-netdisk-storage` / `baidu-drive` | 百度网盘 | 备份/共享 |
| `paddleocr-doc-parsing-v2` | OCR文档解析 | 中英文OCR |
| `pdf-ocr` | PDF OCR | 扫描件文字提取 |
| `pdf` | PDF处理 | 合并/拆分/转换 |

## 📦 飞书生态（约30个Skill）

| 类别 | 技能清单 | 用途 |
|------|---------|------|
| **IM** | `lark-im`, `lark-markdown`, `lark-event`, `lark-shared` | 消息收发/富文本/事件监听/共享 |
| **文档** | `lark-doc`, `lark-sheets`, `lark-slides`, `lark-note`, `lark-markdown`, `lark-create-doc`, `lark-update-doc`, `lark-fetch-doc` | 全类型文档CRUD |
| **驱动** | `lark-drive` | 云空间文件管理 |
| **基础** | `lark-base`, `lark-calendar`, `lark-task`, `lark-approval`, `lark-attendance`, `lark-contact`, `lark-mail` | 业务数据/日程/任务/审批/考勤/通讯录/邮箱 |
| **维基** | `lark-wiki` | 知识库管理 |
| **协作** | `lark-whiteboard`, `lark-vc`, `lark-vc-agent`, `lark-minutes` | 白板/会议/会议纪要 |
| **构建** | `lark-skill-maker`, `lark-openapi-explorer`, `lark-workflow-meeting-summary`, `lark-workflow-standup-report` | Skill构建/API探索/工作流 |
| **其他** | `lark-search-doc-wiki`, `lark-perm`, `lark-channel-rules`, `lark-fetch-doc`, `lark-drive` | 搜索/权限/频道/分享/驱动 |

## 🌐 其他集成

| 技能名称 | 用途 | 调用入口 |
|---------|------|---------|
| `baidu-netdisk-ai-video-notes` | 网盘视频AI笔记 | 百度网盘 |
| `siyuan-mcp` | 思源笔记MCP | 思源API |
| `openclaw-agent-optimize` | OpenClaw Agent优化 | 系统级 |
| `openclaw-backup` | 备份（Skills/MCP配置→GitHub） | 定时/手动 |
| `auto-updater` | 自动更新 | 系统级 |
| `mmskills-agent-adapter` | 多模态Skill适配 | 实验性 |
| `easy-openclaw` | OpenClaw简易操作 | 日常管理 |
| `healthcheck` | 系统健康检查 | 心跳/定时 |

> 🔄 每个Skill的详细SKILL.md在对应skills/目录下。
> 新的Skill通过`skill_workshop`工具创建，经审批后生效。
