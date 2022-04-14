#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-

from models.Label import Label
from models.Template import Template
from utils.parser_util import match_template, erase_img


def check_intersection(scope1, scope2):
    """ 检测直线上两条线段是否有交集
    """
    if (scope2[0] < scope1[0] < scope2[1] or scope2[0] < scope1[1] < scope2[1] or
        (scope1[0] == scope2[0] and scope1[1] == scope2[1])) or \
            (scope1[0] < scope2[0] < scope1[1] or scope1[0] < scope2[1] < scope1[1] or
             (scope2[0] == scope1[0] and scope2[1] == scope1[1])):
        return True
    return False


def check_common_label(parent_label, sub_label):
    """ 检测子标签是否可以合并到父标签
    """
    if abs(parent_label.getX() + parent_label.getWidth() - sub_label.getX()) < 10 and \
            check_intersection((parent_label.getY(), parent_label.getY() + parent_label.getHeight()),
                               (sub_label.getY(), sub_label.getY() + sub_label.getHeight())):
        return True
    return False


def merge_labels(parent_label, sub_label):
    """ 将子标签合并到父标签
    """
    # 更新值
    new_value = parent_label.getValue() + sub_label.getValue()
    parent_label.setValue(new_value)

    # 更新标签纵坐标 y
    new_y = min(parent_label.getY(), sub_label.getY())
    parent_label.setY(new_y)

    # 更新标签高度 height
    new_height = max(parent_label.getY() + parent_label.getHeight(), sub_label.getY() + sub_label.getHeight()) - new_y
    parent_label.setHeight(new_height)

    # 更新标签宽度 width
    new_width = sub_label.getX() + sub_label.getWidth() - parent_label.getX()
    parent_label.setWidth(new_width)


def combine_labels(labels):
    """ 对单个标签进行组合
    """
    cmb_labels = []

    labels.sort(key=lambda label: label.getX())
    for label in labels:
        flag = False

        for cmb_label in cmb_labels:
            if check_common_label(cmb_label, label):
                merge_labels(cmb_label, label)
                flag = True
                break

        if not flag:
            cmb_labels.append(label)

    return cmb_labels


def get_label_templates():
    """ 临时产生所有的标签模板
    """
    templates = []

    # 文字标签模板
    template_word_1 = Template('Label', 'resources/label_templates/word/嘉汉线/', 0.7)
    template_word_2 = Template('Label', 'resources/label_templates/word/汉郑线/', 0.7)
    template_word_3 = Template('Label', 'resources/label_templates/word/#1主变/', 0.7)
    template_word_4 = Template('Label', 'resources/label_templates/word/220kV/', 0.7)
    template_word_5 = Template('Label', 'resources/label_templates/word/500kVI母/', 0.7)
    template_word_6 = Template('Label', 'resources/label_templates/word/500kVII母/', 0.7)
    template_word_7 = Template('Label', 'resources/label_templates/word/35kV/', 0.7)
    template_word_8 = Template('Label', 'resources/label_templates/word/501117/', 0.68)
    template_word_9 = Template('Label', 'resources/label_templates/word/505117/', 0.68)
    template_word_10 = Template('Label', 'resources/label_templates/word/502117/', 0.65)
    template_word_11 = Template('Label', 'resources/label_templates/word/5011/', 0.7)
    template_word_12 = Template('Label', 'resources/label_templates/word/5052/', 0.7)
    templates.append(template_word_1)
    templates.append(template_word_2)
    templates.append(template_word_3)
    templates.append(template_word_4)
    templates.append(template_word_5)
    templates.append(template_word_6)
    templates.append(template_word_7)
    templates.append(template_word_8)
    templates.append(template_word_9)
    templates.append(template_word_10)
    templates.append(template_word_11)
    templates.append(template_word_12)

    # 数字标签模板
    template_0 = Template('Label', 'resources/label_templates/digit/0/', 0.65)
    template_1 = Template('Label', 'resources/label_templates/digit/1/', 0.9)
    template_2 = Template('Label', 'resources/label_templates/digit/2/', 0.65)
    template_5 = Template('Label', 'resources/label_templates/digit/5/', 0.67)
    template_6 = Template('Label', 'resources/label_templates/digit/6/', 0.8)
    template_7 = Template('Label', 'resources/label_templates/digit/7/', 0.8)
    templates.append(template_0)
    templates.append(template_1)
    templates.append(template_2)
    templates.append(template_5)
    templates.append(template_6)
    templates.append(template_7)

    return templates


def parse_labels(targets,texts):
    """ 解析标签
    """
    # 检测到的所有标签
    labels = []

    # 获取所有的标签模板
    #templates = get_label_templates()

    # 逐次检测每种标签

    for target,text in zip(targets,texts):
        label = Label(target)
        label.setValue(text)
        labels.append(label)
        # img_gray = erase_img(img_gray, [[target.getX(), target.getY(), target.getX()+target.getWidth(),
        #                                  target.getY()+target.getHeight()] for target in targets])

    # 组合标签
    cmb_labels = combine_labels(labels)

    # 为标签设置ID值
    index = 2000001
    for label in cmb_labels:
        label.setID(index)
        index += 1

    # 返回检测到的所有标签
    return  cmb_labels
