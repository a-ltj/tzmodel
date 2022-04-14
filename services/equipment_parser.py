#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-
import cv2
from models.Equipment import Equipment
from utils.parser_util import match_template, erase_img
from models.Target import Target


def parse_equipments(targets):
    """ 解析设备信息
    """
    # 检测到的所有设备
    equipments = []


    for target in targets:
        equipment = Equipment(target)
        equipments.append(equipment)
        # img_gray = erase_img(img_gray, [[target.getX(), target.getY(), target.getX()+target.getWidth(),
        #                                  target.getY()+target.getHeight()] for target in targets])


        # 为设备设置ID值
    index = 1000001
    for equip in equipments:
        equip.setID(index)
        index += 1

    # 返回检测到的所有设备
    return equipments
