#!/usr/bin/env python
#!encoding=utf-8


## python2内置yaml模块, python3则需要使用pip安装PyYAML
import yaml
import sys
import os
import base64

def parse_yaml(target_file, curr_dir):
    # 打开yaml文件
    file = open(target_file, 'r')
    file_data = file.read()
    file.close()

    # 将字符串转化为字典或列表
    data = yaml.safe_load(file_data)
    ca_crt = data['clusters'][0]['cluster']['certificate-authority-data']
    client_crt = data['users'][0]['user']['client-certificate-data']
    client_key = data['users'][0]['user']['client-key-data']

    file_ca_crt = open(curr_dir + '/ca.crt', 'wb')
    file_ca_crt.write(base64.b64decode(ca_crt))
    file_ca_crt.close()

    file_client_crt = open(curr_dir + '/client.crt', 'wb')
    file_client_crt.write(base64.b64decode(client_crt))
    file_client_crt.close()

    file_client_key = open(curr_dir + '/client.key', 'wb')
    file_client_key.write(base64.b64decode(client_key))
    file_client_key.close()


if __name__ == '__main__':
    ## python k2file.py /etc/kubernetes/admin.conf 的 argv 中不包含 `python`
    if len(sys.argv) == 3: 
        print("请指定配置文件路径")
        sys.exit(-1)

    target_file = ''
    curr_dir = os.getcwd()
    ## 判断 python 版本.
    if sys.version_info < (3, 0):
        ## python2
        import os
        target_file = os.path.join(curr_dir, sys.argv[1])
    else:
        ## python3
        from pathlib import Path
        target_file = Path(curr_dir).joinpath(sys.argv[1])
    print('yaml file: ', target_file)
    parse_yaml(target_file, curr_dir)

