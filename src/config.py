"""
config.py
所有可配置参数集中在这里，修改这里即可调整行为
"""

# ── 搜索配置 ────────────────────────────────────────────────────────────────

SEARCH_QUERIES = [
    # AI 应用层（Product Hunt 方向）
    ("Product Hunt AI products trending 2026", 10),
    ("Product Hunt AI tools launched 2026", 8),
    ("Y Combinator AI Startups W26 2026", 8),
    ("YC startup AI application 2026", 8),
    ("Y Combinator AI portfolio demo day 2026", 8),
    # GitHub Trending AI
    ("GitHub trending AI LLM open source 2026", 8),
    ("GitHub trending machine learning tools 2026", 6),
    ("site:github.com trending 2026", 8),
    ("GitHub go-to-github trending repositories April 2026", 8),
    ("GitHub open source AI tools trending 2026", 7),
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
    # ── 金融·资本市场动态 ─────────────────────────────────
    # 科技公司高管增减持（AI相关上市公司）
    ("AI company CEO CFO sold shares stock 2026", 8),
    ("tech executive bought sold stock June 2026", 8),
    ("OpenAI Anthropic Google DeepMind executive stock 2026", 6),
    # AI 上市公司最新融资/减持/回购
    ("AI public company raised capital stock offering 2026", 6),
    ("Nvidia CEO Jensen Huang sold stock 2026", 5),
    ("Microsoft Apple Google executive stock sale 2026", 5),
    # 风险投资机构新动态
    ("venture capital fund AI startup investment 2026", 6),
    ("a16z Sequoia Capital AI deal 2026", 6),
    ("VC funding AI agent applications 2026", 6),
    # 美股科技板块动态
    ("NASDAQ AI tech stocks earnings 2026", 5),
    ("S&P 500 AI semiconductor stocks news 2026", 5),
    # 并购/IPO 动态
    ("AI company acquisition merger 2026", 6),
    ("AI startup IPO filing 2026", 6),
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
    "total_target": 20,        # 目标总条数 ← 已更新至20条
    "app_layer_min": 12,       # AI应用层最少条数
    "app_layer_ratio": 0.60,   # AI应用层占比 ≥60%
    "label_source": "PH",      # Product Hunt 标签
    "label_yc": "YC",
    "label_gh": "GH",
    "label_tool": "工具",
    "label_new": "新品",
    "label_fund": "融资",
    "label_finance": "金融",   # 金融/资本市场标签
    "label_exec": "高管交易", # 高管增减持标签
    "label_mna": "并购",       # 并购标签
    "label_ipo": "IPO",
    # ── 去重配置 ────────────────────────────────────────
    "dedup_window_days": 7,     # 7 天内不重复推送同一 URL（避免近一个月内重复新闻）
    "history_file": "data/published_history.json",
}

# ── 输出格式 ───────────────────────────────────────────────────────────────

CONFIG = {
    "search_queries": SEARCH_QUERIES,
    "feishu": FEISHU,
    "recipients": RECIPIENTS,
    "total_target": DIGEST_CONFIG["total_target"],
}