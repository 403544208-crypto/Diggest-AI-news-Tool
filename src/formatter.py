"""
formatter.py
AI 情报格式化器

按照恒宇要求的格式输出：
  - AI应用层 ≥60%（YC / PH / GH / 新品 / 融资 / 工具 标签）
  - 基座模型研究 ≥25%（恒宇重点关注:头部公司技术细节）
  - 金融/资本市场动态（金融、高管交易、并购、IPO 标签）
  - 来源推荐 ≥1条
  - 其他动态 补足至 20 条
  - 新闻时效 ≤5 天（恒宇要求）
"""

import re
import random
from datetime import datetime, timedelta
from config import DIGEST_CONFIG, SOURCE_POOL


APP_LABELS = {"PH", "YC", "GH", "新品", "融资", "工具"}
FINANCE_LABELS = {"金融", "高管交易", "并购", "IPO"}
BASE_MODEL_LABELS = {"基模"}
DOMESTIC_LABELS = {"国产", "国产商业化"}


# 关键词 → 时效天数(估算),用于在 snippet 中识别发布时间
DATE_PATTERNS = [
    (r"(\d+)\s*hours?\s*ago", "hours"),
    (r"(\d+)\s*day(?:s)?\s*ago", "days"),
    (r"(\d+)\s*min(?:ute)?s?\s*ago", "min"),
    (r"yesterday", "yesterday"),
    (r"just\s*now", "now"),
]


def _extract_age_days(snippet: str, title: str = "") -> int | None:
    """从 snippet/title 中提取新闻距今天数。返回 None 表示无法判断。"""
    text = (title + " " + snippet).lower()
    for pat, kind in DATE_PATTERNS:
        m = re.search(pat, text)
        if m:
            if kind == "now":
                return 0
            if kind == "yesterday":
                return 1
            if kind == "min":
                return 0
            if kind == "hours":
                return 0
            if kind == "days":
                n = int(m.group(1))
                return min(n, 30)  # cap at 30
    return None


def _age_label(days: int | None) -> str:
    """把天数转成可读标签,如 '今天'/'1天前'"""
    if days is None:
        return ""
    if days == 0:
        return "今天"
    if days == 1:
        return "昨天"
    return f"{days}天前"


def guess_category(item: dict) -> str:
    """判断是 AI应用层、基座模型研究、金融/资本市场 还是 其他动态"""
    if item.get("label") in FINANCE_LABELS:
        return "finance"
    if item.get("label") in BASE_MODEL_LABELS:
        return "base_model"
    if item.get("label") in DOMESTIC_LABELS:
        return "domestic"
    if item.get("label") in APP_LABELS:
        return "app"
    # 关键词二次判断
    text = (item.get("title", "") + " " + item.get("snippet", "")).lower()
    if any(k in text for k in [
        "arxiv", "research", "paper", "technical report", "benchmark",
        "swe-bench", "mmlu", "arc-agi", "neurips", "icml", "iclr", "acl",
        "pretraining", "pre-training", "fine-tuning", "rlhf", "rlaif",
        "reasoning model", "test-time compute", "scaling", "moe",
        "long context", "attention", "transformer", "state space", "mamba",
        "diffusion model", "architecture", "sparse", "mixture of experts",
        "synthetic data", "post-training", "interpretability", "alignment",
        "openai", "anthropic", "deepmind", "meta ai", "fair", "mistral", "xai",
        "gpt-", "claude", "gemini", "llama", "grok", "qwen", "deepseek",
        "glm-", "kimi", "doubao", "ernie", "wenxin", "minimax",
        "evaluation"
    ]):
        return "base_model"
    if any(k in text for k in [
        "launch", "release", "product", "startup", "raise", "funding",
        "series", "demo day", "open source", "github", "agent", "tool",
        "introducing", "new", "beta", "announce"
    ]):
        return "app"
    return "other"


def format_source(item: dict) -> str:
    """单条情报的富文本格式"""
    label = item.get("label", "动态")
    title = item["title"]
    snippet = item.get("snippet", "")
    url = item.get("url", "")

    # 截断标题（过长）
    if len(title) > 80:
        title = title[:77] + "..."

    parts = [f"{label} "]
    parts.append(f"【{title}】")
    if snippet:
        parts.append(f"  {snippet}")
    if url:
        parts.append(f"  🔗 {url}")

    return "".join(parts)


class DigestFormatter:
    def __init__(self):
        self.cfg = DIGEST_CONFIG

    def format(self, items: list[dict], date: str) -> str:
        """
        将原始条目列表格式化为飞书消息文本。
        恒宇要求:新闻时效 ≤5 天
        """
        target = self.cfg["total_target"]
        max_age_days = 5  # 恒宇硬性要求

        # 0. 时效过滤:只保留 ≤5 天的新闻
        filtered = []
        for it in items:
            age = _extract_age_days(it.get("snippet", ""), it.get("title", ""))
            it["_age_days"] = age
            # age=None 表示无法判断(保留),age>5 过滤掉
            if age is None or age <= max_age_days:
                filtered.append(it)
        items = filtered

        # 分类
        domestic_items = [it for it in items if guess_category(it) == "domestic"]
        app_items      = [it for it in items if guess_category(it) == "app"]
        base_items     = [it for it in items if guess_category(it) == "base_model"]
        finance_items  = [it for it in items if guess_category(it) == "finance"]
        other_items    = [it for it in items if guess_category(it) == "other"]

        # 配额（应用层 ≥50%，基座模型 ≥25%）
        app_min       = max(self.cfg.get("app_layer_min", 10), int(target * self.cfg.get("app_layer_ratio", 0.50)))
        base_min      = max(self.cfg.get("base_model_min", 5), int(target * self.cfg.get("base_model_ratio", 0.25)))
        dom_min       = max(self.cfg.get("domestic_min", 4), int(target * self.cfg.get("domestic_ratio", 0.30)))
        domestic_count = min(max(len(domestic_items), dom_min), target - base_min - app_min)
        app_count     = min(max(len(app_items), app_min), target - base_min - domestic_count)
        base_count    = min(max(len(base_items), base_min), target - app_count)
        finance_count = min(len(finance_items), 5)

        # 取条
        domestic_section = domestic_items[:domestic_count]
        app_section     = app_items[:app_count]
        base_section    = base_items[:base_count]
        finance_section = finance_items[:finance_count]
        cap_other       = target - len(domestic_section) - len(app_section) - len(base_section) - len(finance_section)
        other_section   = other_items[:max(0, cap_other)]

        def _format_item(item: dict) -> list:
            label = item.get("label", "动态")
            title = item["title"]
            snippet = item.get("snippet", "")
            url = item.get("url", "")
            age = item.get("_age_days")
            age_tag = f" · ⏱{_age_label(age)}" if age is not None else ""
            fixed_tag = " · 🔧已修" if item.get("url_fixed") else ""
            dead_tag = " · ⚠️死链" if item.get("url_dead") else ""

            if len(title) > 80:
                title = title[:77] + "..."
            lines = [f"【{label}】 {title}{age_tag}{fixed_tag}{dead_tag}"]
            if snippet:
                lines.append(f"  📌 {snippet[:100]}")
            if url and not item.get("url_dead"):
                lines.append(f"  🔗 {url}")
            elif item.get("url_dead"):
                lines.append(f"  🔍 自行搜索: {title[:50]}")
            return lines

        lines = [
            f"🤖 AI每日情报 · {date}",
            "━" * 28,
            "⏱ 时效过滤:≤5天 | 🎯 聚焦头部公司技术研究",
            "",
        ]

        # ── 来源推荐（从 SOURCE_POOL 每日随机一个）───────────────────────
        if SOURCE_POOL:
            src = random.choice(SOURCE_POOL)
            lines.append("📦 来源推荐")
            lines.append(f"【{src['category']}】 {src['name']}")
            lines.append(f"  📍 {src['tagline']}")
            lines.append(f"  💡 {src['why']}")
            lines.append(f"  🔗 {src['url']}")
            lines.append("")

        # ── 国产厂商 + 商业化数据（恒宇最高权重）─────────────────────────
        if domestic_section:
            lines.append("🇨🇳 国产厂商动态（产品 + 商业化硬数据）")
            for item in domestic_section:
                lines.extend(_format_item(item))
            lines.append("")

        # ── AI应用层 ─────────────────────────────────────────────────────
        lines.append("🚀 AI应用层")
        for item in app_section:
            lines.extend(_format_item(item))
        lines.append("")

        # ── 基座模型研究（恒宇重点关注:头部公司技术细节）─────────────────
        if base_section:
            lines.append("🧪 基座模型研究")
            for item in base_section:
                lines.extend(_format_item(item))
            lines.append("")

        # ── 金融/资本市场动态 ─────────────────────────────────────────────
        if finance_section:
            lines.append("💹 金融/资本市场")
            for item in finance_section:
                lines.extend(_format_item(item))
            lines.append("")

        # ── 其他动态 ─────────────────────────────────────────────────────
        if other_section:
            lines.append("📬 其他动态")
            for item in other_section:
                lines.extend(_format_item(item))

        total = len(domestic_section) + len(app_section) + len(base_section) + len(finance_section) + len(other_section)
        lines.extend([
            "━" * 28,
            f"（共 {total} 条，国产厂商 {len(domestic_section)} 条，AI应用层 {len(app_section)} 条，"
            f"基座模型 {len(base_section)} 条，"
            f"金融 {len(finance_section)} 条）",
            "📡 来源：OpenAI/Anthropic/DeepMind/Meta/DeepSeek/Qwen/GLM 官方 | "
            "PH | HN | TechCrunch | a16z | Latent Space | The Batch 等",
        ])

        return "\n".join(lines)


if __name__ == "__main__":
    # 简单自测
    formatter = DigestFormatter()
    sample = [
        {"title": "Arc for Mac 3.0 发布", "url": "https://example.com", "snippet": "新版界面大幅更新", "label": "PH"},
        {"title": "Nvidia CEO Jensen Huang 出售股票 1.2 亿美元", "url": "https://example.com/2", "snippet": "SEC 文件披露", "label": "高管交易"},
        {"title": "Claude 4.6 发布", "url": "https://example.com/3", "snippet": "性能大幅提升", "label": "动态"},
    ]
    print(formatter.format(sample, "2026-05-18"))