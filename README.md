# 🤖 AI 每日情报机器人

自动抓取 AI 创投 + 技术动态，每天推送到飞书。

## 功能特点

- 🌐 多来源搜索：YC / Product Hunt / GitHub Trending / TechCrunch / 行业媒体
- 📊 智能分类：AI应用层 ≥60%，其余补足至20条
- 🏷️ 自动标签：YC / PH / GH / 新品 / 融资 / 工具
- 📱 飞书推送：支持 Webhook 或开放平台 App 两种方式
- ⏰ 定时任务：Linux crontab 一键配置

## 快速开始

### 1. 克隆 + 安装

```bash
git clone <your-repo-url> ai-news-bot
cd ai-news-bot
pip install -r requirements.txt
```

### 2. 配置

**方式 A：飞书 Webhook（最简单）**

在飞书群聊中添加"自定义机器人"（群设置 → 群机器人 → 添加机器人），
复制 Webhook URL，填入 `config.py` 的 `webhook_url` 字段。

**方式 B：飞书开放平台 App**

在 [飞书开放平台](https://open.feishu.cn/app) 创建应用，
获取 `App ID` 和 `App Secret`，填入 `config.py`。

### 3. 配置搜索偏好

编辑 `src/config.py` 中的 `SEARCH_QUERIES` 列表，调整：
- Product Hunt 权重 → 增加 PH 相关查询词
- YC 权重 → 增加 Y Combinator 相关查询词

### 4. 测试

```bash
python src/feishu.py          # 测试飞书连通性
python src/main.py --test     # 发送测试消息
python src/main.py --dry      # 仅生成内容，不发送
```

### 5. 定时任务

```bash
# 每天早上 9 点（北京时间）执行
0 9 * * * cd /path/to/ai-news-bot && python src/main.py >> logs/cron.log 2>&1
```

## 目录结构

```
ai-news-bot/
├── README.md
├── requirements.txt
├── .env.example
├── config.py              ← 主配置文件
└── src/
    ├── main.py            ← 入口，cron 调用这个
    ├── searcher.py        ← 多来源搜索
    ├── formatter.py        ← 情报格式化
    └── feishu.py           ← 飞书发送
```

## 与 OpenClaw 集成

如果部署在运行 OpenClaw 的同一台机器上，`searcher.py` 会自动
通过本地 MCP 端口（localhost:3100）加速搜索，无需额外配置。

## 自定义信源

在 `config.py` 中编辑 `SEARCH_QUERIES`，格式：

```python
("搜索关键词", 返回条数),
```

## Product Hunt 权重调整

恒宇要求 Product Hunt 权重上调。当前配置已包含：
- Product Hunt AI 产品热门
- Product Hunt AI 工具发布
- YC AI 初创公司

如需进一步上调，增加 PH 相关查询词在列表中的比重即可。
