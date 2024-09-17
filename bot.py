from flask import Flask, request, jsonify
import requests
import os

bot = Flask(__name__)

# 从环境变量读取配置信息
KEYWORDS = os.getenv("KEYWORDS", "").split(",")  # 以逗号分隔的关键词列表
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
WORKFLOW_FILE = os.getenv("WORKFLOW_FILE")

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

# 处理Webhook的路由
@bot.route('/webhook', methods=['POST'])
def handle_webhook():
    # 获取 webhook 请求的内容
    payload = request.data.decode('utf-8')

    # 输出接收到的Body数据，便于调试
    print(f"接收到的Body: {payload}")

    # 检查是否包含关键词
    if any(keyword in payload for keyword in KEYWORDS):
        print("检测到关键词，触发GitHub Action...")
        trigger_github_action()
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # 检查必要的环境变量是否设置
    if not all([GITHUB_REPO, GITHUB_TOKEN, WORKFLOW_FILE]):
        print("请确保所有必要的环境变量都已设置")
    else:
        # 启动 Flask 应用，监听端口 5000
        bot.run(debug=False, host='0.0.0.0', port=5000)
