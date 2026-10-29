"""
config.py
所有可配置参数集中在这里，修改这里即可调整行为
"""

# ── 搜索配置 ────────────────────────────────────────────────────────────────

SEARCH_QUERIES = [
    # ═══════════════════════════════════════════════════════════════════════
    # ⭐⭐⭐ 国产大模型厂商商业化硬数据（恒宇 2026-10-29 指定最高权重）
    #   特征：产品进展 + 可量化数字（ARR/收入/增速/定价/财报指引/生态接入）
    # ═══════════════════════════════════════════════════════════════════════
    ("智谱 AI ARR 收入 指引 2026", 16),
    ("Zhipu AI ARR revenue guidance 2026", 14),
    ("MiniMax 收入 ARR 定价 2026", 16),
    ("MiniMax AI revenue API pricing 2026", 14),
    ("DeepSeek 融资 估值 IPO 2026", 14),
    ("月之暗面 Kimi 营收 商业化 2026", 14),
    ("Moonshot Kimi revenue commercialization 2026", 12),
    ("字节豆包 收入 日活 商业化 2026", 14),
    ("阿里千问 Qwen 商业化 收入 企业客户", 12),
    ("国产大模型 财报 业绩指引 收入 增速", 14),
    ("国产大模型 API 降价 定价 token 价格 2026", 12),
    ("阶跃星辰 面壁智能 零一万物 融资 营收", 10),
    ("百度文心 腾讯混元 收入 商业化 进展 2026", 12),

    # ═══════════════════════════════════════════════════════════════════════
    # ⭐⭐⭐ 头部公司技术研究细节（恒宇重点关注，权重最高）
    # ═══════════════════════════════════════════════════════════════════════

    # OpenAI 官方研究博客
    ("OpenAI research blog new paper last 5 days", 12),
    ("OpenAI technical report GPT model June 2026", 10),
    ("OpenAI API new feature release last week", 8),
    # Anthropic 官方研究博客
    ("Anthropic research blog interpretability Claude", 12),
    ("Anthropic Constitutional AI alignment research 2026", 8),
    ("Anthropic Claude API feature update last week", 8),
    # Google DeepMind 官方
    ("Google DeepMind research blog Gemini last week", 12),
    ("DeepMind paper Nature Science June 2026", 8),
    ("Google AI research paper arxiv last 5 days", 10),
    # Meta FAIR
    ("Meta FAIR research paper Llama last week", 10),
    ("Meta AI research announcement June 2026", 8),
    # xAI
    ("xAI Grok model release technical report last week", 10),
    ("xAI research blog announcement", 8),
    # Mistral
    ("Mistral AI model release technical report last week", 10),
    ("Mistral research paper arxiv", 6),

    # ═══════════════════════════════════════════════════════════════════════
    # ⭐⭐⭐ 国产头部公司技术细节
    # ═══════════════════════════════════════════════════════════════════════

    # DeepSeek
    ("DeepSeek R2 V3 technical report arxiv last week", 12),
    ("DeepSeek new model release research June 2026", 10),
    # 智谱 GLM
    ("Zhipu GLM 5.2 technical report research last week", 10),
    ("Zhipu AI research paper arxiv last 5 days", 8),
    # Moonshot Kimi
    ("Moonshot Kimi K2 model update technical report last week", 10),
    ("Moonshot AI research paper last 5 days", 8),
    # 阿里 Qwen
    ("Alibaba Qwen 3.7 technical report arxiv last week", 10),
    ("Qwen Tongyi research paper last 5 days", 8),
    # 字节豆包
    ("ByteDance Doubao Seed 2.1 technical report last week", 10),
    ("Seed research paper arxiv last 5 days", 8),
    # 百度文心
    ("Baidu Ernie 5 Wenxin technical report last week", 8),
    # 阶跃星辰
    ("StepFun Step research paper last week", 6),
    # MiniMax
    ("MiniMax M3 technical report arxiv last week", 8),
    ("MiniMax research paper last 5 days", 6),

    # ═══════════════════════════════════════════════════════════════════════
    # ⭐⭐⭐ 高质量独立来源（深度报道/Newsletter）
    # ═══════════════════════════════════════════════════════════════════════

    # Simon Willison's Weblog (深度 AI 实战派)
    ("Simon Willison AI blog last 5 days", 10),
    # Latent Space (顶级 AI 工程播客)
    ("Latent Space podcast AI engineering last week", 8),
    # Import AI (Jack Clark, 政策+研究)
    ("Import AI newsletter last week", 8),
    # The Batch (Andrew Ng)
    ("The Batch Andrew Ng deeplearning.ai last week", 8),
    # Last Week in AI
    ("Last Week in AI newsletter last 5 days", 8),
    # TLDR AI
    ("TLDR AI newsletter last 5 days", 8),
    # Stratechery (战略分析)
    ("Stratechery AI analysis last week", 6),

    # ═══════════════════════════════════════════════════════════════════════
    # ⭐⭐ 应用层：Product Hunt / YC / GitHub（精简到只关注头部）
    # ═══════════════════════════════════════════════════════════════════════

    # Product Hunt（只关注本周冠军+AI类前10）
    ("Product Hunt AI tools top this week", 12),
    ("Product Hunt AI productivity trending last 7 days", 10),
    # YC（官方新闻+新批次）
    ("Y Combinator new AI startup launched last week", 10),
    ("YC W26 batch AI company announcement", 8),
    # GitHub Trending（只关注高star的LLM/Agent项目）
    ("GitHub trending AI repository this week stars", 10),
    ("GitHub trending LLM agent framework last 7 days", 8),

    # ═══════════════════════════════════════════════════════════════════════
    # 顶级研究机构（MIT/Stanford/CMU + arXiv 顶会）
    # ═══════════════════════════════════════════════════════════════════════

    ("MIT CSAIL AI research last week", 8),
    ("Stanford HAI research announcement last 5 days", 8),
    ("arXiv cs.AI most cited last 5 days", 10),
    ("NeurIPS ICML ICLR 2026 best paper announced", 10),
    ("Nature Science AI paper published last week", 8),

    # ═══════════════════════════════════════════════════════════════════════
    # 极简版大厂动态（仅重要发布事件）
    # ═══════════════════════════════════════════════════════════════════════

    ("AI model release announcement last 5 days", 10),
    ("OpenAI Anthropic Google DeepMind news last week", 8),

    # ═══════════════════════════════════════════════════════════════════════
    # 基础设施/芯片（精简）
    # ═══════════════════════════════════════════════════════════════════════

    ("NVIDIA AI chip announcement last week", 5),

    # ═══════════════════════════════════════════════════════════════════════
    # 金融·资本市场（美股高管交易 + 上市公司动态）
    # ═══════════════════════════════════════════════════════════════════════

    ("AI company CEO CFO sold shares last week", 8),
    ("tech executive bought sold stock last week", 8),
    ("AI startup acquisition merger last week", 6),
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
    # ── 国产厂商（恒宇 2026-10-29 指定最高权重）────────────────────
    "domestic_min": 4,          # 国产厂商/商业化数据最少4条
    "domestic_ratio": 0.30,     # 国产厂商 + 商业化数据占比 ≥30%
    "max_news_age_days": 5,     # 恒宇要求:新闻时效 ≤5天
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


# ═══════════════════════════════════════════════════════════════════════
# 📦 高质量AI内容来源推荐池（恒宇要求:更多渠道）
# ═══════════════════════════════════════════════════════════════════════
# 每天随机推荐一个,作为📦来源推荐section的内容
SOURCE_POOL = [
    {
        "name": "Simon Willison's Weblog",
        "tagline": "AI实战派深度评测,Llama/Claude/GPT一手使用经验",
        "why": "每篇都是实战测试,技术细节扎实,适合追踪头部模型真实能力差异",
        "url": "https://simonwillison.net/",
        "category": "深度评测"
    },
    {
        "name": "Latent Space",
        "tagline": "顶级AI工程播客,采访AI Lab核心研究员和创始人",
        "why": "嘉宾质量极高(OpenAI/Anthropic/DeepMind一线),话题前沿",
        "url": "https://www.latent.space/",
        "category": "播客"
    },
    {
        "name": "The VC Corner",
        "tagline": "YC官方RFS(Requests for Startups)季度深度解读",
        "why": "YC每季度发布150+创业方向,这是创业雷达的源头",
        "url": "https://www.thevccorner.com/",
        "category": "创投"
    },
    {
        "name": "Import AI (Jack Clark)",
        "tagline": "政策+研究双重视角,前OpenAI政策总监主理",
        "why": "政策动态+学术前沿结合,适合理解监管和宏观趋势",
        "url": "https://importai.substack.com/",
        "category": "Newsletter"
    },
    {
        "name": "The Batch (Andrew Ng)",
        "tagline": "DeepLearning.AI官方周刊,基础模型+应用案例双覆盖",
        "why": "吴恩达团队出品,内容深度稳定,适合系统性跟进",
        "url": "https://www.deeplearning.ai/the-batch/",
        "category": "Newsletter"
    },
    {
        "name": "TLDR AI",
        "tagline": "每日AI新闻简报,5分钟读完所有要点",
        "why": "覆盖面广,适合快速扫描每日动态",
        "url": "https://tldr.tech/ai",
        "category": "Newsletter"
    },
    {
        "name": "Last Week in AI",
        "tagline": "周更AI综述,Podcast+Newsletter双形式",
        "why": "结构化整理一周要闻,适合周末回看",
        "url": "https://lastweekin.ai/",
        "category": "Newsletter"
    },
    {
        "name": "Stratechery (Ben Thompson)",
        "tagline": "顶级科技战略分析,AI对产业格局影响",
        "why": "战略视角独到,适合理解AI商业格局变化",
        "url": "https://stratechery.com/",
        "category": "深度分析"
    },
    {
        "name": "MIT Technology Review (AI)",
        "tagline": "MIT权威科技媒体,AI研究与产业报道",
        "why": "学术严谨+产业洞察,适合做深度决策",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/",
        "category": "权威媒体"
    },
    {
        "name": "The Information (AI)",
        "tagline": "硅谷深度科技媒体,AI公司内部消息",
        "why": "爆料能力强,常领先主流媒体掌握AI公司动向",
        "url": "https://www.theinformation.com/",
        "category": "深度媒体"
    },
    {
        "name": "量子位 QbitAI",
        "tagline": "国内AI头部媒体,日更产业+技术动态",
        "why": "国内AI动态最及时最全,适合追踪国产大模型和应用",
        "url": "https://www.qbitai.com/",
        "category": "中文媒体"
    },
    {
        "name": "机器之心 SOTA模型",
        "tagline": "国内AI技术报道标杆,论文+开源项目解读",
        "why": "技术翻译质量高,适合追踪国内学术前沿",
        "url": "https://www.jiqizhixin.com/",
        "category": "中文媒体"
    },
]

# ── 输出格式 ───────────────────────────────────────────────────────────────

CONFIG = {
    "search_queries": SEARCH_QUERIES,
    "feishu": FEISHU,
    "recipients": RECIPIENTS,
    "total_target": DIGEST_CONFIG["total_target"],
}