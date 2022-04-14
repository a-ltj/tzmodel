#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-

import cv2
import numpy as np

from conf.config import EQUIP_PARSER_CONF
from models.Bus import Bus
from models.ConnectLine import ConnectLine
from services import label_parser, equipment_parser, line_parser
from services import demofenge
from label import demo
from utils.conf_util import load_conf
from utils.parser_util import texts_relevance, find_nearest_equip

BUS_LENGTH_THRESHOLD = 500


def get_horizontal_length(element):
    """ 获取水平直线的长度
    """
    return element.getX2() - element.getX1()


def get_vertical_length(element):
    """ 获取垂直直线的长度
    """
    return element.getY2() - element.getY1()


def get_Y1(element):
    """ 获取直线Y1值
    """
    return element.getY1()


def get_substation_info(image_name):
    """
    从图片名称中获取场站信息
    :param image_name: 图片名称
    :return: 场站信息，包括场站名、场站类型
    """
    prefix = image_name.split('.')[0]
    infos = prefix.split('_')
    sub_name = infos[0]
    sub_type = infos[1]
    return sub_name, sub_type


def parse_image(image_name, image_path):
    """
    接线图识别入口
    :param image_name: 待识别的图片名称
    :param image_path: 待识别的图片路径
    :return: 图片识别结果，格式遵循规则说明中的xml规范
    """
    # 从图片名称中获取场站信息
    sub_name, sub_type = get_substation_info(image_name)
    print(sub_name)

    # 将原图转换为灰度图

    img_gray = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), 0)

    # 解析设备
    targets = demofenge.demo(image_name,image_path)
    equipments = equipment_parser.parse_equipments(targets)

    # 解析标签
    targets,texts= demo.main(image_path)
    labels = label_parser.parse_labels(targets,texts)

    # # 解析直线
    # lines = line_parser.parse_lines(img_gray)
    # horizontal_lines = lines['horizontal']
    # vertical_lines = lines['vertical']
    # print(type(vertical_lines))
    # print(vertical_lines)
    #
    # # 直线划分，母线、连接线
    # buses = []
    # connect_lines = []
    #
    # # 划分母线
    # horizontal_lines.sort(key=get_horizontal_length, reverse=True)
    # delete_horizontal_lines = []
    # for hor_line in horizontal_lines:
    #     if hor_line.getX2() - hor_line.getX1() > BUS_LENGTH_THRESHOLD:
    #         bus = Bus(hor_line.getX1(), hor_line.getY1(), hor_line.getX2(),
    #                   hor_line.getY2())
    #         buses.append(bus)
    #         delete_horizontal_lines.append(hor_line)
    #     else:
    #         break
    # for delete_horizontal_line in delete_horizontal_lines:
    #     horizontal_lines.remove(delete_horizontal_line)
    #
    # bus_index = 1000001 + len(equipments)
    # for bus in buses:
    #     bus.setID(bus_index)
    #     bus_index += 1
    #
    # # 划分连接线
    # for hor_line in horizontal_lines:
    #     conn_line = ConnectLine(hor_line.getX1(), hor_line.getY1(), hor_line.getX2(), hor_line.getY2())
    #     connect_lines.append(conn_line)
    # for ver_line in vertical_lines:
    #     conn_line = ConnectLine(ver_line.getX1(), ver_line.getY1(), ver_line.getX2(), ver_line.getY2())
    #     connect_lines.append(conn_line)
    #
    # conn_index = 3000001
    # for conn_line in connect_lines:
    #     conn_line.setID(conn_index)
    #     conn_index += 1
    #
    # # 设备与文本匹配
    # texts_relevance(equipments, labels)
    #
    # # 连接线与设备的连接关系
    # for conn_line in connect_lines:
    #     start_point = (conn_line.getX1(), conn_line.getY1())
    #     end_point = (conn_line.getX2(), conn_line.getY2())
    #     # 计算起点连接的设备
    #     start_equip = find_nearest_equip(start_point, equipments)
    #     if start_equip is not None:
    #         conn_line.add_link('0,0,' + str(start_equip.getID()))
    #     # 计算终点连接的设备
    #     end_equip = find_nearest_equip(end_point, equipments)
    #     if end_equip is not None:
    #         conn_line.add_link('1,1,' + str(end_equip.getID()))

    # 生成xml
    res_xml = '<?xml version="1.0" encoding="utf-8"?>\n'
    res_xml += '<result w="' + str(img_gray.shape[1]) + '" h="' + str(img_gray.shape[0]) + '">\n'

    # 生成厂站基本信息xml
    res_xml += '    <subinfo>\n'
    res_xml += '        <info SubstationName="' + sub_name + '" SubstationType="' + sub_type + '" VoltageGrade="500kV"/>\n'
    res_xml += '    </subinfo>\n'

    # 生成设备信息xml
    res_xml += '    <icons>\n'
    for equip in equipments:
        #rotate = equip.getTemplate().split('.')[0].split('_')[-1]
        box = str(equip.getX()) + ',' + str(equip.getY()) + ';' + str(equip.getX() + equip.getWidth()) + ',' + \
              str(equip.getY() + equip.getHeight())
        # res_xml += '        <icon id="' + str(equip.getID()) + '" vol="500" type="' + equip.getType() + '" box="' + \
        #            box + '" rotate="' + rotate + '" textId="' + str(equip.getTextID()) + '"/>\n'
        res_xml += '        <icon id="' + str(equip.getID()) + '" vol="500" type="' + equip.getType() + '" box="' + \
                   box + '"/>\n'

    # 生成母线信息xml
    # for bus in buses:
    #     box = str(bus.getX1()) + ',' + str(bus.getY1()) + ';' + str(bus.getX2()) + ',' + str(bus.getY2() + 5)
    #     res_xml += '        <icon id="' + str(bus.getID()) + '" vol="500" type="Bus" box="' + box + \
    #                '" rotate="0" textId=""/>\n'
    #
    # res_xml += '    </icons>\n'
    #
    # 生成文字信息xml
    res_xml += '    <texts>\n'
    for text in labels:
        box = str(text.getX()) + ',' + str(text.getY()) + ';' + str(text.getX() + text.getWidth()) + ',' + \
              str(text.getY() + text.getHeight())
        res_xml += '        <text id="' + str(text.getID()) + '" content="' + text.getValue() + '" box="' + box + \
                   '"/>\n'
    res_xml += '    </texts>\n'
    #
    # # 生成连接线信息xml
    # res_xml += '    <links>\n'
    # for line in connect_lines:
    #     res_xml += '        <link id="' + str(line.getID()) + '" ids="' + line.link_str() + '" path="' + str(
    #         line.getX1()) + ',' + str(line.getY1()) + ';' + str(line.getX2()) + ',' + str(line.getY2()) + '"/>\n'
    # res_xml += '    </links>\n'

    res_xml += '</result>'

    # 返回结果
    return res_xml
