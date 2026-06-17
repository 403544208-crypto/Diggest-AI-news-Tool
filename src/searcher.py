"""
searcher.py
多来源 AI 新闻搜索

支持两种调用方式：
  1. 连接到本地 OpenClaw MCP 端口（网关同机部署时）
  2. 通过 subprocess 调用 npx matrix-mcp（通用方式）

优先使用方式 1，失败后回退到方式 2。
"""

import subprocess, json, time, random, os, sys
import re
import difflib
from urllib.request import Request, urlopen
from urllib.error import URLError

LOCAL_MCP = "http://localhost:3100/mcp/batch_web_search"
TIMEOUT = 25  # 秒


def _search_via_mcp_http(queries: list[tuple[str, int]]) -> list[dict]:
    """
    通过 OpenClaw 本地 MCP HTTP 端口搜索。
    queries: [(query, num_results), ...]
    """
    payload = json.dumps({
        "queries": [
            {"query": q, "numResults": n, "dataRange": "m"}
            for q, n in queries
        ]
    }).encode("utf-8")

    req = Request(LOCAL_MCP, data=payload, headers={
        "Content-Type": "application/json",
    }, method="POST")

    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read())
            results = []
            for batch in data.get("results", []):
                for r in batch.get("results", []):
                    if r.get("title") and r.get("url"):
                        results.append(r)
            return results
    except (URLError, OSError, json.JSONDecodeError):
        return []


def _search_via_subprocess(queries: list[tuple[str, int]]) -> list[dict]:
    """
    通过 npx matrix-mcp 子进程搜索（备用方案）。
    """
    results = []
    for query, num in queries:
        try:
            r = subprocess.run(
                ["npx", "-y", "matrix-mcp", "batch_web_search",
                 query, str(num)],
                capture_output=True, text=True,
                timeout=30, cwd="/workspace"
            )
            try:
                data = json.loads(r.stdout)
                for batch in data.get("results", []):
                    for item in batch.get("results", []):
                        if item.get("title") and item.get("url"):
                            results.append(item)
            except json.JSONDecodeError:
                pass
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        time.sleep(1)  # 避免频率限制
    return results


def _guess_label(item: dict) -> str:
    """根据标题/摘要关键词自动打标签"""
    text = (item.get("title", "") + " " + item.get("snippet", "")).lower()
    if "product hunt" in text or "ph" in text:
        return "PH"
    if "github" in text or "open source" in text or "stars:" in text:
        return "GH"
    if "yc " in text or "y combinator" in text or "demo day" in text:
        return "YC"
    if any(k in text for k in ["raise", "funding", "series", "round", "invest"]):
        return "融资"
    if any(k in text for k in ["open source", "github", "library", "framework"]):
        return "工具"
    # ── 基座模型研究关键词（最高优先级之一）──────────────
    if any(k in text for k in [
        "arxiv", "paper", "research", "technical report", "benchmark",
        "swe-bench", "mmlu", "arc-agi", "neurips", "icml", "iclr", "acl",
        "pretraining", "pre-training", "fine-tuning", "rlhf", "rlaif",
        "reasoning model", "test-time compute", "scaling", "moe",
        "long context", "attention", "transformer", "state space", "mamba",
        "diffusion model", "architecture", "sparse", "mixture of experts",
        "synthetic data", "post-training", "rl on",
        "openai", "anthropic", "deepmind", "meta ai", "fair", "mistral", "xai",
        "gpt-", "claude", "gemini", "llama", "grok", "qwen", "deepseek",
        "glm-", "kimi", "doubao", "ernie", "wenxin", "minimax",
        "interpretability", "alignment", "evaluation"
    ]):
        return "基模"
    if any(k in text for k in ["launch", "release", "new", "introducing"]):
        return "新品"
    return "动态"


def _normalize_title(title: str) -> str:
    """规范化标题：去标点、转小写、去多余空白"""
    if not title:
        return ""
    t = title.lower()
    t = re.sub(r"[^\w\s\u4e00-\u9fff]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _title_similarity(a: str, b: str) -> float:
    """计算两个标题的相似度（0-1）"""
    na, nb = _normalize_title(a), _normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    return difflib.SequenceMatcher(None, na, nb).ratio()


def dedup_by_title(items: list[dict], threshold: float = 0.75) -> list[dict]:
    """按标题相似度去重，保留先出现的（相似度 >threshold 视为同一条）"""
    kept: list[dict] = []
    for it in items:
        dup = False
        for k in kept:
            if _title_similarity(it.get("title", ""), k.get("title", "")) >= threshold:
                dup = True
                break
        if not dup:
            kept.append(it)
    return kept


class NewsSearcher:
    def __init__(self):
        self.used_local = False

    def fetch_all(self, queries: list[tuple[str, int]], max_per_query: int = 8
                  ) -> list[dict]:
        """
        并发从多个查询词抓取结果，自动打标签。
        返回: [{title, url, snippet, source, label}, ...]
        """
        # 用本地 MCP（最快）
        raw = _search_via_mcp_http(queries)
        if raw:
            self.used_local = True
        else:
            # 回退到 subprocess
            raw = _search_via_subprocess(queries)

        out = []
        for item in raw:
            out.append({
                "title": item.get("title", "").strip(),
                "url": item.get("url", ""),
                "snippet": item.get("snippet", "")[:150].strip(),
                "source": item.get("source", "web"),
                "label": _guess_label(item),
            })
        return out


if __name__ == "__main__":
    # 快速测试
    s = NewsSearcher()
    items = s.fetch_all([
        ("AI startup Product Hunt trending 2026", 5),
        ("GitHub trending AI open source 2026", 5),
    ])
    print(f"获取到 {len(items)} 条")
    for it in items[:3]:
        print(f"  [{it['label']}] {it['title']}")
        print(f"  {it['url']}")
