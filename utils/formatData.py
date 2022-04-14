import httpx

import utils.globalVariable as glv


# 格式化通告信息-腾讯云
def format_tx():
    info_url = "https://cloud.tencent.com/announce/detail/"  # + id
    total = glv.get("total")
    old_total = glv.get("old_total")
    page_id = glv.get("page_id")
    titles = glv.get("titles")
    times = glv.get("times")
    risks = glv.get("risks")
    descriptions = glv.get("descriptions")
    versions = glv.get("versions")
    import utils.sendTg as sendTg

    for i in range(total - old_total):
        url = info_url + str(page_id[i])
        title = str(titles[i])
        title = title.replace("【安全通告】", "")  # 替换多余的文字
        time = times[i]
        risk = risks[i]
        description = descriptions[i]
        version = versions[i]
        version = version.replace("\n\n", "\n")  # 替换掉多余空行
        # print(version)
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
                + "</font>\n>影响版本:\n`"
                + version
                + "`[查看详情🔎]("
                + url
                + ")"
            },
        }

        sendTg.send_qywx(send_data)
