from flask import Flask, request, jsonify
import requests
import os
import socket

bot = Flask(__name__)

# 从环境变量读取配置信息
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
WORKFLOW_FILE = os.getenv("WORKFLOW_FILE")
SSH_HOST = os.getenv("SSH_HOST")
SSH_PORT = int(os.getenv("SSH_PORT", 22))

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

# 检查SSH主机的TCP端口连通性
def check_ssh_port():
    try:
        with socket.create_connection((SSH_HOST, SSH_PORT), timeout=5):
            print("SSH 端口连通")
            return True
    except socket.error:
        print("SSH 端口不通")
        return False

# 处理Webhook的路由
@bot.route('/webhook', methods=['POST'])
def handle_webhook():
    # 输出接收到的Body数据，便于调试
    payload = request.data.decode('utf-8')
    print(f"接收到的Body: {payload}")

    # 检查SSH端口状态
    ssh_status = check_ssh_port()

    # 只有当SSH端口连通时才触发GitHub Action
    if ssh_status:
        print("SSH 端口连通，触发GitHub Action...")
        trigger_github_action()
    else:
        print("SSH 端口不通，不触发GitHub Action")
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # 检查必要的环境变量是否设置
    if not all([GITHUB_REPO, GITHUB_TOKEN, WORKFLOW_FILE, SSH_HOST]):
        print("请确保所有必要的环境变量都已设置")
    else:
        # 启动 Flask 应用，监听端口 5000
        bot.run(debug=False, host='0.0.0.0', port=5000)
