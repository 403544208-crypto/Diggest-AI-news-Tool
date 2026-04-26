"""
feishu.py
飞书消息发送器

支持两种模式：
  1. Webhook（极简，推荐）—— 只需一个 Webhook URL
  2. 开放平台 App（更稳定）—— 需要 App ID + App Secret

在 config.py 中填入对应凭证即可。
"""

import json, logging, os, sys
from urllib.request import Request, urlopen
from urllib.error import URLError
from datetime import datetime

# 尝试导入可选依赖
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger("feishu")


# ── Webhook 发送 ────────────────────────────────────────────────────────────

def send_via_webhook(webhook_url: str, text: str) -> bool:
    """
    通过飞书自定义机器人 Webhook 发送文本消息。
    文档：https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkj
    """
    payload = json.dumps({
        "msg_type": "text",
        "content": {"text": text},
        # "secret": "xxx",  # 加签密钥（可选）
    }).encode("utf-8")

    req = Request(webhook_url, data=payload, headers={
        "Content-Type": "application/json",
    }, method="POST")

    try:
        with urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read())
            if body.get("code") == 0 or body.get("StatusCode") == 0:
                return True
            logger.error(f"飞书返回错误: {body}")
            return False
    except URLError as e:
        logger.error(f"Webhook 请求失败: {e}")
        return False


# ── 开放平台 App 发送 ───────────────────────────────────────────────────────

def get_tenant_access_token(app_id: str, app_secret: str) -> str | None:
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            if data.get("code") == 0:
                return data["tenant_access_token"]
    except URLError as e:
        logger.error(f"获取 token 失败: {e}")
    return None


def send_via_app(token: str, chat_id: str, text: str) -> bool:
    """
    通过飞书开放平台 API 发送消息到群/用户。
    chat_id: 可以是 open_id / union_id / chat_id
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = json.dumps({
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}),
    }).encode("utf-8")

    req = Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }, method="POST")

    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            if data.get("code") == 0:
                return True
            logger.error(f"App 发送失败: {data}")
            return False
    except URLError as e:
        logger.error(f"App 请求失败: {e}")
        return False


# ── 主类 ────────────────────────────────────────────────────────────────────

class FeishuSender:
    def __init__(self):
        # 延迟导入 config，避免循环
        from config import FEISHU
        self.cfg = FEISHU

    def send(self, text: str) -> bool:
        """
        自动选择方式发送消息。
        优先 Webhook（配置简单），否则用 App 方式。
        """
        webhook = self.cfg.get("webhook_url", "").strip()
        app_id = self.cfg.get("app_id", "").strip()
        app_secret = self.cfg.get("app_secret", "").strip()
        chat_id = self.cfg.get("chat_id", "").strip()

        # 方式 1：Webhook
        if webhook and webhook.startswith("https://"):
            print(f"[Feishu] 使用 Webhook 发送 ({len(text)} 字)")
            return send_via_webhook(webhook, text)

        # 方式 2：开放平台 App
        if app_id and app_secret and chat_id:
            print(f"[Feishu] 使用 App API 发送 ({len(text)} 字)")
            token = get_tenant_access_token(app_id, app_secret)
            if token:
                return send_via_app(token, chat_id, text)
            return False

        # 方式 3：fallback —— 打印到 stdout，供 cron 重定向收集
        print("[Feishu] 未配置飞书，输出到 stdout:")
        print(text[:200], "...")
        return True

    def send_test(self) -> bool:
        """发送测试消息"""
        return self.send(f"🧪 AI情报机器人测试消息\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n✅ 机器人运行正常")


# ── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    sender = FeishuSender()
    ok = sender.send_test()
    print("发送成功" if ok else "发送失败")
