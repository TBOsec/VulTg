"""
Created on Mar 9, 2021
@author: TBOsec   
"""
# coding = utf-8
import json
import os
import re
from sys import exit

import httpx

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4495.0 Safari/537.36"
# 机器人地址
webhook_addr = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx-xxxx"
id_url = "https://cloud.tencent.com/announce/ajax"
info_url = "https://cloud.tencent.com/announce/detail/"  # + id

# header头部
getID_headers = {
    "User-Agent": user_agent,
    "Referer": "https://cloud.tencent.com/announce?page=1&categorys=21",
    "Content-Type": "application/json; charset=UTF-8",
    "Origin": "https://cloud.tencent.com",
}

getInfo_headers = {
    "User-Agent": user_agent,
    "Referer": "https://cloud.tencent.com/announce?page=1&categorys=21",
}

# 机器人header头部
tx_headers = {
    "User-Agent": user_agent,
    "Content-Type": "application/json",
}

home = os.environ["HOME"]
dirs = home + "/.config/vul_TG/"
global page_id, total, titles, descriptions, old_total
page_id = []  # 文章ID号
titles = []  # 文章标题
times = []  # 通告时间
descriptions = []  # 漏洞风险
risks = []  # 风险等级


# 获取漏洞ID号
def getID():
    global page_id, total, old_total
    data = {
        "action": "getAnnounceList",
        "data": {"rp": 10, "page": 1, "categorys": ["21"], "labs": [], "keyword": ""},
    }
    with httpx.Client() as client:
        res = client.post(url=id_url, headers=getID_headers, json=data)
        res = json.loads(res.text)
        total = res["data"]["total"]
        # print(total)
        with open(dirs + "tx_id_history.log", "r+") as f:
            old_total = int(f.readlines()[0].strip())
            if total <= old_total:
                # print("【!】暂时无新漏洞！！！")
                exit()
            else:
                content = f.read()
                f.seek(0, 0)
                f.write(str(total) + "\n" + content)
                # f.writelines(str(total))
                for i in range(10):
                    page_id.append(res["data"]["rows"][i]["announceId"])


# 获取漏洞详情
def getInfo():
    global page_id, total, titles, descriptions
    with httpx.Client() as client:
        for i in range(total - old_total):
            url = info_url + str(page_id[i])
            res = client.get(url=url, headers=getInfo_headers)
            # print(res.text)
            a = re.compile(r"<h1>【安全通告】(.*?)</h1>", re.S)  # 获取标题
            b = re.compile(r"攻击者利用(.*?)</div>", re.S)  # 漏洞风险
            c = re.compile(r"风险等级.*?bold;\">(.*?)</span>", re.S)  # 风险等级

            e = re.compile(
                r"<span id=\"date\" style=\"font-family: 微软雅黑; font-size: 14px;\">(.*?)</span>",
                re.S,
            )  # 通过时间

            titles.append(re.findall(a, res.text)[0])
            descriptions.append(re.findall(b, res.text)[0])
            risks.append(re.findall(c, res.text)[0])
            times.append(re.findall(e, res.text)[0])


# 发送@all信息
# def send_all():
#     # global headers
#     data = {"msgtype": "text", "text": {"content": "", "mentioned_list": ["@all"]}}
#     with httpx.Client() as client:
#         client.post(webhook_addr, headers=tx_headers, json=data)

# 格式化通告信息
def format_data():

    for i in range(total - old_total):
        url = info_url + str(page_id[i])
        title = titles[i]
        time = times[i]
        risk = risks[i]
        description = descriptions[i]
        # print(title, time, risk, description)
        send_data = {
            "msgtype": "markdown",
            "markdown": {
                "content": "#### "
                + title
                + "\n>通告时间:"
                + time
                + "\n>风险等级:`**"
                + risk
                + '**`\n>漏洞风险:<font color="comment">'
                + description
                + "</font>\n[查看详情🔎]("
                + url
                + ")"
            },
        }
        # print(send_data)
        send_tg(send_data)


# 发送的企微机器人
def send_tg(send_data):
    try:
        # with httpx.Client() as client:
        r = httpx.post(url=webhook_addr, headers=tx_headers, json=send_data)
        with open(dirs + "tx_history.log", "a") as f:
            f.writelines(r.text + "\n")
        # print(r.text)

    except:
        exit()


def main():
    getID()
    getInfo()
    format_data()


if __name__ == "__main__":
    main()
