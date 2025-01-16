#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:张红
# from common.public import base_dir
import json
import os.path

import yaml

from others.测试相关.api_baofyy import base_dir


def readJson():
         return json.load(open(file=os.path.join(base_dir(),'testdata','fengbao.json'),encoding='utf-8'))

# print(readJson())

def readYaml():
        with open(file=os.path.join(base_dir(),'config','url.sina.yaml'),encoding="utf-8")as f:
            return yaml.safe_load(f)
# print(readYaml())