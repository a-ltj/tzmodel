#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-


class Target:
    """ 匹配目标类
    """

    def __init__(self, type, x, y, width, height):
        self.__type = type
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        #self.__template = template

    def getType(self):
        return self.__type

    def setType(self, type):
        self.__type = type

    def getX(self):
        return self.__x

    def setX(self, x):
        self.__x = x

    def getY(self):
        return self.__y

    def setY(self, y):
        self.__y = y

    def getWidth(self):
        return self.__width

    def setWidth(self, width):
        self.__width = width

    def getHeight(self):
        return self.__height

    def setHeight(self, height):
        self.__height = height

    # def getTemplate(self):
    #     return self.__template
    #
    # def setTemplate(self, template):
    #     self.__template = template
