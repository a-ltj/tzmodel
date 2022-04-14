#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-

import xml.dom.minidom

from models.Template import Template


def load_conf(conf_file):
    """
    解析配置文件
    :param conf_file: 配置文件路径
    :return: 所有的设备模板信息
    """
    # 使用minidom解析器打开XML文档
    DOMTree = xml.dom.minidom.parse(conf_file)
    root = DOMTree.documentElement

    # 获取配置文件中设备模板信息
    templates = []
    equips_confs = root.getElementsByTagName('equipments')
    if len(equips_confs) != 0:
        equips_conf = equips_confs[0]
        equip_confs = equips_conf.getElementsByTagName('equipment')
        for equip_conf in equip_confs:
            # 获取设备基本信息
            type = equip_conf.getElementsByTagName('type')[0].childNodes[0].data
            template = equip_conf.getElementsByTagName('template')[0].childNodes[0].data
            similarity = float(equip_conf.getElementsByTagName('similarity')[0].childNodes[0].data)
            template = Template(type, template, similarity)
            templates.append(template)

    # 返回配置文件相关信息
    return templates
