"""
formatter.py
AI 情报格式化器

按照恒宇要求的格式输出：
  - AI应用层 ≥60%（YC / PH / GH / 新品 / 融资 / 工具 标签）
  - 来源推荐 ≥1条
  - 其他动态 补足至 20 条
"""

from config import DIGEST_CONFIG


APP_LABELS = {"PH", "YC", "GH", "新品", "融资", "工具"}


def guess_category(item: dict) -> str:
    """判断是 AI应用层 还是 其他动态"""
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
        app_items = [it for it in items if guess_category(it) == "app"]
        other_items = [it for it in items if guess_category(it) == "other"]

        # 确保 AI应用层 ≥60%
        app_count = max(len(app_items), int(target * self.cfg["app_layer_ratio"]))
        app_section = app_items[:app_count]
        other_section = other_items[:max(0, target - len(app_section))]

        lines = [
            f"🤖 AI每日情报 · {date}",
            "━" * 28,
            "",
            "🚀 AI应用层",
        ]

        # 来源推荐（第一条 AI应用层作为来源推荐）
        if app_section:
            first = app_section[0]
            lines.extend([
                f"📦 来源推荐",
                f"【{first['label']}】 {first['title']}",
                f"  {first.get('snippet', '')[:100]}",
                f"  🔗 {first.get('url', '')}",
                "",
            ])

        # 逐条列出 AI应用层（从第二条开始）
        for i, item in enumerate(app_section[1:], 1):
            lines.append(f"{i}. 【{item['label']}】 {item['title']}")
            if item.get("snippet"):
                lines.append(f"   📌 {item['snippet'][:80]}")
            lines.append(f"   🔗 {item.get('url', '')}")

        # 其他动态
        if other_section:
            lines.append("")
            lines.append("📬 其他动态")
            for i, item in enumerate(other_section, len(app_section)):
                lines.append(f"{i}. 【{item['label']}】 {item['title']}")
                if item.get("snippet"):
                    lines.append(f"   📌 {item['snippet'][:80]}")
                lines.append(f"   🔗 {item.get('url', '')}")

        lines.extend([
            "",
            "━" * 28,
            f"（共 {len(app_section) + len(other_section)} 条，"
            f"AI应用层 {len(app_section)} 条）",
            "来源：YC / PH / HN / TechCrunch / a16z 等",
        ])

        return "\n".join(lines)


if __name__ == "__main__":
    # 简单自测
    formatter = DigestFormatter()
    sample = [
        {"title": "Arc for Mac 3.0 发布", "url": "https://example.com", "snippet": "新版界面大幅更新", "label": "PH"},
        {"title": "Claude 4.6 发布", "url": "https://example.com/2", "snippet": "性能大幅提升", "label": "动态"},
    ]
    print(formatter.format(sample, "2026-04-26"))
