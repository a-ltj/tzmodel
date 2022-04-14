#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-


class Template:
    """ 匹配模板类
    """

    def __init__(self, type, template_path, similarity):
        self.__type = type
        self.__template_path = template_path
        self.__similarity = similarity

    def getType(self):
        return self.__type

    def getTemplatePath(self):
        return self.__template_path

    def getSimilarity(self):
        return self.__similarity
