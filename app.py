import config  # 先ほど作成したconfig.pyをインポート
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    process.env.LINE_CHANNEL_ACCESS_TOKEN
)  # cyclicで設定したチャネルアクセストークン
handler = WebhookHandler(
    process.env.LINE_CHANNEL_SECRET
)  # cyclicで設定したチャネルシークレット


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == "00000000000000000000000000000000":
        return

    if event.message.text == "test":
        text = "testコマンドが実行されました\n"+event.source.user_id
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=text)
        )

    print(event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    app.run(host="localhost", port=8000)  # ポート番号を8000に指定
