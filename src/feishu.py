import requests
import json
from config import FEISHU_WEBHOOK_URL, FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_CHAT_ID


def send_webhook(content: str) -> bool:
    """群机器人 Webhook 方式（推荐，最简单）"""
    if not FEISHU_WEBHOOK_URL:
        print("[Feishu] 未配置 FEISHU_WEBHOOK_URL，跳过发送")
        return False

    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "🤖 AI 情报日报"},
                "template": "blue",
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content[:4000],  # 飞书卡片单块上限
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {"tag": "plain_text", "content": "查看更多 →"},
                            "url": "https://www.producthunt.com",
                            "type": "default",
                        }
                    ],
                },
            ],
        },
    }

    try:
        resp = requests.post(
            FEISHU_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15,
        )
        data = resp.json()
        if data.get("code") == 0 or data.get("StatusCode") == 0:
            print("[Feishu] Webhook 发送成功")
            return True
        else:
            print(f"[Feishu] Webhook 返回错误: {data}")
            return False
    except Exception as e:
        print(f"[Feishu] Webhook 发送失败: {e}")
        return False


def _get_app_token() -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET,
    }, timeout=10)
    return resp.json().get("tenant_access_token", "")


def send_app_message(content: str) -> bool:
    """飞书应用方式（需要 App ID + Secret）"""
    if not all([FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_CHAT_ID]):
        return False
    try:
        token = _get_app_token()
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
        payload = {
            "receive_id": FEISHU_CHAT_ID,
            "msg_type": "text",
            "content": json.dumps({"text": content}),
        }
        resp = requests.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=15,
        )
        ok = resp.json().get("code") == 0
        print(f"[Feishu] App 消息{'成功' if ok else '失败'}: {resp.json().get('msg')}")
        return ok
    except Exception as e:
        print(f"[Feishu] App 消息发送失败: {e}")
        return False


def send(content: str) -> bool:
    """优先 Webhook，失败则尝试 App 方式"""
    if FEISHU_WEBHOOK_URL:
        return send_webhook(content)
    return send_app_message(content)
