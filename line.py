from linebot import LineBotApi
from linebot.models import TextSendMessage

CHANNEL_ACCESS_TOKEN = ""

def line_bot(value):
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.broadcast(TextSendMessage(text = value))



