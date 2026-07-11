---
last_updated: 2026-07-11T16:57:00+08:00
version: 1.0.0
tags: [index, manifest, entry, master]
author: 旺财 (OpenClaw AI Assistant)
repo: https://github.com/spring-admin/wangcai-daily/tree/main/knowledge
status: active
auto_update: true
---

# 🧠 旺财AI私人知识库 — 总索引 (Master Index)

> **任何Agent** 读取本仓库后，应在 **1 轮对话内** 完全掌握用户人设、技术栈、偏好、约束和能力边界。
> 这是唯一的总纲文件。所有维度的更新必须同步更新本文件。

---

## 📋 维度清单

| # | 文件 | 维度 | 描述 | 最后更新 | 优先级 |
|---|------|------|------|---------|--------|
| 1 | `AI_Persona.md` | 核心人设 | AI名称、角色、风格、禁限清单 | 2026-07-11 | 🔴 P0 |
| 2 | `User_Profile.md` | 用户档案 | 技术栈、沟通习惯、核心关注点、历史轨迹 | 2026-07-11 | 🔴 P0 |
| 3 | `Long_Term_Memory.md` | 长期绝对记忆 | 防幻觉规则、历史红线（最高优先级） | 2026-07-11 | 🔴 P0 |
| 4 | `Experience_&_Pitfalls.md` | 经验与避坑指南 | 踩坑记录、最佳实践（持续更新） | 2026-07-11 | 🟡 P1 |
| 5 | `Skills.md` | 技能树 | OpenClaw Skills清单 | 2026-07-11 | 🟡 P1 |
| 6 | `MCP_Config.md` | MCP连接配置 | 工具列表、API端点、鉴权方式 | 2026-07-11 | 🟢 P2 |

## 🔄 版本历史

| 版本 | 日期 | 变更内容 | 提交者 |
|------|------|---------|--------|
| 1.0.0 | 2026-07-11 | 首次初始化，6维度+总索引全部生成 | 旺财 |

## 📌 快速加载指南

```bash
# 方式1：快速加载（适合轻量Agent）
cat Master_Index.md AI_Persona.md User_Profile.md Long_Term_Memory.md > /tmp/brief.txt

# 方式2：深度加载（适合全功能Agent）
cat Master_Index.md AI_Persona.md User_Profile.md Long_Term_Memory.md \
    Experience_&_Pitfalls.md Skills.md MCP_Config.md > /tmp/full_brief.txt
```

## ⚙️ 自进化规则

- **触发时机**：每次交互结束后自动执行
- **更新流程**：提炼新知识 → 增量修改对应文件 → Git Add/Commit/Push
- **Commit前缀**：`[Auto-Evolve]`
- **回滚方案**：如果自动更新导致冲突，手动 `git revert HEAD`
