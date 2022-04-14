#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-

import os
from math import sqrt
import cv2
import numpy as np
from PIL import Image, ImageDraw
import math

from models.Target import Target


def erase_img(img, areas, fill='white'):
    """ 删除图片中的特定区域
    """
    img_gray = Image.fromarray(img)
    draw = ImageDraw.Draw(img_gray)
    for area in areas:
        draw.rectangle(area, fill=fill)
    del draw
    return np.array(img_gray)


def cal_distance(pt1, pt2):
    """ 计算两点之间的欧式距离
    """
    if len(pt1) != 2 or len(pt2) != 2:
        return None
    return int(sqrt(pow(abs(pt1[0] - pt2[0]), 2) + pow(abs(pt1[1] - pt2[1]), 2)))


def check_unique_pt(pts, check_pt, threshold=10):
    """ 检测唯一点
    """
    for pt in pts:
        if cal_distance(pt, check_pt) <= threshold:
            return False
    return True


def resize_img(img, fx, fy):
    """ 图片缩放扩大
    """
    new_img = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
    return new_img


def match_template(img_gray, template):
    """ 多尺寸模板匹配
    """
    # 匹配到的所有目标
    targets = []

    # 获取模板文件夹下所有的模板文件路径
    files = os.listdir(template.getTemplatePath())
    spec_templates = []
    for file in files:
        file_path = os.path.join(template.getTemplatePath(), file)
        spec_templates.append(file_path)

    # 对每个模板逐次进行多尺寸匹配
    pts = []
    for spec_template in spec_templates:
        spec_template_gray = cv2.imdecode(np.fromfile(spec_template, dtype=np.uint8), 0)

        # 正常尺寸模板匹配
        res = cv2.matchTemplate(img_gray, spec_template_gray, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= template.getSimilarity())
        for pt in zip(*loc[::-1]):
            if check_unique_pt(pts, pt):
                pts.append(pt)
                target = Target(template.getType(), pt[0], pt[1], spec_template_gray.shape[1],
                                spec_template_gray.shape[0], spec_template)
                targets.append(target)

        # 缩小尺寸进行模板匹配
        for i in range(1, 11):
            factor = pow(0.95, i)
            small_template = resize_img(spec_template_gray, factor, factor)
            res = cv2.matchTemplate(img_gray, small_template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= template.getSimilarity())
            for pt in zip(*loc[::-1]):
                if check_unique_pt(pts, pt):
                    pts.append(pt)
                    target = Target(template.getType(), pt[0], pt[1], spec_template_gray.shape[1],
                                    spec_template_gray.shape[0], spec_template)
                    targets.append(target)

        # 放大尺寸进行模板匹配
        for i in range(1, 11):
            factor = pow(1.05, i)
            large_template = resize_img(spec_template_gray, factor, factor)
            res = cv2.matchTemplate(img_gray, large_template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= template.getSimilarity())
            for pt in zip(*loc[::-1]):
                if check_unique_pt(pts, pt):
                    pts.append(pt)
                    target = Target(template.getType(), pt[0], pt[1], spec_template_gray.shape[1],
                                    spec_template_gray.shape[0], spec_template)
                    targets.append(target)

    # 返回匹配到的所有目标
    return targets


# 两点距离
def point_distance(point1, point2):
    p1 = np.array(point1)
    p2 = np.array(point2)
    p3 = p2 - p1
    p4 = math.hypot(p3[0], p3[1])
    return p4


def takeFirst(equipment):
    return equipment.getY()


def texts_relevance(equipments, labels):
    rel_labels = [label for label in labels]
    equipments.sort(key=takeFirst)
    for equipment in equipments:
        point1 = ((equipment.getX()+equipment.getWidth()/2), (equipment.getY()+equipment.getHeight()/2))
        min_distance = 9999
        current_label = None
        for label in rel_labels:
            point2 = ((label.getX() + label.getWidth() / 2), (label.getY() + label.getHeight() / 2))
            current_distance = point_distance(point1, point2)
            if current_distance < min_distance:
                min_distance = current_distance
                current_label = label
        if current_label is not None:
            rel_labels.remove(current_label)
            equipment.setTextID(current_label.getID())
    return equipments, labels


def point_distance(point1, point2):
    p1 = np.array(point1)
    p2 = np.array(point2)
    p3 = p2 - p1
    p4 = math.hypot(p3[0], p3[1])
    return p4


def find_nearest_equip(point, equipments):
    min_dist = 10000
    nearest_equip = None
    for equipment in equipments:
        mid_point = ((equipment.getX()+equipment.getWidth()/2), (equipment.getY()+equipment.getHeight()/2))
        cur_distance = point_distance(point, mid_point)
        if cur_distance < min_dist:
            min_dist = cur_distance
            nearest_equip = equipment
    if min_dist < 30:
        return nearest_equip
    else:
        return None




