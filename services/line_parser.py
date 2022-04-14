#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-

from models.Line import Line
from models.Template import Template
from utils.parser_util import match_template


def check_horizontal_combine(line, pt):
    """ 检测水平点是否可以合并到水平线
    """
    if abs(line.getY1() - pt.getY()) < 10 and abs(line.getX2() - pt.getX()) < 15:
        return True
    return False


def combine_horizontal_pt(line, pt):
    """ 将水平点合并到水平线
    """
    line.setX2(pt.getX() + pt.getWidth())


def combine_horizontal_lines(horizontal_pts):
    """ 水平点组合成为水平线
    """
    horizontal_lines = []

    horizontal_pts.sort(key=lambda pt: pt.getX())
    for pt in horizontal_pts:
        flag = False
        for line in horizontal_lines:
            if check_horizontal_combine(line, pt):
                combine_horizontal_pt(line, pt)
                flag = True
                break
        if not flag:
            new_line = Line(pt.getX(), pt.getY(), pt.getX() + pt.getWidth(), pt.getY())
            horizontal_lines.append(new_line)

    return horizontal_lines


def check_vertical_combine(line, pt):
    """ 检测垂直点是否可以合并到垂直线
    """
    if abs(line.getX1() - pt.getX()) < 10 and abs(line.getY2() - pt.getY()) < 15:
        return True
    return False


def combine_vertical_pt(line, pt):
    """ 将垂直点合并到垂直线
    """
    line.setY2(pt.getY() + pt.getHeight())


def combine_vertical_lines(vertical_pts):
    """ 垂直点组成垂直线
    """
    vertical_lines = []

    vertical_pts.sort(key=lambda pt: pt.getY())
    for pt in vertical_pts:
        flag = False
        for line in vertical_lines:
            if check_vertical_combine(line, pt):
                combine_vertical_pt(line, pt)
                flag = True
                break
        if not flag:
            new_line = Line(pt.getX(), pt.getY(), pt.getX(), pt.getY() + pt.getHeight())
            vertical_lines.append(new_line)

    return vertical_lines


def parse_lines(img_gray):
    """ 解析直线
    """
    # 检测到的所有直线
    lines = {}

    # 检测水平直线
    horizontal_pt_temp = Template('Point', 'resources/line_templates/horizontal/', 0.8)
    horizontal_pts = match_template(img_gray, horizontal_pt_temp)
    horizontal_lines = combine_horizontal_lines(horizontal_pts)

    # 检测垂直直线
    vertical_pt_temp = Template('Point', 'resources/line_templates/vertical/', 0.8)
    vertical_pts = match_template(img_gray, vertical_pt_temp)
    vertical_lines = combine_vertical_lines(vertical_pts)

    # 返回所有直线
    lines['horizontal'] = horizontal_lines
    lines['vertical'] = vertical_lines
    return lines
