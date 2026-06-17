"""
config.py
所有可配置参数集中在这里，修改这里即可调整行为
"""

# ── 搜索配置 ────────────────────────────────────────────────────────────────

SEARCH_QUERIES = [
    # AI 应用层（Product Hunt 方向）— 质量关键
    ("Product Hunt AI tools trending week 2026", 12),
    ("Product Hunt AI productivity tools launched 2026", 12),
    ("Product Hunt AI developer tools new this month 2026", 10),
    ("Product Hunt AI assistant apps top rated 2026", 10),
    ("Product Hunt AI automation bots 2026", 10),
    ("Product Hunt AI design creative tools 2026", 8),
    ("Y Combinator AI startups demo day 2026", 10),
    ("YC W26 Summer 2026 AI startup batch", 10),
    # GitHub Trending AI — 真实新产品
    ("GitHub trending AI open source new release 2026", 10),
    ("GitHub trending LLM tool this week 2026", 10),
    ("GitHub new AI repository trending 2026", 8),
    # AI Agent & 应用层新品
    ("AI agent new product launch June 2026", 10),
    ("AI startup product launch June 2026", 10),
    ("AI tool launched this week 2026", 10),
    ("AI app new release this month 2026", 10),
    ("autonomous AI agent new version 2026", 8),
    ("AI coding assistant new tool 2026", 8),
    # ── 保留：AI 融资（但聚焦应用层，不是大厂模型）─────────────────
    ("AI agent startup raised seed round June 2026", 8),
    ("AI application startup Series A funding June 2026", 8),
    # ── 保留：大厂动态（仅限实际发布事件）──────────────────────
    ("OpenAI Anthropic Google DeepMind news June 2026", 8),
    ("AI model release announcement June 2026", 8),
    # ── 大幅压缩：基础设施/芯片（不是应用层）───────────────
    ("NVIDIA AI chip news June 2026", 5),
    # ── 保留：金融·资本市场（美股上市公司高管交易）──────────
    ("AI company CEO CFO sold shares stock June 2026", 8),
    ("OpenAI Anthropic Google executive stock sale June 2026", 6),
    ("tech executive bought sold stock June 2026", 8),
    ("NASDAQ AI tech stocks earnings news June 2026", 6),
    ("AI startup acquisition merger June 2026", 6),
    ("AI startup IPO filing 2026", 6),
    # ── 字节/阿里/百度/智谱/阶跃星辰（已恢复 2026-06-17）──────────
    ("Zhipu GLM new model release research 2026", 8),
    ("Zhipu AI research paper arxiv 2026", 6),
    ("Moonshot Kimi K2 model update 2026", 8),
    ("DeepSeek new model release technical report 2026", 10),
    ("DeepSeek R2 V3 research paper 2026", 8),
    ("Alibaba Qwen Tongyi new model release 2026", 8),
    ("Qwen3 Qwen2.5 technical report arxiv 2026", 6),
    ("ByteDance Doubao Seed model release 2026", 6),
    ("Baidu Ernie 5 Wenxin model 2026", 5),
    ("StepFun Step ai research 2026", 5),
    ("MiniMax model release research 2026", 5),
    # ── 基座模型研究：国际顶会/论文/实验室 ─────────────────────
    ("arXiv LLM pretraining scaling 2026", 10),
    ("arXiv new LLM architecture attention 2026", 10),
    ("arXiv reasoning model test-time compute 2026", 10),
    ("NeurIPS ICML ICLR 2026 LLM paper accepted", 10),
    ("OpenAI research blog GPT model 2026", 10),
    ("Anthropic research blog Claude interpretability 2026", 10),
    ("Google DeepMind research blog Gemini 2026", 10),
    ("Meta FAIR Llama research paper 2026", 8),
    ("Mistral AI research technical report 2026", 8),
    ("xAI Grok research model release 2026", 6),
    ("Nature Science LLM foundation model paper 2026", 8),
    ("SWE-bench MMLU ARC-AGI benchmark result 2026", 8),
    ("LLM Stats model release update 2026", 8),
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
    "total_target": 20,
    "app_layer_min": 10,        # AI应用层最少10条
    "app_layer_ratio": 0.50,    # AI应用层占比 ≥50%
    "base_model_min": 5,        # 基座模型研究最少5条
    "base_model_ratio": 0.25,   # 基座模型研究占比 ≥25%
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
    "label_base": "基模",       # 基座模型研究标签
    # ── 去重配置 ────────────────────────────────────────
    "dedup_window_days": 7,     # 7 天内不重复推送同一 URL
    "dedup_title_threshold": 0.75,  # 标题相似度阈值（>0.75 视为同一条）
    "history_file": "data/published_history.json",
}

# ── 输出格式 ───────────────────────────────────────────────────────────────

CONFIG = {
    "search_queries": SEARCH_QUERIES,
    "feishu": FEISHU,
    "recipients": RECIPIENTS,
    "total_target": DIGEST_CONFIG["total_target"],
}