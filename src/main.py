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

import argparse, sys, os
from datetime import datetime

# 确保 src 目录在 path 中
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from searcher import NewsSearcher
from formatter import DigestFormatter
from feishu import FeishuSender
from config import CONFIG


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

    # 2. 去重 + 过滤
    seen, items = set(), []
    for item in raw_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            items.append(item)
    log(f"  → 去重后: {len(items)} 条")

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
    log("✅ 发送成功" if ok else "❌ 发送失败")


if __name__ == "__main__":
    main()
