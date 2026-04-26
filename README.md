# AI News Bot — Diggest AI 情报日报

每日自动抓取 Product Hunt、TechCrunch、VentureBeat 等来源的 AI 新闻，用 Claude 生成中文简评，发送到飞书群。

## 目录结构

```
Diggest-AI-news-Tool/
├── README.md
├── requirements.txt
├── .env.example        # 环境变量模板
├── config.py           # ⚡ 主配置（搜索词 / RSS / 飞书凭证）
└── src/
    ├── main.py         # 入口（直接运行 or --cron 定时模式）
    ├── searcher.py     # 多来源抓取（RSS + 搜索）
    ├── formatter.py    # Claude AI 摘要 & 格式化
    └── feishu.py       # 飞书发送（Webhook / App 两种）
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入飞书 Webhook 和 Anthropic API Key
```

### 3. 配置飞书机器人

在飞书群里：**设置 → 群机器人 → 添加机器人 → 自定义机器人** → 复制 Webhook URL → 粘贴到 `.env`

### 4. 运行

```bash
# 立即运行一次（测试用）
python src/main.py

# 定时模式（每天 09:00 自动运行）
python src/main.py --cron
```

## 定时任务（服务器 Cron）

```cron
0 9 * * * cd /path/to/Diggest-AI-news-Tool && python src/main.py >> logs/cron.log 2>&1
```

## 配置说明

在 `config.py` 中可以调整：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `SEARCH_QUERIES` | 搜索词列表（weight 越高越靠前） | 10 条，PH 权重最高 |
| `RSS_FEEDS` | RSS 订阅源 | 6 个主流 AI 媒体 |
| `MAX_ITEMS_IN_REPORT` | 每日报告最多条目数 | 15 |
| `LOOKBACK_HOURS` | 只取过去 N 小时的新闻 | 24 |
| `SEND_HOUR` | 定时发送时间（24h） | 9 |
| `MIN_AI_RELEVANCE_SCORE` | AI 相关性最低分（0-100） | 60 |

## 新闻来源权重

| 来源 | 权重 |
|------|------|
| Product Hunt | 10 ⭐ |
| AI Weekly | 8 |
| TechCrunch AI | 7 |
| VentureBeat AI | 7 |
| HuggingFace Blog | 7 |
| The Verge AI | 6 |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `FEISHU_WEBHOOK_URL` | ✅ | 飞书群机器人 Webhook |
| `ANTHROPIC_API_KEY` | 推荐 | Claude API，无则降级为纯文本格式 |
| `FEISHU_APP_ID` | 可选 | 飞书应用方式（替代 Webhook） |
| `FEISHU_APP_SECRET` | 可选 | 飞书应用方式 |
| `FEISHU_CHAT_ID` | 可选 | 飞书应用方式目标群 ID |
