# coding:utf-8
"""
Created on Mar 9, 2021
@author: TBOsec   
"""
import argparse

# import json
# import os
# import re
from sys import exit

import utils.globalVariable as glv
import utils.initFile as Init

# import httpx


glv._init()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-init", help="初始化通告数据", action="store_true")
    args = parser.parse_args()
    if True == args.init:
        Init.init()
    else:
        import utils.decideVul as decideVul

        flag = decideVul.txVulID()
        if flag:
            import utils.vulInfo as vulInfo

            vulInfo.getInfo_tx()
            import utils.formatData as formatData

            formatData.format_tx()
        else:
            exit()
    # getID()

    # getInfo()
    # format_data()


if __name__ == "__main__":
    main()
