from telegram.ext import Updater, MessageHandler, Filters
import requests
import os

# 从环境变量读取配置信息
KEYWORDS = os.getenv("KEYWORDS", "").split(",")  # 以逗号分隔的关键词列表
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
WORKFLOW_FILE = os.getenv("WORKFLOW_FILE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# 触发GitHub Action的函数
def trigger_github_action():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "ref": "main"  # 指定要触发workflow的分支
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 204:
        print("GitHub Action 触发成功！")
    else:
        print(f"触发失败: {response.status_code}, {response.text}")

# 处理接收到的Telegram消息
def handle_message(update, context):
    message = update.message.text
    if any(keyword in message for keyword in KEYWORDS):
        print("检测到关键词，触发GitHub Action...")
        trigger_github_action()

def main():
    # 检查是否所有环境变量都存在
    if not all([TELEGRAM_TOKEN, GITHUB_REPO, GITHUB_TOKEN, WORKFLOW_FILE]):
        print("请确保所有必要的环境变量都已设置")
        return
    
    # 初始化Updater
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    
    # 添加消息处理器
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    # 启动Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
