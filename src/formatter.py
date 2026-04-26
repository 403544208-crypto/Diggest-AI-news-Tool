import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_ITEMS_IN_REPORT, MIN_AI_RELEVANCE_SCORE


def _score_and_filter(items: list[dict]) -> list[dict]:
    """用关键词快速预过滤，减少 API 调用"""
    ai_keywords = {
        "ai", "llm", "gpt", "claude", "gemini", "mistral", "agent",
        "generative", "machine learning", "deep learning", "neural",
        "openai", "anthropic", "hugging face", "langchain", "copilot",
        "chatbot", "artificial intelligence", "model", "inference",
        "product hunt", "saas", "startup", "launch", "tool",
    }
    scored = []
    for item in items:
        text = (item.get("title", "") + " " + item.get("summary", "")).lower()
        hits = sum(1 for kw in ai_keywords if kw in text)
        score = min(100, hits * 12 + item.get("weight", 0) * 3)
        if score >= MIN_AI_RELEVANCE_SCORE:
            item["relevance_score"] = score
            scored.append(item)
    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    return scored[:MAX_ITEMS_IN_REPORT * 2]


def _build_prompt(items: list[dict]) -> str:
    news_lines = []
    for i, item in enumerate(items, 1):
        news_lines.append(
            f"{i}. [{item['source']}] {item['title']}\n"
            f"   URL: {item.get('url', 'N/A')}\n"
            f"   摘要: {item.get('summary', '')[:200]}\n"
        )
    news_text = "\n".join(news_lines)

    return f"""你是一位 AI 行业分析师，负责每日整理 AI 应用层的重要动态。

以下是今日抓取的原始新闻列表（来自 Product Hunt、TechCrunch、VentureBeat 等）：

{news_text}

请完成以下任务：
1. 筛选出最具价值的 {MAX_ITEMS_IN_REPORT} 条（优先：新产品发布、功能更新、融资、AI 应用层 ≥60%）
2. 对每条新闻写 1-2 句中文简评（点明亮点/影响）
3. 输出格式严格按照下面的 Markdown 模板，不要添加额外内容：

---
## 🤖 AI 情报日报 · {{日期}}

### 🏆 Product Hunt 精选
{{如有 PH 内容则列出，格式如下}}
- **[产品名](URL)** — 简评（1句）

### 🚀 新品发布 & 功能更新
- **[标题](URL)** — 简评
...

### 💰 融资 & 商业动态
- **[标题](URL)** — 简评
...

### 📌 技术 & 行业观察
- **[标题](URL)** — 简评
...

> 数据来源：Product Hunt · TechCrunch · VentureBeat · The Verge · HuggingFace
---

今天日期：{__import__('datetime').datetime.now().strftime('%Y年%m月%d日')}"""


def format_news(items: list[dict]) -> str:
    if not items:
        return "今日暂无符合条件的 AI 新闻。"

    filtered = _score_and_filter(items)
    print(f"[Formatter] 过滤后 {len(filtered)} 条，调用 Claude 生成摘要...")

    if not ANTHROPIC_API_KEY:
        return _fallback_format(filtered)

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2048,
            messages=[{"role": "user", "content": _build_prompt(filtered)}],
        )
        return message.content[0].text
    except Exception as e:
        print(f"[Formatter] Claude API 失败，使用纯文本格式: {e}")
        return _fallback_format(filtered)


def _fallback_format(items: list[dict]) -> str:
    from datetime import datetime
    lines = [f"## 🤖 AI 情报日报 · {datetime.now().strftime('%Y年%m月%d日')}\n"]
    for item in items[:MAX_ITEMS_IN_REPORT]:
        title = item.get("title", "无标题")
        url = item.get("url", "")
        source = item.get("source", "")
        summary = item.get("summary", "")[:100]
        lines.append(f"- **[{title}]({url})** [{source}]\n  {summary}\n")
    return "\n".join(lines)
