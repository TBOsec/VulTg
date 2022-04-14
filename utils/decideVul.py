import utils.globalVariable as glv
import utils.initFile as Init


# 获取漏洞ID号
def txVulID():

    res, total = Init.req()
    glv.set("total", total)  # 设置全局变量
    page_id = []  # 文章ID号
    dirs = glv.get("dirs")
    with open(dirs + "tx_id_history.log", "r+") as f:
        old_total = int(f.readlines()[0].strip())
        glv.set("old_total", old_total)
        if total <= old_total:

            return False  # print("【!】暂时无新漏洞！！！")
        else:

            f.seek(0, 0)
            f.write(str(total) + "\n")
            for i in range(10):
                page_id.append(res["data"]["rows"][i]["announceId"])
            glv.set("page_id", page_id)
            return True
