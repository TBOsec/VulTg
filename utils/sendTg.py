import httpx

import utils.globalVariable as glv

glv._init()
# 发送的企微机器人
def send_qywx(send_data):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4495.0 Safari/537.36"
    # 机器人地址
    webhook_addr = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx-xxxx"

    # 机器人header头部
    tx_headers = {
        "User-Agent": user_agent,
        "Content-Type": "application/json",
    }
    dirs = glv.get("dirs")
    try:
        # with httpx.Client() as client:
        r = httpx.post(url=webhook_addr, headers=tx_headers, json=send_data)
        with open(dirs + "tx_history.log", "a") as f:
            f.writelines(r.text + "\n")

    except:
        exit()
