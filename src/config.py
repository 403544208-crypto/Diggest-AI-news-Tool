"""
config.py
所有可配置参数集中在这里，修改这里即可调整行为
"""

# ── 搜索配置 ────────────────────────────────────────────────────────────────

SEARCH_QUERIES = [
    # AI 应用层（Product Hunt 方向）
    ("Product Hunt AI products trending 2026", 10),
    ("Product Hunt AI tools launched 2026", 8),
    # Y Combinator AI Startups W26 2026", 8),
    ("YC startup AI application 2026", 8),
    ("Y Combinator AI portfolio demo day 2026", 8),
    # GitHub Trending AI
    ("GitHub trending AI LLM open source 2026", 8),
    ("GitHub trending machine learning tools 2026", 6),
    # AI Agent & 应用层
    ("AI agent framework new release 2026", 8),
    ("LLM application startup product launch 2026", 8),
    ("AI coding tools new product 2026", 6),
    # AI 融资
    ("AI startup Series A funding 2026", 6),
    ("AI agent startup raised seed round 2026", 6),
    # 大厂动态
    ("GPT Claude Gemini new model release 2026", 6),
    ("Anthropic OpenAI Google DeepMind news April 2026", 8),
    ("字节豆包 阿里通义 百度文心 AI动态 2026", 6),
    # 基础设施
    ("NVIDIA AMD AI chip news 2026", 5),
    ("AI infrastructure data center investment 2026", 5),
]

# ── 飞书配置 ────────────────────────────────────────────────────────────────

FEISHU = {
    # 方式一：Webhook（无需配置 App，简单）
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_ID",

    # 方式二：飞书开放平台 App（支持更复杂消息）
    # 请从 https://open.feishu.cn/app 创建企业内部应用
    "app_id": "",           # cli_xxx
    "app_secret": "",        # App Secret
    "chat_id": "",          # 需要推送的会话 ID
}

# ── 推送目标 ────────────────────────────────────────────────────────────────

# 推送给谁（webhook 方式下此字段不生效）
RECIPIENTS = [
    "ou_ea0289cfea518ab7b1d63d4107fd146f",  # 恒宇
]

# ── 格式化配置 ─────────────────────────────────────────────────────────────

DIGEST_CONFIG = {
    "total_target": 20,        # 目标总条数
    "app_layer_min": 12,       # AI应用层最少条数
    "app_layer_ratio": 0.60,   # AI应用层占比 ≥60%
    "label_source": "PH",      # Product Hunt 标签
    "label_yc": "YC",
    "label_gh": "GH",
    "label_tool": "工具",
    "label_new": "新品",
    "label_fund": "融资",
}

# ── 输出格式 ───────────────────────────────────────────────────────────────

CONFIG = {
    "search_queries": SEARCH_QUERIES,
    "feishu": FEISHU,
    "recipients": RECIPIENTS,
    "total_target": DIGEST_CONFIG["total_target"],
}
