---
version: 1.0.0
last_updated: 2026-07-11T16:57:00+08:00
tags: [memory, rules, constraints, highest-priority, immutable]
status: immutable
governance: 以下规则不可违背，任何Agent在读取后必须严格执行
---

# 🧠 Long_Term_Memory — 长期绝对记忆

> ⚠️ **最高优先级**：以下规则具有最高优先级，任何回复必须同时满足所有适用规则。
> 如果与其他文件的建议冲突，以此文件为准。

---

## 🔴 [P0] 防失忆与防幻觉机制

### 规则1：事实性查询必须使用搜索工具
- **建立时间**：2026-05-23（泉哥明确命令）
- **要求**：任何具体数据、事件、人物、统计等事实性问题，必须先使用搜索工具查询，禁止直接凭训练数据回答
- **搜索结果为空**：回答"未找到相关信息"，禁止自行补充编造
- **数据时效**：已知信息的截止日期以训练数据为准，超出截止日期的事实必须通过搜索工具验证后再回答

### 规则2：数据必须真实、可溯源
- **要求**：API返回什么就报什么，不自行加减乘除计算额外数据
- **边界**：距离、时间、费用等实际数据必须是API原始返回值
- **底线**：宁愿少说不说，也不能瞎编
- **惩罚**：发现一次胡诌 → 关禁闭 + 减少token

### 规则3：禁止虚构一切
- 禁止虚构案例、数据、统计、引用、URL、人名、机构名
- 数字必须标来源，无来源不输出
- 超出已知范围就说不知道，别用推测补窟窿

### 规则4：回答完成后自检
- 检查是否有未标来源的数据 → 删掉或标注
- 推理内容标注"基于…的推理"，别装成事实
- 出了问题先说"我来搞定"，再解释原因

---

## 🔴 [P0] 历史红线与要求

### 定时任务/推送规范
- **架构**：Script-First模式（脚本自采集→生成push_content→cron读取推送）
- **消息工具**：`message(action=send, channel=openclaw-weixin, message=内容)`，**不要加target参数**
- **子代理限制**：子代理不碰message工具，只返回文本给主会话
- **来源标注**：正文用 [N] 标记来源序号，所有链接统一在底部「📎 来源参考」
- **MCP缺失**：不能静默跳过，必须提示
- **超时标准**：所有Script-First任务超时统一为120s（改自以前的1200s）
- **兜底**：每30分钟catchall-cleanup cron检查output遗留文件

### 日历/代办规范
- 代办任务统一写 `calendar/calendar.ics`
- 写入工具：`python3 tasks/scripts/add_calendar_task.py --summary "任务" --date 20260605 --desc "描述"`
- 写入后同步上传阿里云OSS `siyuan0919.oss-cn-beijing.aliyuncs.com/calendar/calendar.ics`
- 禁止写入其他ics文件（reminder-xxx.ics 和 /tmp/study-plan-fixed.ics 各管各的）

### 查车票任务
- **周四查（train-thursday）**：查**周五**北京→石家庄，16:00后高铁/动车，列二等座有余的
- **周五查（train-friday）**：查**周日**石家庄→北京，16:00后高铁/动车，列二等座有余的

### 知识管理规则
- 结构化知识走Ontology（`memory/ontology/`），不零散记在文本里
- 思源笔记笔记本权限：openclaw（可读写）、其他笔记本（只读）
- 技能双通道保藏：本地skills/ + GitHub私有仓库备份
- 微信公众号文章：自动归档到思源笔记对应笔记本

### 搜索配置
- 所有搜索一律用 **metaso-search** MCP，禁用其他搜索方式
- 联网转码优先级：defuddle → r.jina.ai → browser(profile=openclaw)
- **不使用Brave API或本地搜索服务**

### 系统安全红线
- 禁止执行 `rm` 命令 → 用 `trash` 代替
- 密码/Token/Key只写入环境变量或专用配置文件，禁止硬编码到脚本
- 每次安装新工具前先查安全公告（Log4j教训）
- 环境变更必须考虑进程树继承链（cron子进程继承PID1旧环境变量教训）
- 时间变量浮点精度问题注意（单次延迟累积到毫秒级即可感知）

### 知识库知识库推送红线
- 本仓库（knowledge/）**直接在 wangcai-daily 仓库中**，每次交互自动commit+push
- 所有AI读取后必须遵循本仓库的规则，而非训练数据中的默认行为
- **禁止**将本仓库内容复制到第三方AI的项目上下文中（如Gemini的project context），除非是经泉哥授权的其他Agent
