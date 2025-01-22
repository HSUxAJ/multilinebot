from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 定義多個 Bot 的憑證
BOTS = {
    "U1130a755f844329337100a89b97fba31": {
        "access_token": "b4VDCmYuaqw5q/N4G4LF3/SB5b/UP68+W3YNwXJh7q2CQEmIkpdIGFAoMs4GlxlO3NIDoeiOe4ShtfTz474Uz1wceGW2C9aBPu5cYYVbXDiwNzNWCFh93FhGDnfxkwGzYadARXczmXr9xqNLgy8bHAdB04t89/1O/w1cDnyilFU=",
        "secret": "68d83db85f175aa513b472f2462861ae",
    },
    "U2bf30bd527482d2fdd8a708edd387d3b": {
        "access_token": "ipQeI2XS6TarIKzoSgAqxTTU5NNw0QlRLoJ2pa4F7YF2neW1OHFOy0UIzzgCyFuG2MqM5j2bYM05yj6fy+B3l7D8jIAjBzfR5t5v2/I5ujt33aQFcNuIaCXaMNhA3iL8fQQwy1H4j9Nm84AU9n7phwdB04t89/1O/w1cDnyilFU=",
        "secret": "1065a1fcc79ad249ff83be16c5e89b69",
    },
}

@app.route("/webhook", methods=["POST"])
def webhook():
    # 從請求中獲取 Channel ID
    body = request.get_json()
    print(body)
    channel_id = body.get("destination")  # "destination" 是 Webhook 的目標 ID

    if channel_id not in BOTS:
        return "Invalid Channel ID", 400

    # 初始化對應的 Bot API 和 Handler
    bot_config = BOTS[channel_id]
    line_bot_api = LineBotApi(bot_config["access_token"])
    handler = WebhookHandler(bot_config["secret"])

    # 處理事件
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        reply_text = f"你傳送了：{event.message.text}"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_text)
        )

    # 驗證並處理 Webhook
    signature = request.headers["X-Line-Signature"]
    try:
        handler.handle(request.get_data(as_text=True), signature)
    except Exception as e:
        print(f"Error: {e}")
        return "Error", 500

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
