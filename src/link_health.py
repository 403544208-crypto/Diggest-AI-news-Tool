"""
link_health.py
链接健康检查 + 自动修复（恒宇 2026-08-24 反馈：部分 link 404）

原因: MCP 搜索结果返回的 url 字段有时是被截断的 slug (末尾 "-s" / "-" / 空 slug),
title 是完整的但 url 不是,导致 404 / 403。
解决: 拿到 url 后先 HEAD 探测,死的就用标题 site: 限定重新搜替换。
"""

import re
import sys
import json
import threading
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from difflib import SequenceMatcher

LOCAL_MCP = "http://localhost:3100/mcp/batch_web_search"

def _web_search_one(query: str, num: int = 5) -> list[dict]:
    """单条搜索: 优先本地 MCP HTTP, 回退 subprocess npx matrix-mcp。"""
    import subprocess
    try:
        payload = json.dumps({"queries":[{"query":query,"numResults":num,"dataRange":"m"}]}).encode("utf-8")
        req = Request(LOCAL_MCP, data=payload, headers={"Content-Type":"application/json"}, method="POST")
        with urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        out=[]
        for batch in data.get("results",[]):
            for item in batch.get("results",[]):
                if item.get("title") and item.get("url"): out.append(item)
        if out: return out
    except Exception: pass
    try:
        r=subprocess.run(["npx","-y","matrix-mcp","batch_web_search",query,str(num)],capture_output=True,text=True,timeout=30,cwd="/workspace")
        data=json.loads(r.stdout); out=[]
        for batch in data.get("results",[]):
            for item in batch.get("results",[]):
                if item.get("title") and item.get("url"): out.append(item)
        return out
    except Exception: return []


def _title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()


def _check_url_alive(url: str, timeout: int = 6) -> bool:
    """HEAD → GET 双探测。200/2xx/3xx = True。"""
    if not url or not url.startswith(("http://", "https://")):
        return False
    for method in ("HEAD", "GET"):
        try:
            req = Request(url, method=method, headers={
                "User-Agent": "Mozilla/5.0 (compatible; AINewsBot/1.0)"
            })
            with urlopen(req, timeout=timeout) as r:
                if 200 <= r.status < 400:
                    return True
        except Exception:
            continue
    return False


def _looks_truncated(url: str) -> bool:
    """启发式: 末尾是孤立连字符 / 长度太短 → 极可能是占位符。"""
    if re.search(r"-$", url):
        return True
    # 路径段最后一段过短(≤2 字符) 且 以连字符结尾
    try:
        path = urlparse(url).path.rstrip("/")
        if path and path[-1] == "-":
            return True
    except Exception:
        pass
    return False


def _retry_search_for_real_url(title: str, original_url: str, timeout: int = 15) -> str | None:
    """标题正常但 URL 死的: 用 site: 限定 + 标题重搜, 找第一个活的。"""
    if not title:
        return None
    try:
        domain = urlparse(original_url).netloc.replace("www.", "")
    except Exception:
        domain = ""
    query = f'"{title[:60]}"' + (f" site:{domain}" if domain else "")
    candidates = _web_search_one(query, num=5)
    for item in candidates:
        u = item.get("url", "")
        t = item.get("title", "")
        if u and _check_url_alive(u, timeout=5):
            if _title_similarity(t, title) >= 0.55:
                return u
    return None


def fix_dead_urls(items: list[dict], max_fix: int = 10, log=None) -> list[dict]:
    """
    对每条 item 检查 url 死活, 死的用标题重搜修复。
    标记:
      _url_fixed=True  → 已修好
      _url_dead=True   → 修不上, 飞书显示时会加 ⚠️
    """
    out_log = log or (lambda *a, **k: print(*a, file=sys.stderr, **k))
    fixed, still_dead = 0, 0
    for it in items:
        url = it.get("url", "")
        title = it.get("title", "")
        if not url or not title:
            continue
        # 快速过滤: 明显截断的直接进修复, 不浪费一次 HEAD
        if not _looks_truncated(url) and _check_url_alive(url):
            continue
        if fixed >= max_fix:
            it["_url_fixed"] = False
            it["_url_dead"] = True
            still_dead += 1
            continue
        real = _retry_search_for_real_url(title, url)
        if real and real != url:
            it["url"] = real
            it["_url_fixed"] = True
            out_log(f"  🔧 修链接: {url[:55]}... → {real[:55]}...")
            fixed += 1
        else:
            it["_url_fixed"] = False
            it["_url_dead"] = True
            still_dead += 1
            out_log(f"  ⚠️  死链: {url[:60]}...")
    if fixed or still_dead:
        out_log(f"  📊 链接健康: 修复 {fixed} 条, 仍死 {still_dead} 条")
    return items
