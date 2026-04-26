#!/usr/bin/env python3
"""
AI News Bot — 入口文件
用法：
  python src/main.py          # 立即运行一次
  python src/main.py --cron   # 按 config.SEND_HOUR 定时运行
"""

import sys
import os
import schedule
import time

# 确保根目录在 path 中（支持从任意位置运行）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.searcher import collect_news
from src.formatter import format_news
from src import feishu
from config import SEND_HOUR


def run_once():
    print("=" * 50)
    print("[Main] 开始抓取 AI 新闻...")
    items = collect_news()

    print("[Main] 格式化报告...")
    report = format_news(items)

    print("[Main] 发送到飞书...")
    success = feishu.send(report)

    print(f"[Main] 完成，发送{'成功' if success else '失败'}")
    print("=" * 50)
    return report


def run_scheduled():
    print(f"[Main] 定时模式启动，每天 {SEND_HOUR:02d}:00 发送")
    schedule.every().day.at(f"{SEND_HOUR:02d}:00").do(run_once)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    if "--cron" in sys.argv:
        run_scheduled()
    else:
        run_once()
