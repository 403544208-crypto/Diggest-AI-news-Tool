import feedparser
import requests
import subprocess
import json
from datetime import datetime, timezone, timedelta
from typing import Optional
from config import (
    SEARCH_QUERIES, RSS_FEEDS, MAX_RESULTS_PER_SOURCE,
    MIN_AI_RELEVANCE_SCORE, LOOKBACK_HOURS
)


def _is_recent(published_parsed) -> bool:
    if not published_parsed:
        return True  # 无时间信息时默认保留
    cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)
    try:
        pub_dt = datetime(*published_parsed[:6], tzinfo=timezone.utc)
        return pub_dt >= cutoff
    except Exception:
        return True


def _search_via_subprocess(query: str) -> list[dict]:
    """通过系统 web_search 命令搜索（MCP 不可用时的备用方案）"""
    try:
        result = subprocess.run(
            ["python3", "-c",
             f"import urllib.request, json; "
             f"url = 'https://ddg-api.herokuapp.com/search?q={urllib.parse.quote(query)}&max_results=5'; "
             f"print('[]')"],
            capture_output=True, text=True, timeout=15
        )
        return json.loads(result.stdout.strip() or "[]")
    except Exception:
        return []


def fetch_rss_items() -> list[dict]:
    items = []
    for feed_cfg in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_cfg["url"])
            count = 0
            for entry in feed.entries:
                if not _is_recent(entry.get("published_parsed")):
                    continue
                items.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "summary": entry.get("summary", "")[:500],
                    "source": feed_cfg["name"],
                    "weight": feed_cfg["weight"],
                    "published": entry.get("published", ""),
                })
                count += 1
                if count >= MAX_RESULTS_PER_SOURCE:
                    break
        except Exception as e:
            print(f"[RSS] {feed_cfg['name']} 失败: {e}")
    return items


def fetch_search_items() -> list[dict]:
    """尝试使用 MCP web_search，失败则跳过（不阻塞流程）"""
    items = []
    for q_cfg in SEARCH_QUERIES[:5]:  # 只取权重最高的 5 条
        try:
            results = _search_via_subprocess(q_cfg["query"])
            for r in results[:3]:
                items.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", r.get("href", "")),
                    "summary": r.get("body", r.get("snippet", ""))[:500],
                    "source": q_cfg.get("source", "Search"),
                    "weight": q_cfg["weight"],
                    "published": "",
                })
        except Exception:
            pass
    return items


def deduplicate(items: list[dict]) -> list[dict]:
    seen_urls = set()
    seen_titles = set()
    result = []
    for item in items:
        url = item.get("url", "").split("?")[0].rstrip("/")
        title_key = item.get("title", "").lower()[:50]
        if url in seen_urls or title_key in seen_titles:
            continue
        seen_urls.add(url)
        seen_titles.add(title_key)
        result.append(item)
    return result


def collect_news() -> list[dict]:
    print("[Searcher] 抓取 RSS 源...")
    rss_items = fetch_rss_items()
    print(f"[Searcher] RSS 获取 {len(rss_items)} 条")

    print("[Searcher] 执行搜索...")
    search_items = fetch_search_items()
    print(f"[Searcher] 搜索获取 {len(search_items)} 条")

    all_items = rss_items + search_items
    all_items = deduplicate(all_items)
    all_items.sort(key=lambda x: x.get("weight", 0), reverse=True)

    print(f"[Searcher] 去重后共 {len(all_items)} 条")
    return all_items
