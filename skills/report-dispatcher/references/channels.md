# 渠道配置与约束

## 当前可用渠道

| 渠道 | 状态 | 配置来源 |
|------|------|----------|
| wecom | ✅ 可用 | `~/.openclaw/openclaw.json` → channels.wecom |
| feishu | ✅ 可用 | OpenClaw feishu plugin |
| telegram | ✅ 可用 | `~/.openclaw/openclaw.json` → channels.telegram |

## 各渠道限制

### 企微（wecom）

**限制：**
- 当前会话绑定飞书 channel 时无法直接向企微发消息
- 需要用户先与企微机器人有过互动，bot 才能获取到用户的 chat_id
- chat_id 使用用户名字符串（如 `XiaoYunLong`）

**发送方式：**
```python
message(
    action="send",
    channel="wecom",
    target="XiaoYunLong",  # 用户名字符串
    message="内容"
)
```

**已知可用 chat_id：**
- `XiaoYunLong` ✅（已通过测试）

### 飞书（feishu）

**限制：**
- open_id 格式：`ou_` 前缀
- 使用 `user:<open_id>` 作为 target

**发送方式：**
```python
message(
    action="send",
    channel="feishu",
    target="user:ou_xxxxxxxx",  # open_id 前加 user:
    message="内容"
)
```

**已知 open_id：**
- `ou_b3684886aec79ed01cc69552d9d4730b`（肖云龙主会话）
- `ou_55a456ead919db40a34edc2ec2d18edf`（亚特鲁）
- `ou_72c5a4d4a0b77a58e965c600cde96b9d`（陆姝）

### Telegram

**限制：**
- 需要 bot token 已配置
- 群组发送需 bot 已加入群组
- 个人发送需用户先与 bot 开始对话

**发送方式：**
```python
message(
    action="send",
    channel="telegram",
    target="<chat_id>",  # 数字ID或 @username
    message="内容"
)
```

## GitHub 仓库配置

### 仓库信息

| 报告类型 | 仓库 | 默认路径 |
|---------|------|----------|
| daily（每日早报） | howard54592-cpu/satellite-insulation-reports | reports/daily/YYYY-MM-DD.md |
| weekly（每周报告） | howard54592-cpu/satellite-insulation-reports | reports/weekly/YYYY-WXX-report.md |

### Git 推送前置条件

```bash
export HTTP_PROXY=http://127.0.0.1:8001
export HTTPS_PROXY=http://127.0.0.1:8001
export GITHUB_API_TOKEN=$(gh auth token)

git config --global user.name "AeroFlux Bot"
git config --global user.email "aeroflux@openclaw.ai"
```

### 分发脚本（scripts/dispatch.py）说明

`dispatch.py` 接收 JSON 参数：
```json
{
  "title": "报告标题",
  "content": "报告正文（markdown）",
  "report_type": "daily | weekly",
  "sync_github": true,
  "dry_run": false
}
```

执行逻辑：
1. 确定目标仓库和路径
2. 写入临时文件 `/tmp/dispatch_<type>_<date>.md`
3. git add + commit + push
4. 返回 commit URL

## 飞书文档创建

使用 `feishu_doc` 工具：
```python
feishu_doc(
    action="create",
    title="报告标题",
    folder_token=None  # 默认文件夹
)
# 返回 doc_token
feishu_doc(
    action="write",
    doc_token="<doc_token>",
    content="报告正文（markdown）"
)
```

文档创建后返回 URL：`https://feishu.cn/docx/<doc_token>`
