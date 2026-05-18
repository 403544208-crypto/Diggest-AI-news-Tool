"""
formatter.py
AI 情报格式化器

按照恒宇要求的格式输出：
  - AI应用层 ≥60%（YC / PH / GH / 新品 / 融资 / 工具 标签）
  - 金融/资本市场动态（金融、高管交易、并购、IPO 标签）
  - 来源推荐 ≥1条
  - 其他动态 补足至 20 条
"""

from config import DIGEST_CONFIG


APP_LABELS = {"PH", "YC", "GH", "新品", "融资", "工具"}
FINANCE_LABELS = {"金融", "高管交易", "并购", "IPO"}


def guess_category(item: dict) -> str:
    """判断是 AI应用层、金融/资本市场 还是 其他动态"""
    if item.get("label") in FINANCE_LABELS:
        return "finance"
    if item.get("label") in APP_LABELS:
        return "app"
    # 关键词二次判断
    text = (item.get("title", "") + " " + item.get("snippet", "")).lower()
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
        """
        target = self.cfg["total_target"]

        # 分类
        app_items   = [it for it in items if guess_category(it) == "app"]
        finance_items = [it for it in items if guess_category(it) == "finance"]
        other_items = [it for it in items if guess_category(it) == "other"]

        # 确保 AI应用层 ≥60%
        app_count = max(len(app_items), int(target * self.cfg["app_layer_ratio"]))

        # 金融/资本市场：全部保留，最多占 5 条
        finance_count = min(len(finance_items), 5)

        # 取条
        app_section     = app_items[:app_count]
        finance_section = finance_items[:finance_count]
        cap_other       = target - len(app_section) - len(finance_section)
        other_section   = other_items[:max(0, cap_other)]

        # 编号计数器
        def enumerate_with_offset(section, start=1):
            return enumerate(section, start)

        lines = [
            f"🤖 AI每日情报 · {date}",
            "━" * 28,
        ]

        # ── 来源推荐（第一条 AI应用层）──────────────────────────────────
        if app_section:
            first = app_section[0]
            lines.extend([
                f"📦 来源推荐",
                f"【{first['label']}】 {first['title']}",
                f"  {first.get('snippet', '')[:100]}",
                f"  🔗 {first.get('url', '')}",
                "",
            ])

        # ── AI应用层 ─────────────────────────────────────────────────────
        lines.append("🚀 AI应用层")
        for item in app_section[1:]:
            lines.append(f"【{item['label']}】 {item['title']}")
            if item.get("snippet"):
                lines.append(f"  📌 {item['snippet'][:100]}")
            lines.append(f"  🔗 {item.get('url', '')}")
        lines.append("")

        # ── 金融/资本市场动态 ─────────────────────────────────────────────
        if finance_section:
            lines.append("💹 金融/资本市场")
            for item in finance_section:
                lines.append(f"【{item['label']}】 {item['title']}")
                if item.get("snippet"):
                    lines.append(f"  📌 {item['snippet'][:100]}")
                lines.append(f"  🔗 {item.get('url', '')}")
            lines.append("")

        # ── 其他动态 ─────────────────────────────────────────────────────
        if other_section:
            lines.append("📬 其他动态")
            num = len(app_section) + len(finance_section) + 1
            for item in other_section:
                lines.append(f"【{item['label']}】 {item['title']}")
                if item.get("snippet"):
                    lines.append(f"  📌 {item['snippet'][:100]}")
                lines.append(f"  🔗 {item.get('url', '')}")
                num += 1

        total = len(app_section) + len(finance_section) + len(other_section)
        lines.extend([
            "━" * 28,
            f"（共 {total} 条，AI应用层 {len(app_section)} 条，"
            f"金融 {len(finance_section)} 条）",
            "来源：YC / PH / HN / TechCrunch / a16z / 金融媒体 等",
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