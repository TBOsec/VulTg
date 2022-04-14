import re

import httpx
from bs4 import BeautifulSoup

import utils.globalVariable as glv

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4495.0 Safari/537.36"
getInfo_headers = {
    "User-Agent": user_agent,
    "Referer": "https://cloud.tencent.com/announce?page=1&categorys=21",
}
info_url = "https://cloud.tencent.com/announce/detail/"  # + id
# 获取漏洞详情
def getInfo_tx():
    # global page_id, total, titles, descriptions
    titles = []  # 文章标题
    times = []  # 通告时间
    descriptions = []  # 漏洞风险
    risks = []  # 风险等级
    versions = []  # 影响版本
    total = glv.get("total")
    old_total = glv.get("old_total")
    page_id = glv.get("page_id")
    with httpx.Client() as client:
        for i in range(total - old_total):
            url = info_url + str(page_id[i])
            html_doc = httpx.get(url=url, headers=getInfo_headers)

            html_doc = html_doc.text
            soup = BeautifulSoup(html_doc, "lxml")

            # 获取标题
            title = soup.find("h1").string
            titles.append(title)
            # 通告时间
            date = soup.find(id="date").string
            times.append(date)

            all = re.compile(r"影响版本.*?</div>(.*?)修复建议", re.S)
            all = re.findall(all, html_doc)[0]
            version = ""
            if "安全版本" in all:
                if "排查办法" in all:
                    # print("1")
                    data1 = re.compile(r"(.*?)<span.*?排查办法", re.S)
                    data1 = re.findall(data1, all)[0]
                    soup = BeautifulSoup(data1, "lxml")
                    for info in soup.find("div").contents:
                        if str(info) == "<br/>":
                            version += "\n"
                        else:
                            version += info.string
                    versions.append(version)
                else:
                    # print("2")
                    data2 = re.compile(r"(.*?)安全版本", re.S)
                    data2 = re.findall(data2, all)[0]
                    soup = BeautifulSoup(data2, "lxml")
                    for info in soup.find("div").contents:
                        if str(info) == "<br/>":
                            version += "\n"
                        else:
                            version += info.string
                            # print(info.string, end="")
                    versions.append(version)

            # 风险等级
            risk = re.compile(r"风险等级.*?bold;\">(.*?)</span>", re.S)
            risks.append(re.findall(risk, html_doc)[0])
            # 漏洞风险
            description = re.compile(r"攻击者利用(.*?)</div>", re.S)
            descriptions.append(re.findall(description, html_doc)[0])
        glv.set("titles", titles)
        glv.set("times", times)
        glv.set("descriptions", descriptions)
        glv.set("versions", versions)
        glv.set("risks", risks)
