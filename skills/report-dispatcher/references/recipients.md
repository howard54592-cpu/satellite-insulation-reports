# 团队成员花名册

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 渠道对话ID（企微为用户名，飞书为 open_id，Telegram 为数字ID或用户名） |
| `nickname` | string | 昵称 |
| `name` | string | 姓名 |
| `channel` | string | 渠道：wecom / feishu / telegram |
| `group` | string[] | 所属分组列表 |
| `enabled` | boolean | 是否启用 |

## 默认分组（default）

```json
[
  {
    "id": "XiaoYunLong",
    "nickname": "云龙",
    "name": "肖云龙",
    "channel": "wecom",
    "group": ["default", "leadership"],
    "enabled": true,
    "note": "需在企微机器人处发过消息才能发送"
  },
  {
    "id": "ou_b3684886aec79ed01cc69552d9d4730b",
    "nickname": "总师",
    "name": "肖云龙（主会话）",
    "channel": "feishu",
    "group": ["default", "leadership"],
    "enabled": true
  },
  {
    "id": "ou_55a456ead919db40a34edc2ec2d18edf",
    "nickname": "亚特鲁",
    "name": "亚特鲁",
    "channel": "feishu",
    "group": ["default", "rd"],
    "enabled": true
  },
  {
    "id": "ou_72c5a4d4a0b77a58e965c600cde96b9d",
    "nickname": "陆姝",
    "name": "陆姝",
    "channel": "feishu",
    "group": ["default", "rd"],
    "enabled": true
  }
]
```

## 其他分组

```json
// leadership（管理层）
[
  "肖云龙"
]

// rd（研发部）
[
  "亚特鲁",
  "陆姝"
]

// tech（科技委）
[] // 暂无独立配置，与 default 合并

// qa（质量检验部）
[] // 暂无独立配置

// process（工艺技术部）
[] // 暂无独立配置
```

## 快捷查询

- **全员**：`recipients=["all"]` → 等价于所有 `enabled=true` 的成员
- **研发组**：`groups=["rd"]` → 亚特鲁 + 陆姝
- **管理层**：`groups=["leadership"]` → 肖云龙
- **默认**：`recipients=["all"]` 且未指定 `groups` → 所有 enabled=true 成员

## 新增成员流程

1. 在上方 JSON 数组中追加新条目
2. 企微渠道需要成员先与机器人互动以获取有效 chat_id
3. 飞书渠道直接使用 open_id（可从飞书管理后台获取）
4. Telegram 渠道使用数字 chat_id（群组）或 @username（个人）
