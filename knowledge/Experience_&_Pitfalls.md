---
version: 1.0.0
last_updated: 2026-07-11T16:57:00+08:00
tags: [experience, pitfalls, best-practices, continuously-updated]
pitfall_count: 7
best_practice_count: 5
---

# 📖 Experience & Pitfalls — 经验与避坑指南

> 本章记录实战血泪史和经过验证的高效工作流。
> 新踩的坑和新的最佳实践自动添加到此文件。

---

## 🕳️ 踩坑记录

### 坑1：子代理不可靠 → Script-First改造
- **时间**：2026-05-22 发现 → 2026-06-19 根治
- **场景**：定时任务结果推送卡壳，信号文件留在tasks/output/无人处理
- **根因**：
  - cron agentTurn prompt里塞了太多任务（跑脚本+MCP搜索+内容整理+message推送）
  - deepseek-v4-flash在isolated session经常跑不满1200s超时
- **解决**：
  - Script-First改造：脚本自己采集数据+生成push_content
  - cron agentTurn只做三件事：跑脚本 → 读push_content → 返回
  - 超时从1200s降至120s
- **教训**：不要依赖AI处理复杂的数据采集流程，脚本应该自给自足
- **受影响脚本**：morning_news.py, ai_news.py, chen_editor.py, it_audit.py, study_review.py, daily_study_push.py（全部已改为needs_ai: False）

### 坑2：数据真实性翻车 → 微信读书API切换
- **时间**：2026-06-01
- **场景**：《明朝那些事儿》被误报为进度99%
- **根因**：使用已失效的第三方API（weread.deno.dev）
- **解决**：
  - 切换至微信读书官方API（https://i.weread.qq.com/api/agent/gateway）
  - 后续还经历了API Key更新后cron仍用旧Key的环境变量继承问题（坑3）
- **教训**：数据供应链必须多源回退，单点依赖等于没查；数据源头必须追溯到官方

### 坑3：环境变量继承陷阱
- **时间**：2026-06-06
- **场景**：微信读书API Key更新后cron任务仍失败（errcode -2010「用户不存在」）
- **根因**：cron子进程继承gateway(PID1)的旧环境变量，不读取.env文件
- **解决**：
  - 在cron指令中显式 `source /home/node/.openclaw/env/weread.env`（before curl）
  - SIGHUP重启cron
- **教训**：环境变更必须考虑进程树继承链，不能只改文件；cron需要显式source环境变量文件

### 坑4：中国网站对爬虫不友好 → 三级回退
- **时间**：2026-06-15
- **场景**：旺财日报采集新闻，央视网等RSS源/网页接口被封
- **根因**：目标网站对非浏览器流量做限制
- **解决**：defuddle → r.jina.ai → browser(profile=openclaw) 三级回退
- **教训**：中国网站对爬虫友好度时好时坏，必须预留多级回退方案

### 坑5：硬件兼容性翻车
- **时间**：2026-06-04
- **场景**：买完硬件发现网卡不兼容群晖
- **解决**：换成兼容型号
- **教训**：买硬件前先查兼容性列表，P40之外的大路货才稳

### 坑6：OpenCode MCP通而不通
- **时间**：2026-06-08
- **场景**：安装了opencode-mcp但OpenCode实例没接到MCP请求
- **根因**：OpenCode需要独立的Agent配置 + 正确的URL/Token配对
- **解决**：在OpenCode中新建Agent（Sisyphus等）+ 配置3主7子Agent
- **教训**：MCP装好不算完，两端的Agent配置必须pair好；需要完整的3主7子配置才能发挥全部能力

### 坑7：GitHub Actions + Hugo部署踩空
- **时间**：2026-06-01
- **场景**：旺财日报从Jekyll迁Hugo，GitHub Actions跑不起来
- **根因**：
  - 用于Hugo部署的ghp_xxx token无workflow权限
  - GitHub raw资源在中国大陆连不上（Hugo二进制下载失败）
- **解决**：放弃Hugo+Actions方案，改用纯HTML直接推到main分支，GitHub Pages读取根目录
- **教训**：对中国用户，CI/CD依赖海外资源必须先测连通性；一遇阻就切方案，不跟工具死磕

### 坑8：[空位 — 下次踩坑后补]

---

## ✅ 最佳实践

### BP1：Script-First架构（2026-06-19起标准化）
所有定时/周期性任务采用以下模型：
1. 脚本自包含——不依赖AI处理，自己爬数据、整理、输出push_content
2. 脚本头部加 `needs_ai: False` 标记
3. cron agentTurn prompt极简化：「跑脚本→读push_content→返回」
4. 超时统一120s
5. 兜底：每30分钟catchall-cleanup cron检查output遗落文件并清理

### BP2：三级内容获取链（数据供应链韧性）
```
L1: metaso-search（主力搜索，不可替代）
L2: defuddle → https://目标网址（页面转码）
L3: r.jina.ai → http://目标网址（二次转码）
L4: browser(profile=openclaw)（浏览器兜底，最后手段）
```
每一级失败自动降级到下一级，不中断流程。

### BP3：数据安全分层
```
L0: 环境变量（env/目录）         — Token/Key/Secret（不硬编码）
L1: Gateway进程PID1            — 持久化环境
L2: cron指令显式source          — 避免继承链陷阱
L3: GitHub Secrets             — CI/CD凭据（有限scope）
L4: 专用配置文件（.env/.json）   — 定期轮换
```

### BP4：多Agent编排模式（已超越Claude Code）
```
问题 → Sisyphus（主Agent，Claude Opus 4.7）
         ├─ build（编码执行）
         ├─ librarian（知识检索）
         ├─ oracle（技术咨询）
         ├─ Metis（策略分析）
         ├─ Momus（代码审查）
         ├─ explore（探索验证）
         └─ multimodal-looker（多模态处理）
→ Hephaestus（质量保障）
→ Prometheus（战略评估）
```
各Agent职责清晰，不互相覆盖。泉哥定位为「AI之上的决策者」，让AI管理AI。

### BP5：每日晨间报告生产流程（已验证10+次）
1. 检测 `morning_report_signal`
2. 读取 `news_focus.json`（7个关注点，涵盖AI/企业应用/审计/融资/中美博弈/政策/宏观）
3. 每个关注点用metaso-search搜索2-3条
4. 每条展开至少2-3句描述（不只是标题）
5. 获取北京天气（amap-maps__maps_weather）
6. 汇总日历今日任务（3个ics文件各自读取，不合并）
7. 按规范格式化推送微信
