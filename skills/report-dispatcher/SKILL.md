---
name: report-dispatcher
description: 航天热防护材料领域报告（早报/周报/快讯）的多渠道分发技能。当需要向多位团队成员或多个渠道（企微/飞书/Telegram）同步推送报告时激活。也适用于"发送早报给所有人"、"按分组发周报"、"推送到企微和飞书"等任务。
---

# report-dispatcher

航天领域报告多渠道分发技能。

## 核心能力

- **多渠道并发推送**：企微 / 飞书 / Telegram 可任意组合
- **多接收对象**：支持按个人或分组选择，默认全选
- **附件同步**：自动写入飞书文档 + 推送 GitHub 仓库
- **发送回执**：每次分发记录到 `memory/dispatch-log.jsonl`

## 快速使用

```json
{
  "content": "报告正文内容（markdown）",
  "title": "报告标题",
  "report_type": "daily | weekly | alert",
  "channels": ["wecom", "feishu", "telegram"],
  "recipients": ["all"] | ["肖云龙", "陆姝"],
  "groups": ["default"] | ["研发", "科技委"],
  "sync_feishu": true,
  "sync_github": true,
  "dry_run": false
}
```

**最小调用示例：**
```
发送早报：channels=["wecom"], recipients=["肖云龙"]
```

## 工作流程

### Step 1 — 读取花名册与渠道配置

- 花名册：`skills/report-dispatcher/references/recipients.md`
- 渠道配置：`skills/report-dispatcher/references/channels.md`

### Step 2 — 解析分发列表

根据 `channels` + `recipients` + `groups` 确定实际发送目标：

```
channels = ["wecom", "feishu"]
recipients = ["肖云龙", "亚特鲁"]
groups = ["default"]

→ 肖云龙(wecom) + 亚特鲁(wecom) + 肖云龙(feishu) + 亚特鲁(feishu)
```

### Step 3 — 渠道发送

**企微**（wecom）：
- 调用 `message(action=send, channel=wecom, target=<chat_id>, message=<content>)`
- chat_id 格式：用户名字符串（如 `XiaoYunLong`）
- 发送前确保目标用户在企微侧已与机器人有过互动

**飞书**（feishu）：
- 调用 `message(action=send, channel=feishu, target=user:<open_id>, message=<content>)`
- open_id 格式：`ou_` 前缀

**Telegram**：
- 调用 `message(action=send, channel=telegram, target=<chat_id>, message=<content>)`
- chat_id 可为数字ID或用户名（如 `@username`）

### Step 4 — 附件同步（可并行）

**飞书文档**（`sync_feishu=true`）：
- 调用 `feishu_doc(action=create, title=<title>)`
- 用 `feishu_doc(action=write, doc_token=<token>, content=<content>)` 写入正文
- 返回文档链接

**GitHub 推送**（`sync_github=true`）：
- 使用 `scripts/dispatch.py` 自动处理
- 早报 → `satellite-insulation-reports/reports/daily/` 目录
- 周报 → `satellite-insulation-reports/reports/weekly/` 目录
- 自动 commit + push

### Step 5 — 记录发送日志

每次发送后，追加一行到 `memory/dispatch-log.jsonl`：
```json
{"ts": 1775430000, "title": "...", "channel": "wecom", "recipient": "肖云龙", "status": "ok", "message_id": "..."}
```

## 报告类型与格式模板

### daily（每日早报）
```
🛡️🔥 航天热防护材料每日简报 - YYYY-MM-DD

🔥 核心进展
• ...

📊 关键数据
• ...

🔭 前沿探索
• ...

---
来源：... | 编译：AeroFlux
```

### weekly（每周报告）
```
📊 卫星绝热材料每周研究报告 - YYYY-WXX

一、本周研究背景与目标
...

二、文献综述
...

三、专利分析
...

四、行业动态
...

五、可行性评估
...

六、结论与建议
```

### alert（实时快讯）
```
🚨 [紧急] 航天热防护材料快讯 - YYYY-MM-DD HH:MM

[标题]
[内容摘要]
详情：<链接>
```

## GitHub 仓库配置

| 报告类型 | 仓库 | 路径 |
|---------|------|------|
| daily | howard54592-cpu/satellite-insulation-reports | reports/daily/ |
| weekly | howard54592-cpu/satellite-insulation-reports | reports/weekly/ |

如需修改仓库配置，编辑 `references/channels.md`。

## 注意事项

- **dry_run=true**：只打印发送计划，不实际发送，用于确认分发范围
- **某渠道失败不阻断其他渠道**：try-catch 隔离各渠道
- **飞书 open_id** 必须从 `references/recipients.md` 读取，不要硬编码
- **企微 chat_id** 为用户名字符串，发送前需确认用户已与机器人互动
- **Telegram group** 发送需确认机器人已加入群组
