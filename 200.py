# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 20:41
# @Author  : lagelanren
# @Email   : forhaogege@163.com
# @File    : 200.py
# @Software: PyCharm

import re, os
re_str = "TCP_ERROR[\S\s]*?\);[\S\s]*?\);"
re_str_params = "\((.*)?\);"
new_code_template_one = 'TcpErrLog({}, {}, {}, {}, {}, {});'
new_code_template_two = 'TcpErrLog({}, {}, {}, {});'
if __name__ == '__main__':
    base_dir = input("输入文件夹")
    result_dir = os.path.join(base_dir, "result")
    os.mkdir(result_dir)
    for item_file in os.listdir(base_dir):
        if item_file.endswith("c"):
            with open(os.path.join(base_dir, item_file),"r") as file:
                new_code = []
                code = file.read()
                code_new = code
                waiter_code = re.findall(re_str, code)
                for item in waiter_code:
                    if("%s" in item):
                        continue
                    item = item.replace("%d,","@")
                    part_one, part_two, _ = item.split(";")
                    part_one = part_one.strip() + ";"
                    part_two = part_two.strip() + ";"
                    part_one_params = re.findall(re_str_params, part_one)[0].split(",")
                    part_two_params = re.findall(re_str_params, part_two)[0].split(",")
                    part_one_params = [item_params.strip() for item_params in part_one_params]
                    part_two_params = [item_params.strip() for item_params in part_two_params]
                    if(len(part_one_params[4:])<=4):
                        if(part_one_params[3].split("X")[-1] != '"'):
                            item_new_code = new_code_template_one.format(part_two_params[0], part_two_params[2],
                                                                         part_one_params[2], part_one_params[3],
                                                                         '"'+part_one_params[3].split("X")[-1].strip(),
                                                                         ", ".join(part_one_params[4:]))
                        else:
                            item_new_code = new_code_template_two.format(part_two_params[0], part_two_params[2],
                                                                         part_one_params[2], part_one_params[3])
                        item = item.replace("@", "%d,")
                        item_new_code = item_new_code.replace("@", "%d,")
                        code_new = code_new.replace(item, item_new_code)

                with open(os.path.join(result_dir,item_file), "w") as file:
                    file.write(code_new)
                print(item_file + "--------处理完成")






