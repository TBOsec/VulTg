# coding:utf-8
import json
import os

import httpx
from rich import print

home = os.environ["HOME"]
dirs = home + "/.config/vul_TG/"
id_url = "https://cloud.tencent.com/announce/ajax"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4495.0 Safari/537.36"
# header头部
getID_headers = {
    "User-Agent": user_agent,
    "Referer": "https://cloud.tencent.com/announce?page=1&categorys=21",
    "Content-Type": "application/json; charset=UTF-8",
    "Origin": "https://cloud.tencent.com",
}
data = {
    "action": "getAnnounceList",
    "data": {
        "rp": 10,
        "page": 1,
        "categorys": ["21"],
        "labs": [],
        "keyword": "",
    },
}


def req():
    with httpx.Client() as client:
        res = client.post(url=id_url, headers=getID_headers, json=data)
        res = json.loads(res.text)
        total = res["data"]["total"]
    return res, total


def init():
    # print("[bold cyan]...正在进行初始化！[/bold cyan]...")
    res, total = req()
    # print(total)
    with open(dirs + "tx_id_history.log", "w") as f:
        f.write(str(total))
    exit()
