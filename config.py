import os
from dotenv import load_dotenv

load_dotenv()

# ─── 飞书配置 ────────────────────────────────────────────────
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL", "")
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_CHAT_ID = os.getenv("FEISHU_CHAT_ID", "")

# ─── AI 摘要配置 ─────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-6"

# ─── 搜索词配置（权重越高排序越靠前）───────────────────────────
SEARCH_QUERIES = [
    # Product Hunt 专属（权重最高）
    {"query": "site:producthunt.com AI tool 2025", "weight": 10, "source": "ProductHunt"},
    {"query": "producthunt.com/posts AI application launch", "weight": 9, "source": "ProductHunt"},
    # 核心 AI 应用层
    {"query": "AI application SaaS product launch 2025", "weight": 8, "source": "General"},
    {"query": "LLM app new product AI tool release", "weight": 8, "source": "General"},
    {"query": "generative AI startup launch funding 2025", "weight": 7, "source": "General"},
    # 行业动态
    {"query": "AI agent workflow automation new 2025", "weight": 7, "source": "General"},
    {"query": "ChatGPT Claude Gemini new feature update", "weight": 6, "source": "General"},
    {"query": "AI coding tool developer productivity 2025", "weight": 6, "source": "General"},
    # 融资 & 商业
    {"query": "AI startup funding Series A B 2025", "weight": 5, "source": "General"},
    {"query": "AI company acquisition partnership 2025", "weight": 5, "source": "General"},
]

# RSS 订阅源
RSS_FEEDS = [
    {"url": "https://www.producthunt.com/feed", "name": "Product Hunt", "weight": 10},
    {"url": "https://feeds.feedburner.com/TechCrunchAI", "name": "TechCrunch AI", "weight": 7},
    {"url": "https://venturebeat.com/category/ai/feed/", "name": "VentureBeat AI", "weight": 7},
    {"url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "name": "The Verge AI", "weight": 6},
    {"url": "https://aiweekly.co/issues.rss", "name": "AI Weekly", "weight": 8},
    {"url": "https://huggingface.co/blog/feed.xml", "name": "HuggingFace Blog", "weight": 7},
]

# ─── 过滤配置 ─────────────────────────────────────────────────
MAX_RESULTS_PER_SOURCE = int(os.getenv("MAX_RESULTS_PER_SOURCE", "10"))
MIN_AI_RELEVANCE_SCORE = int(os.getenv("MIN_AI_RELEVANCE_SCORE", "60"))
MAX_ITEMS_IN_REPORT = 15  # 每次报告最多条目数

# ─── 时间配置 ─────────────────────────────────────────────────
LOOKBACK_HOURS = 24  # 只取过去 N 小时内的新闻
SEND_HOUR = 9        # 每天几点发送（24h 制）
