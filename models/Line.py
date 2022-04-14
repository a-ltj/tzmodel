#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-


class Line():
    """ 直线类
    """

    def __init__(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

    def getX1(self):
        return self.__x1

    def setX1(self, x1):
        self.__x1 = x1

    def getY1(self):
        return self.__y1

    def setY1(self, y1):
        self.__y1 = y1

    def getX2(self):
        return self.__x2

    def setX2(self, x2):
        self.__x2 = x2

    def getY2(self):
        return self.__y2

    def setY2(self, y2):
        self.__y2 = y2
