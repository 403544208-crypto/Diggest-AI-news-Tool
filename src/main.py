"""
AI News Digest Bot
每日自动抓取 AI 情报，发送至飞书

依赖:
  pip install requests python-dotenv

运行:
  python src/main.py          # 单次执行
  python src/main.py --watch   # 监听模式（开发用）
  python src/main.py --test    # 发送测试消息到飞书

定时任务（Linux crontab）:
  0 9 * * * cd /path/to/ai-news-bot && python src/main.py >> logs/cron.log 2>&1
"""

import argparse, sys, os, json
from datetime import datetime, timedelta

# 确保 src 目录在 path 中
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from searcher import NewsSearcher, dedup_by_title, _title_similarity
from formatter import DigestFormatter
from feishu import FeishuSender
from config import CONFIG, DIGEST_CONFIG


def _load_history(path: str, window_days: int) -> list[dict]:
    """读取历史发布记录，返回在窗口期内的条目列表"""
    if not os.path.exists(path):
        return []
    try:
        records = json.loads(open(path).read())
    except Exception:
        return []
    cutoff = datetime.now() - timedelta(days=window_days)
    active = []
    for rec in records:
        try:
            ts = datetime.fromisoformat(rec.get("ts", ""))
            if ts >= cutoff:
                active.append(rec)
        except Exception:
            pass
    return active


def _save_history(path: str, items: list[dict]):
    """将本次推送的条目追加写入历史记录（保存 url + title 用于相似度查重）"""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    now = datetime.now().isoformat()
    entries = [
        {"url": it["url"], "title": it.get("title", ""), "ts": now}
        for it in items
        if it.get("url")
    ]
    history = []
    if os.path.exists(path):
        try:
            history = json.loads(open(path).read())
        except Exception:
            pass
    history.extend(entries)
    with open(path, "w") as f:
        json.dump(history, f, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="AI 每日情报推送机器人")
    parser.add_argument("--test", action="store_true", help="发送测试消息")
    parser.add_argument("--dry", action="store_true", help="仅生成内容，不发送")
    parser.add_argument("--watch", action="store_true", help="监听模式，每小时检查一次")
    parser.add_argument("--quiet", action="store_true", help="静默模式，减少输出")
    args = parser.parse_args()

    log = print if not args.quiet else lambda *a, **k: None

    # ── 测试模式 ──────────────────────────────────────────
    if args.test:
        sender = FeishuSender()
        ok = sender.send_test()
        print("✅ 测试消息发送成功" if ok else "❌ 发送失败")
        return

    # ── 主流程 ────────────────────────────────────────────
    log(f"[{datetime.now().strftime('%H:%M:%S')}] 开始抓取 AI 情报...")

    # 1. 搜索
    searcher = NewsSearcher()
    raw_items = searcher.fetch_all(CONFIG["search_queries"], max_per_query=8)
    log(f"  → 原始结果: {len(raw_items)} 条")

    # 2. 多层去重
    #    第一层：URL 去重（同一 session 内）
    #    第二层：URL 历史去重（窗口期内已推送过）
    #    第三层：标题相似度去重（同一条新闻的不同来源报道）
    history_file    = DIGEST_CONFIG.get("history_file", "data/published_history.json")
    window_days     = DIGEST_CONFIG.get("dedup_window_days", 7)
    title_threshold = DIGEST_CONFIG.get("dedup_title_threshold", 0.75)

    history  = _load_history(history_file, window_days)
    recent_urls   = {r["url"] for r in history if r.get("url")}
    recent_titles = [r.get("title", "") for r in history if r.get("title")]
    log(f"  → 历史窗口期({window_days}d)内: URL {len(recent_urls)} 条，标题 {len(recent_titles)} 条")

    seen, items = set(), []
    for item in raw_items:
        url = item.get("url", "")
        title = item.get("title", "")
        if not url or url in seen:
            continue
        if url in recent_urls:
            continue
        # 标题相似度查重
        is_dup = any(
            _title_similarity(title, t) >= title_threshold
            for t in recent_titles
        )
        if is_dup:
            continue
        seen.add(url)
        items.append(item)
    log(f"  → URL+标题 去重后: {len(items)} 条")

    # 3. 进一步按标题去重（防止一次抓取中重复）
    items = dedup_by_title(items, threshold=title_threshold)
    log(f"  → 标题相似度去重后: {len(items)} 条")

    # 3. 格式化
    formatter = DigestFormatter()
    digest = formatter.format(items, date=datetime.now().strftime("%Y-%m-%d"))
    log(f"  → 格式化完成，字数: {len(digest)}")

    # 4. 输出或发送
    if args.dry:
        print(digest)
        return

    sender = FeishuSender()
    ok = sender.send(digest)

    # 推送成功后才写入历史记录
    if ok:
        _save_history(history_file, items)
        log("✅ 发送成功，已记录历史")


if __name__ == "__main__":
    main()
