#!/usr/bin/python3
# -*- coding utf-8 -*-
# @Description: Altium 器件坐标转换
# @Author: diyhome
# @Date: 2021/7/21 16:50
import re
import os

txt_path = ""
dir_path = ""
new_name = ""

def readData(path):
    """
    读取源文件
    :param path: 源文件路径
    :return: 文件内容List
    """
    with open(path, 'r', encoding='ANSI') as f:
        data = f.readlines()
    return data


def getColPos(input_data):
    """
    获取列的开始位置
    :param input_data: 读取出来的文件列表
    :return: {[列名,开始位置]}
    """
    data = []

    # 原始文件头
    bool_begin_get_data = False
    for item in input_data:
        if not bool_begin_get_data:
            if "Designator" not in item:
                continue
            else:
                bool_begin_get_data = True
        data.append(item)
    col_count = []
    pos_point = 1
    for item in data[0].replace("\n", "").split(" "):
        if len(item) != 0:
            col_count.append([item, pos_point])
            pos_point += len(item)
        pos_point += 1
    return col_count


def generate_csv(input_data):
    data = []
    bool_begin_get_data = False
    for item in input_data:
        if not bool_begin_get_data:
            if "Designator" not in item:
                continue
            else:
                bool_begin_get_data = True
        data.append(re.sub(r'[ ]+', ',', item).rstrip(","))
    with open(dir_path + new_name, 'w+', encoding="utf-8") as f:
        f.writelines(data)


if __name__ == "__main__":
    txt_path = input("拖动导出文件到这里:")
    txt_path = txt_path.strip('"')
    dir_path = os.path.dirname(txt_path) + "/"
    new_name = os.path.basename(txt_path).split('.')[0] + "_修改这个.csv"

    data_raw = readData(txt_path)
    pos_data = getColPos(data_raw)
    fomat_data = []
    for item in data_raw:
        if "Designator" in item:
            break
        fomat_data.append(item)
    if not os.path.exists(dir_path+new_name):
        generate_csv(data_raw)
        print("使用Excel编辑{0}".format(new_name))
    else:
        with open(dir_path + new_name, 'r', encoding="utf-8") as f:
            read_buf = f.readlines()
        for read_tmp in read_buf:
            res = ""
            list_index = 0
            tmp = read_tmp.replace(",\n", "").strip().split(',')
            for item in tmp:
                if pos_data[list_index][1] == 1:
                    res += item
                else:
                    for i in range(0, pos_data[list_index][1] - len(res) - 1):
                        res += " "
                    res += item
                list_index += 1
            fomat_data.append(res + "\n")
        with open(dir_path + os.path.basename(txt_path).split('.')[0] + "_修改后.txt", 'w+', encoding="utf-8") as f:
            f.writelines(fomat_data)
        print("使用Altium导入{0}".format(os.path.basename(txt_path).split('.')[0] + "_修改后.txt"))
