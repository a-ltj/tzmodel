#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-

from models.Target import Target


class Label(Target):
    """ 标签类
    """

    def __init__(self, target):
        Target.__init__(self, target.getType(), target.getX(), target.getY(), target.getWidth(),target.getHeight())

    def setID(self, id):
        self.__id = id

    def getID(self):
        return self.__id

    def setValue(self, value):
        self.__value = value

    def getValue(self):
        return self.__value
