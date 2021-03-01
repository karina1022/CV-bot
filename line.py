from linebot import LineBotApi
from linebot.models import TextSendMessage

CHANNEL_ACCESS_TOKEN = "OrCb+t6DK58FLZyYkx24iM5Zh7ngO5wgc3vwB3BulAW7mvnBH1Skb9n8nC/P4lp00uxRiUMtTH1USGGzyexg1pWe7Wh35lvwft5c/r1zKSRoMncSGEH+MSafIf7ebI4zru/q1VhZUsmlgFvk5jma8gdB04t89/1O/w1cDnyilFU="

def line_bot(value):
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.broadcast(TextSendMessage(text = value))



