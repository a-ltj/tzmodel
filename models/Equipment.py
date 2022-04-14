#!/usr/bin/env/ python3
# -*- encoding: utf-8 -*-

from models.Target import Target


class Equipment(Target):
    """ 设备类
    """

    def __init__(self, target):
        Target.__init__(self, target.getType(), target.getX(), target.getY(), target.getWidth(),target.getHeight())

    def setID(self, id):
        self.__id = id

    def getID(self):
        return self.__id

    def setTextID(self, text_id):
        self.__text_id = text_id

    def getTextID(self):
        return self.__text_id
